import os
import io
import json
import numpy as np
import torch
import open_clip
import faiss
import cv2
from PIL import Image
from flask import Flask, request, jsonify, render_template, Response, stream_with_context

from story_engine import StoryEngine

from dotenv import load_dotenv
load_dotenv()

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["OMP_NUM_THREADS"] = "1"

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r

# --- CONFIGURATION ---
DATABASE_DIR = "database"
EMBEDDINGS_PATH = os.path.join(DATABASE_DIR, "embeddings.npy")
LABELS_PATH = os.path.join(DATABASE_DIR, "labels.json")

# Artwork crop coordinates from full screenshot (x, y, w, h)
CARD_REGIONS = [
    (34, 429, 127, 131),   # Card 1
    (214, 438, 120, 118),  # Card 2
    (381, 423, 131, 138),  # Card 3
    (552, 422, 135, 134),  # Card 4
    (33, 716, 124, 142),   # Card 5
    (212, 717, 121, 115),  # Card 6
    (387, 713, 111, 117),  # Card 7
    (563, 714, 117, 113),  # Card 8
]

# --- LOAD MODELS & DATABASE ---
print("Loading database...")
try:
    embeddings = np.load(EMBEDDINGS_PATH).astype("float32")
    with open(LABELS_PATH) as f:
        labels = json.load(f)
    faiss_index = faiss.IndexFlatIP(embeddings.shape[1])
    faiss_index.add(embeddings)
    print(f"Loaded {len(labels)} cards from database.")
except Exception as e:
    print(f"Error loading database: {e}")
    embeddings = None
    labels = None
    faiss_index = None

print("Loading CLIP model...")
device = "cuda" if torch.cuda.is_available() else "cpu"
model, _, preprocess = open_clip.create_model_and_transforms(
    "ViT-B-32",
    pretrained="laion2b_s34b_b79k"
)
model = model.to(device)
model.eval()
print(f"Model loaded on {device}.")

# --- HELPER FUNCTIONS ---
def get_embedding(pil_image):
    image = preprocess(pil_image.convert("RGB")).unsqueeze(0).to(device)
    with torch.no_grad():
        feature = model.encode_image(image)
        feature /= feature.norm(dim=-1, keepdim=True)
    return feature.cpu().numpy().astype("float32")

# --- ROUTES ---
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    
    if faiss_index is None:
         return jsonify({"error": "Database not loaded"}), 500

    try:
        # Read image using OpenCV
        in_memory_file = io.BytesIO(file.read())
        file_bytes = np.frombuffer(in_memory_file.read(), np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        
        if img is None:
            return jsonify({"error": "Invalid image format"}), 400
            
        results = []
        for i, (x, y, w, h) in enumerate(CARD_REGIONS):
            # Crop image
            crop = img[y:y+h, x:x+w]
            
            # Convert OpenCV (BGR) to PIL (RGB)
            crop_rgb = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(crop_rgb)
            
            # Get embedding
            query = get_embedding(pil_image)
            
            # Search
            k = 5 # Return top 5 matches
            scores, ids = faiss_index.search(query, k)
            
            top_matches = []
            for j in range(k):
                top_matches.append({
                    "label": labels[ids[0][j]],
                    "score": float(scores[0][j])
                })
            
            best_match_label = labels[ids[0][0]]
            best_match_score = scores[0][0]
            
            results.append({
                "region": i + 1,
                "label": best_match_label,
                "score": float(best_match_score),
                "matches": top_matches
            })

        return jsonify({"results": results})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/generate_story", methods=["POST"])
def generate_story():
    data = request.json
    if not data or "deck" not in data:
        return jsonify({"error": "No deck provided"}), 400
        
    deck = data["deck"]
    if not isinstance(deck, list):
        return jsonify({"error": "Deck must be a list of card names"}), 400
        
    try:
        engine = StoryEngine()
        
        def generate():
            for chunk in engine.generate_story(deck):
                yield chunk
                
        return Response(stream_with_context(generate()), mimetype='text/plain')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
