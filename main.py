import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Configuración de la página
st.set_page_config(page_title="WorthIt", page_icon="🔍")

# 2. Conexión invisible con tu llave (usando los Secrets)
# Asegúrate de haber guardado GOOGLE_API_KEY en los ajustes de Streamlit Cloud
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("Error de configuración: La llave no está en los Secrets.")

# 3. Diseño de la App
st.title("🔍 WorthIt")
st.write("¡Hola! Haz una foto a cualquier cosa y te diré qué es y cuánto vale.")

# 4. Funcionalidad
img_file = st.camera_input("Haz una foto")

if img_file:
    img = Image.open(img_file)
    with st.spinner("Buscando precio..."):
        # El prompt es la orden que le das a la IA
        prompt = "Identifica este objeto. Dime su nombre, su valor aproximado en euros en el mercado de segunda mano en España y una curiosidad corta."
        response = model.generate_content([prompt, img])
        st.success("¡Encontrado!")
        st.write(response.text)
