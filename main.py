import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="WorthIt", page_icon="🔍")

# 1. Configuración de la API
try:
    api_key = st.secrets["GOOGLE_API_KEY"].strip()
    genai.configure(api_key=api_key)
    
    # CAMBIO CRÍTICO: Usamos el nombre que Google sugiere para evitar el 404
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception as e:
    st.error(f"Error de configuración: {e}")

st.title("🔍 WorthIt")

# 2. Selector de imagen
img_file = st.file_uploader("📸 HAZ LA FOTO", type=['jpg', 'jpeg', 'png'])

if img_file:
    img = Image.open(img_file)
    st.image(img, use_container_width=True)
    
    if st.button("💰 ¿CUÁNTO VALE?"):
        with st.spinner("Analizando..."):
            try:
                # Simplificamos el envío al máximo
                response = model.generate_content([
                    "Dime qué es este objeto y su precio aproximado de segunda mano en euros. Sé breve.",
                    img
                ])
                
                if response:
                    st.success("¡Tasación lista!")
                    st.write(response.text)
            except Exception as e:
                # Si esto vuelve a dar 404, probamos el modelo pro
                try:
                    model_pro = genai.GenerativeModel('gemini-pro-vision')
                    response = model_pro.generate_content(["¿Qué es esto y precio?", img])
                    st.write(response.text)
                except Exception as e2:
                    st.error(f"Error persistente: {e2}")
                    st.info("Intenta crear una API Key nueva eligiendo 'Gemini 1.5 Flash' específicamente en AI Studio.")
