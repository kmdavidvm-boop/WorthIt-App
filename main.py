import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="WorthIt Gratis", layout="centered")
st.title("🔍 WorthIt")

api_key = st.sidebar.text_input("Pega tu API Key de Google", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # Este bloque busca qué modelo tienes activo para no dar error 404
        modelos_disponibles = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # Priorizamos el flash que es el más rápido
        modelo_nombre = 'models/gemini-1.5-flash' if 'models/gemini-1.5-flash' in modelos_disponibles else modelos_disponibles[0]
        
        model = genai.GenerativeModel(modelo_nombre)
        st.sidebar.success(f"Conectado a: {modelo_nombre}")

        opcion = st.radio("Capturar:", ("Cámara", "Galería"))
        img_file = st.camera_input("Foto") if opcion == "Cámara" else st.file_uploader("Imagen", type=['jpg', 'png'])

        if img_file:
            img = Image.open(img_file)
            st.image(img, use_container_width=True)
            prompt = "Dime qué es este objeto, su valor aproximado en el mercado de segunda mano y un dato curioso. Sé breve."
            
            with st.spinner("Analizando gratis..."):
                response = model.generate_content([prompt, img])
                st.subheader("Resultado:")
                st.write(response.text)
                
    except Exception as e:
        st.error(f"Error: {e}")
        st.info("Asegúrate de que la API Key es la correcta.")
else:
    st.info("Copia la API Key de Google AI Studio y pégala a la izquierda.")
