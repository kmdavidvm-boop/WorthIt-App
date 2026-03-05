import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="WorthIt", page_icon="🔍")

# Intentamos conectar de forma robusta
try:
    key = st.secrets["GOOGLE_API_KEY"].strip()
    genai.configure(api_key=key)
    
    # Probamos con el nombre técnico exacto que Google pide ahora
    model = genai.GenerativeModel('models/gemini-1.5-flash')
except Exception as e:
    st.error("Error de configuración inicial.")

st.title("🔍 WorthIt")

# Subida nativa de Apple
img_file = st.file_uploader("📸 TOCA PARA HACER FOTO O SUBIR", type=['jpg', 'jpeg', 'png'])

if img_file:
    img = Image.open(img_file)
    st.image(img, use_container_width=True)
    
    if st.button("💰 ¿CUÁNTO VALE?"):
        with st.spinner("Analizando..."):
            try:
                # El comando
                response = model.generate_content([
                    "Identifica este objeto y dime su precio de segunda mano en España. Sé muy breve.", 
                    img
                ])
                
                if response:
                    st.success("¡Tasación lista!")
                    st.write(response.text)
            except Exception as e:
                # Si esto da 404, probamos el modelo alternativo automáticamente
                try:
                    alt_model = genai.GenerativeModel('gemini-1.5-flash-latest')
                    response = alt_model.generate_content(["¿Qué es esto y precio?", img])
                    st.write(response.text)
                except:
                    st.error(f"Error técnico de Google: {e}")
                    st.info("Si el error persiste, comprueba que has aceptado los términos en Google AI Studio.")

st.caption("Si sale error 404, prueba a refrescar el navegador del iPad una vez.")
