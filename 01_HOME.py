import streamlit as st
import base64
from pathlib import Path

st.set_page_config(page_title="Home", page_icon="🏠", layout="wide")

BASE_DIR = Path(__file__).resolve().parent
IMAGE_PATH = BASE_DIR / "media" / "back.jpg"

with open(IMAGE_PATH, "rb") as f:
    data = f.read()
    encoded = base64.b64encode(data).decode()

# CSS avec "dézoom"
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: 100%; 
        background-position: center 5%;
    }}
    .content {{
        position: fixed;
        top: 50%;
        left: 80%;
        transform: translate(-50%, -50%);
        text-align: center;
        color: white;
        z-index: 1;
    }}
    </style>

    <div class="content">
       <h1 style="text-align:center;color:white;background-color:rgba(255,255,255,0.2);padding:10px 20px;border-radius:5px;display:inline-block;"><b>Bienvenue sur le Dashboard</b></h1>
       <h5><b>Analysez, comprenez et exploitez vos données comme jamais !</b></h5>
    </div>
    """,
    unsafe_allow_html=True
)
