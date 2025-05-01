import streamlit as st
from PIL import Image, UnidentifiedImageError
import google.generativeai as genai
from dotenv import load_dotenv
import os
import io

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Configure Gemini API
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash")

# Supported formats
SUPPORTED_FORMATS = ["jpg", "jpeg", "png", "bmp", "tiff", "gif"]

# Streamlit page config
st.set_page_config(
    page_title="🌱 Plant Disease Detector",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Sidebar with instructions
with st.sidebar:
    st.header("How to Use")
    st.markdown("""
    1. **Upload** a clear image of a plant leaf (formats: JPG, PNG, BMP, TIFF, GIF).
    2. **Click 'Analyze'** to detect diseases and get suggestions.
    3. **Download** the diagnosis report if needed.
    """)
    st.markdown("---")
    st.info("For best results, use clear, close-up images of single leaves.")

st.title("🌱 Plant Disease Detector")
st.write("Upload a plant leaf image. The AI will detect possible diseases and suggest remedies.")

# File uploader
uploaded_file = st.file_uploader(
    "Choose an image file (JPG, PNG, BMP, TIFF, GIF)", 
    type=SUPPORTED_FORMATS,
    accept_multiple_files=False
)

def preprocess_image(image):
    # Convert to RGB and resize if too large
    image = image.convert("RGB")
    max_size = (1024, 1024)
    if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
        image.thumbnail(max_size)
    return image

def generate_report(text):
    return io.BytesIO(text.encode("utf-8"))

if uploaded_file:
    try:
        image = Image.open(uploaded_file)
        image = preprocess_image(image)
        st.image(image, caption="Uploaded Leaf Image", use_column_width=True)
        st.info("Click 'Analyze' to detect diseases and get suggestions.")

        if st.button("🔎 Analyze"):
            with st.spinner("Analyzing the image... Please wait."):
                prompt = (
                    "You are a plant pathology expert. Analyze the uploaded leaf image for any signs of disease. "
                    "If a disease is detected, specify its name, describe the symptoms, and provide actionable suggestions for treatment and prevention. "
                    "If the leaf appears healthy, state that as well."
                )
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format='PNG')
                img_bytes = img_byte_arr.getvalue()

                try:
                    # Show progress bar
                    progress = st.progress(0)
                    response = model.generate_content(
                        [prompt, genai.types.Blob(content=img_bytes, mime_type="image/png")]
                    )
                    progress.progress(100)
                    st.success("Analysis Complete!")
                    st.markdown(f"**Diagnosis & Suggestions:**\n\n{response.text}")

                    # Downloadable report
                    report_bytes = generate_report(response.text)
                    st.download_button(
                        label="💾 Download Diagnosis Report",
                        data=report_bytes,
                        file_name="plant_disease_report.txt",
                        mime="text/plain"
                    )
                except Exception as e:
                    st.error(f"Error analyzing image: {e}")

        st.button("🔄 Reset", on_click=lambda: st.experimental_rerun())
    except UnidentifiedImageError:
        st.error("The uploaded file is not a valid image or is corrupted. Please upload a supported image file.")
    except Exception as e:
        st.error(f"Unexpected error: {e}")
else:
    st.info("Please upload a clear image of a plant leaf to begin.")

st.markdown("---")
st.caption("Built with Gardeners & Plant growers")
