from sentence_transformers import SentenceTransformer
import streamlit as st
import os

MODEL_PATH = "models/bge-small-en-v1.5"

@st.cache_resource
def load_embedding_model():

    if os.path.exists(MODEL_PATH):
        print("✅ Loading local embedding model...")
        return SentenceTransformer(MODEL_PATH)

    print("🌐 Local model not found. Downloading once...")

    # Create models directory if it doesn't exist
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

    model = SentenceTransformer("BAAI/bge-small-en-v1.5")
    model.save(MODEL_PATH)

    return model