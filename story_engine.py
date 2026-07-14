import os
import json
from openai import OpenAI

from dotenv import load_dotenv
load_dotenv()

class StoryEngine:
    def __init__(self):
        # Configure Fireworks API key
        api_key = os.environ.get("FIREWORKS_API_KEY")
        if not api_key:
            raise ValueError("FIREWORKS_API_KEY environment variable is missing. Please set it in your .env file.")
        
        self.client = OpenAI(
            base_url="https://api.fireworks.ai/inference/v1",
            api_key=api_key
        )
        self.model = "accounts/fireworks/models/deepseek-v4-pro"
        
        # Path to the knowledge folder
        self.knowledge_dir = os.path.join(os.path.dirname(__file__), "knowledge")
        self.prompt_template_path = os.path.join(os.path.dirname(__file__), "prompt_template.txt")
        
        # Build file mapping
        self.file_map = {}
        if os.path.exists(self.knowledge_dir):
            for root, _, files in os.walk(self.knowledge_dir):
                for f in files:
                    if f.endswith('.json') or f.endswith('.md'):
                        # Normalize filename by stripping spaces, hyphens and underscores
                        basename = os.path.splitext(f)[0]
                        norm_name = basename.lower().replace("_", "").replace("-", "").replace(" ", "")
                        self.file_map[norm_name] = os.path.join(root, f)

    def _normalize_label(self, label: str) -> str:
        """Converts detector label to normalized key (e.g. pekkaevo)"""
        norm = label.lower()
        if norm.endswith("-ev1") or norm.endswith("evolved"):
            norm = norm.replace("-ev1", "evo").replace("-evolved", "evo").replace("evolved", "evo")
        return norm.replace("-", "").replace("_", "").replace(" ", "")

    def build_context(self, deck: list) -> str:
        """Reads JSON files for the detected deck and builds a context string."""
        context_parts = []
        
        for card_label in deck:
            norm_label = self._normalize_label(card_label)
            file_path = self.file_map.get(norm_label)
            
            if file_path and os.path.exists(file_path):
                try:
                    card_context = f"--- {card_label.replace('-', ' ').title()} ---\n"
                    
                    if file_path.endswith('.json'):
                        with open(file_path, "r", encoding="utf-8") as f:
                            data = json.load(f)
                            
                        # Build a structured string for this card
                        for key, value in data.items():
                            if isinstance(value, list):
                                value_str = ", ".join(value)
                            elif isinstance(value, dict):
                                # Handle evolution dictionary
                                value_str = ", ".join(f"{k}: {v}" for k, v in value.items())
                            else:
                                value_str = str(value)
                                
                            card_context += f"{key.replace('_', ' ').capitalize()}: {value_str}\n"
                            
                    elif file_path.endswith('.md'):
                        with open(file_path, "r", encoding="utf-8") as f:
                            card_context += f.read() + "\n"
                            
                    context_parts.append(card_context)
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
            else:
                print(f"No details found for {card_label} (normalized: {norm_label})")
                
        return "\n\n".join(context_parts)

    def generate_story(self, deck: list):
        """Builds context, loads prompt template, and yields a story stream using Fireworks."""
        context = self.build_context(deck)
        
        if not context.strip():
            yield "Could not generate story because no card context was found for the detected cards."
            return
            
        try:
            with open(self.prompt_template_path, "r", encoding="utf-8") as f:
                prompt = f.read()
        except FileNotFoundError:
            yield "Error: prompt_template.txt not found."
            return
            
        prompt = prompt.replace("{context}", context)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a creative storyteller."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                stream=True
            )
            for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            yield f"Error generating story with Fireworks API: {str(e)}"
