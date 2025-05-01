import streamlit as st
from PIL import Image, UnidentifiedImageError
import mimetypes
import io
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load Gemini API key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash")

# Supported MIME types for Gemini 2.0 Flash
GEMINI_MIME_TYPES = {
    # Images
    "image/png", "image/jpeg", "image/webp",
    # Audio
    "audio/flac", "audio/mp3", "audio/m4a", "audio/mpeg",
    # Video
    "video/x-flv", "video/quicktime", "video/mpeg", "video/mpegps", "video/mpg",
    "video/mp4", "video/webm", "video/wmv", "video/3gpp",
    # Documents
    "application/pdf", "text/plain"
}

def get_mime_type(file):
    mime_type, _ = mimetypes.guess_type(file.name)
    # Fallback for some audio types
    if not mime_type and file.name.lower().endswith(".m4a"):
        mime_type = "audio/m4a"
    return mime_type

def file_to_blob(file, mime_type):
    # For images, ensure correct format
    if mime_type and mime_type.startswith("image/"):
        try:
            image = Image.open(file)
            buf = io.BytesIO()
            image.save(buf, format="PNG")
            return genai.types.Blob(content=buf.getvalue(), mime_type="image/png")
        except UnidentifiedImageError:
            return None
    else:
        # For other types, just use raw bytes
        return genai.types.Blob(content=file.read(), mime_type=mime_type)

st.set_page_config(
    page_title="🌐 Gemini Universal File Analyzer",
    page_icon="✨",
    layout="centered"
)

st.title("🌐 Gemini Universal File Analyzer")
st.write("Upload any file supported by Gemini 2.0 Flash (images, audio, video, PDF, text) for intelligent analysis and suggestions.")

uploaded_file = st.file_uploader(
    "Upload a file (image, audio, video, PDF, or text)", 
    type=None,  # Accept any file type
    accept_multiple_files=False
)

if uploaded_file:
    mime_type = get_mime_type(uploaded_file)
    st.write(f"**Detected file type:** `{mime_type or 'Unknown'}`")

    if mime_type not in GEMINI_MIME_TYPES:
        st.error("This file type is not supported by Gemini 2.0 Flash. Please upload an image (PNG/JPEG/WebP), audio (FLAC/MP3/MPA/MPEG), video (FLV/MOV/MPEG/MP4/WEBM/WMV/3GPP), PDF, or plain text file.")
    else:
        blob = file_to_blob(uploaded_file, mime_type)
        if blob is None:
            st.error("Could not process the uploaded file. Please ensure it is valid and try again.")
        else:
            prompt = (
                "You are an expert assistant. Analyze the uploaded file and provide a detailed summary, "
                "identify any relevant information, and give actionable suggestions if applicable. "
                "If the file is an image of a plant leaf, diagnose possible diseases and suggest remedies. "
                "If it's a document, summarize its contents. For audio/video, describe the content."
            )
            if st.button("🔎 Analyze"):
                with st.spinner("Analyzing the file..."):
                    try:
                        response = model.generate_content([prompt, blob])
                        st.success("Analysis Complete!")
                        st.markdown(f"**Result:**\n\n{response.text}")
                    except Exception as e:
                        st.error(f"Error analyzing file: {e}")
else:
    st.info("Please upload a file to begin.")

st.markdown("---")
st.caption("Powered by Gemini 2.0 Flash | Built with Streamlit")
