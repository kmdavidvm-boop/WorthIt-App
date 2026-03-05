import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="WorthIt", page_icon="🔍")

# 1. Configuración ultra-limpia
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("🚨 LA LLAVE NO ESTÁ EN SECRETS. Ve a Settings -> Secrets y ponla.")
    st.stop()

api_key = st.secrets["GOOGLE_API_KEY"].strip()
genai.configure(api_key=api_key)

st.title("🔍 WorthIt")

# 2. Selector de modelo automático (Para matar el 404)
img_file = st.file_uploader("📸 HAZ LA FOTO", type=['jpg', 'jpeg', 'png'])

if img_file:
    img = Image.open(img_file)
    st.image(img, use_container_width=True)
    
    if st.button("💰 ¿CUÁNTO VALE?"):
        with st.spinner("Analizando..."):
            # INTENTO 1: Modelo estándar
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(["¿Qué es esto y cuánto vale? Sé breve", img])
                st.success("¡FUNCIONA!")
                st.write(response.text)
            except Exception as e1:
                # INTENTO 2: Si el 1 da 404, probamos el nombre largo
                try:
                    model_alt = genai.GenerativeModel('models/gemini-1.5-flash')
                    response = model_alt.generate_content(["¿Qué es esto y cuánto vale?", img])
                    st.success("¡FUNCIONA (Vía alternativa)!")
                    st.write(response.text)
                except Exception as e2:
                    # SI TODO FALLA, ESCUPIMOS EL ERROR REAL
                    st.error("🔴 SIGUE DANDO ERROR")
                    st.warning(f"Error 1: {e1}")
                    st.warning(f"Error 2: {e2}")
                    st.info("Si el error dice 'User location not supported', es que España está bloqueada temporalmente en tu cuenta de Google.")
