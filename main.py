import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="WorthIt", layout="centered")

st.title("🔍 WorthIt")

# Barra lateral
api_key = st.sidebar.text_input("API Key de Google", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # Cambiamos a 'gemini-pro-vision' o 'gemini-1.5-flash-latest' que son más estables
        model = genai.GenerativeModel('gemini-1.5-flash-latest')

        # Usamos el cargador de archivos estándar de Streamlit además de la cámara
        # Esto es un truco para iPad: si la cámara falla, puedes subir la foto del carrete
        opcion = st.radio("Selecciona fuente:", ("Cámara", "Subir foto del carrete"))
        
        img_file = None
        if opcion == "Cámara":
            img_file = st.camera_input("Haz la foto")
        else:
            img_file = st.file_uploader("Elige una foto", type=['jpg', 'png', 'jpeg'])

        if img_file:
            img = Image.open(img_file)
            st.image(img, use_container_width=True)
            
            prompt = "Actúa como un experto en tasación. Identifica este objeto. Dime su nombre, precio aproximado de mercado de segunda mano y un dato curioso. Sé breve y directo."
            
            with st.spinner("Analizando con IA..."):
                response = model.generate_content([prompt, img])
                st.success("¡Análisis completado!")
                st.write(response.text)
                
    except Exception as e:
        st.error(f"Error técnico: {e}")
else:
    st.info("👈 Introduce tu API Key en la barra lateral para empezar.")
