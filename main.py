import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

st.set_page_config(page_title="WorthIt", page_icon="🔍")

# Configuración de seguridad para evitar bloqueos en Europa
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # Forzamos la versión 1.5-flash que es la más estable
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        safety_settings=safety_settings
    )
except:
    st.error("Error en la configuración de la API Key.")

st.title("🔍 WorthIt")

img_file = st.file_uploader("📸 TOCA AQUÍ PARA EMPEZAR", type=['jpg', 'png', 'jpeg'])

if img_file:
    img = Image.open(img_file)
    # Miniatura muy pequeña para que no haya lag
    img.thumbnail((400, 400))
    st.image(img, caption="Imagen lista")
    
    if st.button("💰 ¿CUÁNTO VALE?"):
        with st.spinner("Conectando con el servidor..."):
            try:
                # Prompt directo y sencillo
                prompt = "Identifica el objeto de la imagen. Dime su nombre y su precio estimado en euros en el mercado de segunda mano. Sé breve."
                
                # Ejecutar con timeout implícito
                response = model.generate_content([prompt, img])
                
                if response:
                    st.subheader("Resultado:")
                    st.write(response.text)
                else:
                    st.error("No hay respuesta del servidor.")
            except Exception as e:
                # ESTO ES LO MÁS IMPORTANTE: Si falla, nos dirá el CÓDIGO de error
                st.error(f"Error detectado: {e}")
                if "finish_reason" in str(e):
                    st.warning("La IA bloqueó la imagen por seguridad. Intenta con otra foto.")
