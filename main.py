import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configuración con icono de lupa
st.set_page_config(
    page_title="WorthIt", 
    page_icon="🔍", 
    layout="centered"
)

# Estética de la App
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    stButton>button {
        width: 100%;
        border-radius: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# El resto del código que ya tienes...

# Configuramos la llave desde los Secretos de Streamlit
api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="WorthIt App", layout="centered")
st.title("🔍 WorthIt")

opcion = st.radio("Capturar:", ("Cámara", "Galería"))
img_file = st.camera_input("Foto") if opcion == "Cámara" else st.file_uploader("Imagen", type=['jpg', 'png'])

if img_file:
    img = Image.open(img_file)
    st.image(img, use_container_width=True)
    with st.spinner("Analizando..."):
        response = model.generate_content(["Identifica este objeto y di su precio.", img])
        st.write(response.text)
