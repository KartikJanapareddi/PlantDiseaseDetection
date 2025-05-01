import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image
import io

# Load API key from .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file.")

# Configure Gemini with your API key
genai.configure(api_key=api_key)

# Initialize Gemini Flash 2.0
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

def analyze_plant_disease(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))

    response = model.generate_content(
        [
            "You are a plant pathologist. Carefully analyze this image of a leaf. "
            "Identify any diseases or symptoms the plant might be suffering from, and provide bullet-point remedies. "
            "Avoid mentioning AI, Gemini, or that this is a generated response.",
            image
        ],
        stream=False  # Set to True if streaming responses
    )

    return response.text.strip()
