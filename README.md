# Clash Chronicles ⚔️📜

![Clash Chronicles Banner](https://img.shields.io/badge/Status-Hackathon_Ready-success?style=for-the-badge)
![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge)
![PyTorch](https://img.shields.io/badge/PyTorch-AI_Vision-ee4c2c?style=for-the-badge)

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
4. **Story Engine:** The extracted team roster is fed into Deepseek V4 Pro via the Fireworks AI API.
5. **Real-time Streaming:** The LLM streams back a 3-act story in real-time to the browser via Server-Sent Events (SSE).

## 💻 Tech Stack

* **Frontend:** Vanilla HTML, CSS, & JavaScript, featuring a custom glassmorphism medieval design system, CSS animations, and `ReadableStream` API.
* **Backend:** Python Flask & Werkzeug.
* **Computer Vision:** OpenCV (`opencv-python-headless`) and Pillow.
* **Image Recognition AI:** PyTorch & `open_clip_torch`.
* **Vector Database:** `faiss-cpu`.
* **Generative Text AI:** Deepseek V4 Pro via Fireworks AI API.

---

## ⚙️ Local Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/aryan-v-aid/Clash-Chronicles.git
cd Clash-Chronicles
```

### 2. Install Dependencies
It is highly recommended to use a virtual environment (`venv`).
```bash
pip install -r requirements.txt
```

### 3. Setup API Keys
Create a `.env` file in the root directory (you can copy `.env.example`):
```bash
cp .env.example .env
```
Open `.env` and add your Fireworks AI API key:
```env
FIREWORKS_API_KEY=your_actual_key_here
```

### 4. Run the Application
Start the Flask development server:
```bash
flask run
```
Then, open your browser and navigate to `http://localhost:5000`.

---

## 🔮 What's Next?
* **Voice Generation:** Using AI text-to-speech to narrate the stories.
* **Image Generation:** Creating custom comic-book style illustrations for each Act.
* **Player Stats Integration:** Connecting to the official Supercell API to reference your actual win rates and trophy counts in the lore!

---
*Disclaimer: This is an unofficial fan project and is not affiliated with, endorsed, sponsored, or specifically approved by Supercell.*
