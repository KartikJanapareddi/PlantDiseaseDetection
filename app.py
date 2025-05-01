import streamlit as st
import os
from dotenv import load_dotenv
from PIL import Image
import google.generativeai as genai

# Load API key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

# Initialize model
model = genai.GenerativeModel("gemini-2.0-flash")

# Streamlit UI
st.set_page_config(page_title="🌿 Plant Disease Detector", layout="centered")

st.markdown("""
    <h1 style='color:#2E8B57; text-align:center;'>🌿 Plant Disease Detector</h1>
    <p style='text-align:center;'>Upload a leaf image to identify the disease and get remedies</p>
    """, unsafe_allow_html=True)

uploaded_image = st.file_uploader("Upload Leaf Image", type=["jpg", "jpeg", "png"])

if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Leaf", use_column_width=True)

    with st.spinner("Analyzing the leaf..."):
        prompt = """You are a plant pathologist. Analyze the uploaded leaf image.
        Predict the plant disease (if any) and suggest effective remedies to treat or manage it.
        Return the result in the format:
        Disease: <disease_name>
        Remedies: <bulleted list of remedies>"""

        response = model.generate_content([prompt, image])
        output = response.text

    st.markdown("### 🩺 Diagnosis Result")
    st.markdown(output)
