import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="WorthIt", page_icon="🔍")

# 1. Configuración de API
api_key = st.secrets["GOOGLE_API_KEY"].strip()
genai.configure(api_key=api_key)

st.title("🔍 WorthIt")

# 2. AUTODETECCIÓN DE MODELO
def obtener_modelo_valido():
    # Listamos todos los modelos disponibles para tu llave
    models = genai.list_models()
    for m in models:
        # Buscamos modelos que soporten generación de contenido con imágenes
        if 'generateContent' in m.supported_generation_methods and 'vision' in m.name or '1.5' in m.name:
            return genai.GenerativeModel(m.name)
    return None

img_file = st.file_uploader("📸 HAZ LA FOTO", type=['jpg', 'jpeg', 'png'])

if img_file:
    img = Image.open(img_file)
    st.image(img, use_container_width=True)
    
    if st.button("💰 ¿CUÁNTO VALE?"):
        with st.spinner("Buscando modelo compatible..."):
            model = obtener_modelo_valido()
            
            if model:
                try:
                    response = model.generate_content([
                        "Identifica el objeto, da su valor de segunda mano y curiosidad. Sé breve.",
                        img
                    ])
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error en la llamada: {e}")
            else:
                st.error("No se encontró ningún modelo compatible con tu llave.")
                st.info("Revisa si tu cuenta de Google AI Studio tiene límites activados.")
