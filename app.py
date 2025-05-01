import streamlit as st
from PIL import Image
from gemini_api import analyze_plant_disease

# Configure Streamlit page
st.set_page_config(
    page_title="🌿 Plant Disease Detector",
    page_icon="🍃",
    layout="centered"
)

# Custom UI styles
st.markdown("""
    <style>
        .main {
            background-color: #e8f5e9;
        }
        img {
            border: 3px solid #4caf50;
            border-radius: 12px;
            margin-top: 1rem;
            max-height: 400px;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-size: 16px;
            border-radius: 10px;
            padding: 0.5em 1.5em;
        }
    </style>
""", unsafe_allow_html=True)

# App Header
st.title("🍃 Plant Disease Detector")
st.subheader("Upload a leaf image to detect disease and get treatment advice")

# Upload file section
uploaded_file = st.file_uploader("📤 Upload Leaf Image (JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file)
        st.image(image, caption="📷 Uploaded Leaf", use_column_width=True)

        if st.button("🔍 Diagnose Now"):
            with st.spinner("Analyzing leaf image... 🌿"):
                image_bytes = uploaded_file.getvalue()
                result = analyze_plant_disease(image_bytes)

                st.success("✅ Diagnosis Complete!")
                st.markdown("### 🩺 **Diagnosis & Remedies**")
                st.markdown(result)

    except Exception as e:
        st.error("⚠️ Error processing image. Make sure it's a valid image file.")
        st.exception(e)
else:
    st.warning("📸 Please upload a clear leaf image to begin diagnosis.")

# Footer
st.markdown("---")
st.markdown("<center><small>🌱 Built with love for growers and green thumbs</small></center>", unsafe_allow_html=True)
