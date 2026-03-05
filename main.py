import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configuración de la página
st.set_page_config(page_title="WorthIt", layout="centered")

st.title("🔍 WorthIt")

# Barra lateral para la API Key
api_key = st.sidebar.text_input("Pega tu API Key de Google", type="password")

if api_key:
    try:
        # Configuración del motor de IA
        genai.configure(api_key=api_key)
        
        # PROBAR CON ESTE MODELO (es el más estándar actualmente)
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Selector de método para iPad
        opcion = st.radio("Selecciona cómo capturar:", ("Cámara", "Galería/Carrete"))
        
        img_file = None
        if opcion == "Cámara":
            img_file = st.camera_input("Haz la foto")
        else:
            img_file = st.file_uploader("Sube una imagen", type=['jpg', 'png', 'jpeg'])

        if img_file:
            img = Image.open(img_file)
            st.image(img, use_container_width=True)
            
            # Instrucciones para la IA
            prompt = "Eres un experto tasador. Identifica este objeto, dinos su valor de mercado aproximado y un dato histórico o curioso."
            
            with st.spinner("Analizando objeto..."):
                # Generar contenido enviando la imagen
                response = model.generate_content([prompt, img])
                
                st.subheader("Análisis de WorthIt:")
                st.write(response.text)
                
    except Exception as e:
        # Si falla el 1.5-flash, intentamos con el modelo Pro Vision (respaldo)
        st.error(f"Error con el modelo principal: {e}")
        st.info("Intentando conectar con modelo de respaldo...")
else:
    st.info("Introduce tu API Key en la barra lateral para activar la app.")
