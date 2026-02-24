import streamlit as st
import os
import time
from PIL import Image

# --- CONFIGURATION ---
DATA_DIR = "smartphone_dataset"
os.makedirs(DATA_DIR, exist_ok=True)

# Page Branding
st.set_page_config(page_title="Smartphone Dataset Lab", page_icon="📱")

st.title("📱 Smartphone Dataset Lab")
st.markdown("Upload photos to build your **2020-2024** model detection dataset.")

# --- HELPER FUNCTIONS ---
def get_brand(name):
    name = name.lower()
    if "iphone" in name or "apple" in name: return "Apple"
    if "samsung" in name or "galaxy" in name: return "Samsung"
    if "pixel" in name or "google" in name: return "Google"
    if "xiaomi" in name: return "Xiaomi"
    if "oneplus" in name: return "OnePlus"
    return "Other"

# --- INTERFACE ---
existing_models = [d for d in os.listdir(DATA_DIR) if os.path.isdir(os.path.join(DATA_DIR, d))]
existing_models.sort()

with st.expander("📂 View Current Dataset Stats"):
    if not existing_models:
        st.write("Dataset is currently empty.")
    for model in existing_models:
        count = len([f for f in os.listdir(os.path.join(DATA_DIR, model)) if f.endswith('.jpg')])
        st.write(f"- **{model}**: {count} images")

st.divider()

# Model Selection
col1, col2 = st.columns(2)
with col1:
    mode = st.radio("Action:", ["Add to Existing Model", "Create New Model Entry"])

with col2:
    if mode == "Add to Existing Model":
        final_model_name = st.selectbox("Select Model:", existing_models) if existing_models else None
        if not existing_models: st.warning("No models found. Create one first!")
    else:
        new_name = st.text_input("Enter Model Name (e.g., iPhone 15 Pro):")
        final_model_name = new_name.strip().replace(" ", "_") if new_name else None

# Image Upload
if final_model_name:
    brand = get_brand(final_model_name)
    st.info(f"Labeling for: **{brand} {final_model_name}**")
    
    uploaded_file = st.file_uploader("Upload Smartphone Image", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, use_container_width=True, caption="Preview")
        
        if st.button("🚀 Save to Dataset", use_container_width=True):
            # Path Logic
            save_path = os.path.join(DATA_DIR, final_model_name)
            os.makedirs(save_path, exist_ok=True)
            
            # Save Image
            timestamp = int(time.time())
            filename = f"{final_model_name}_{timestamp}.jpg"
            img.convert("RGB").save(os.path.join(save_path, filename))
            
            # Save Metadata
            with open(os.path.join(save_path, f"{final_model_name}_{timestamp}.txt"), "w") as f:
                f.write(f"brand: {brand}\nmodel: {final_model_name}\ndate: 2020-2024")
                
            st.success(f"Successfully saved to {final_model_name} folder!")
            st.balloons()