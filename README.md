# Clash Chronicles ⚔️📜

![Clash Chronicles Banner](https://img.shields.io/badge/Status-Hackathon_Ready-success?style=for-the-badge)
![Python Version](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge)
![PyTorch](https://img.shields.io/badge/PyTorch-AI_Vision-ee4c2c?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge)

**Bring Your Deck to Life.** 

Clash Chronicles uses advanced computer vision and PyTorch AI to scan any Clash Royale screenshot, instantly identify your exact battle deck, and use Generative AI to stream a unique, thrilling 3-act cinematic story based on your squad's exact characters and personalities.

## 🌟 The Problem
Every Clash Royale player has a favorite deck, but have you ever wondered how those specific characters interact outside the arena? 
* **No Personalized Lore:** Millions of players love Clash Royale, but there is no lore for their specific team combinations.
* **Static Characters:** You play the same 8 cards for years, but never see how they interact outside of gameplay.

## 🚀 Our Solution
Clash Chronicles brings your team to life by giving them their own official cinematic lore. Users simply upload a screenshot of their Clash Royale game or deck. The app analyzes the image, identifies your exact 8 cards, and streams a highly creative, 3-Act story in real-time, highlighting the unique personalities, strengths, and relationships of your troops.

---

## 🛠️ How It Works (The Pipeline)

1. **Upload & Crop:** OpenCV processes the uploaded gameplay image and extracts the individual cards.
2. **Vision Model:** PyTorch and CLIP (`open_clip_torch`) generate high-dimensional image embeddings of the cropped cards.
3. **Vector Database:** `faiss-cpu` instantly matches the embeddings against our local vector database of 180+ Clash Royale cards to achieve zero-shot classification.
4. **Story Engine:** The extracted team roster is fed into a large language model via the Fireworks AI API.
5. **Real-time Streaming:** The LLM streams back a 3-act story in real-time to the browser via Server-Sent Events (SSE).

## 💻 Tech Stack

* **Frontend:** Vanilla HTML, CSS, & JavaScript, featuring a custom glassmorphism medieval design system, CSS animations, and `ReadableStream` API.
* **Backend:** Python Flask & Werkzeug (served with Gunicorn in production).
* **Computer Vision:** OpenCV (`opencv-python-headless`) and Pillow.
* **Image Recognition AI:** PyTorch & `open_clip_torch`.
* **Vector Database:** `faiss-cpu`.
* **Generative Text AI:** LLMs accessed via Fireworks AI API.

---

## ⚙️ Setup & Installation

You can run this project locally in two ways: using **Docker** (recommended) or a standard Python environment.

### 1. Clone the repository
```bash
git clone https://github.com/aryan-v-aid/Clash-Chronicles.git
cd Clash-Chronicles
```

### 2. Setup API Keys
You need API keys to generate the stories and download the CLIP model without rate limits.
1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and add your keys:
   ```env
   FIREWORKS_API_KEY=your_fireworks_api_key_here
   HF_TOKEN=your_huggingface_token_here
   ```

---

### Method A: Run with Docker (Recommended 🐳)
Docker is the easiest way to run the app because it handles the complex PyTorch and OpenCV system requirements automatically.

1. **Build the container:**
   ```bash
   docker build -t clash-chronicles .
   ```
2. **Run the container:**
   *(We pass the `.env` file securely at runtime)*
   ```bash
   docker run -p 5000:5000 --env-file .env clash-chronicles
   ```
3. Open your browser and navigate to `http://localhost:5000`.

---

### Method B: Run with Python (Local Virtual Environment)
If you prefer running it locally on your machine without Docker.

1. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Start the application:**
   You can run our convenient auto-start script which launches the server and opens your web browser instantly:
   ```bash
   python start_server.py
   ```

---

## 🔮 What's Next?
* **Voice Generation:** Using AI text-to-speech to narrate the stories.
* **Image Generation:** Creating custom comic-book style illustrations for each Act.
* **Player Stats Integration:** Connecting to the official Supercell API to reference your actual win rates and trophy counts in the lore!

---
*Disclaimer: This is an unofficial fan project and is not affiliated with, endorsed, sponsored, or specifically approved by Supercell.*
