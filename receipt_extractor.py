import os
import json
import httpx
import base64
from PIL import Image
import pandas as pd

# === CONFIGURATION ===
image_folder = "pics"
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)

# === FUNCTION TO ENCODE IMAGE ===
def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# === FUNCTION TO QUERY LLAVA VIA HTTP API ===
def query_llava(image_path):
    image_base64 = encode_image(image_path)
    payload = {
        "model": "llava",
        "prompt": "Extract all receipt details in text format.",
        "images": [image_base64],
        "stream": False
    }
    try:
        # Use longer timeout for slow generation
        response = httpx.post("http://localhost:11434/api/generate", json=payload, timeout=120.0)
        response.raise_for_status()
        result = response.json()
        return result.get("response", "").strip()
    except Exception as e:
        print(f"❌ Error querying Ollama: {e}")
        return ""

# === FUNCTION TO SAVE RAW TEXT TO FILE ===
def save_response(text, filename):
    with open(filename, "w") as f:
        f.write(text)

# === PROCESS ALL IMAGES ===
image_extensions = [".jpg", ".jpeg", ".png"]
image_files = [f for f in os.listdir(image_folder) if os.path.splitext(f)[1].lower() in image_extensions]

for image_file in image_files:
    image_path = os.path.join(image_folder, image_file)
    print(f"\n🖼️ Processing: {image_file}")
    result = query_llava(image_path)

    if result:
        text_path = os.path.join(output_folder, f"{os.path.splitext(image_file)[0]}_raw.txt")
        save_response(result, text_path)
        print(f"✅ Saved response to: {text_path}")
    else:
        print("⚠️ Failed to extract data.")
