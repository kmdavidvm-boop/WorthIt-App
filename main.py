import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Configuración de la página
st.set_page_config(page_title="WorthIt", page_icon="🔍")

# 2. Conexión invisible con tu llave
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("Revisa los Secrets en Streamlit.")

# 3. Diseño de la App
st.title("🔍 WorthIt")
st.write("Pulsa el botón de abajo para identificar un objeto.")

# 4. EL TRUCO MÁGICO:
# Usamos file_uploader pero con una etiqueta que incite a la acción.
# En iPad/iPhone, al no especificar 'camera_input', el sistema abre su propio menú.
img_file = st.file_uploader("📸 PULSA AQUÍ PARA HACER FOTO O SUBIR", type=['jpg', 'png', 'jpeg'])

if img_file:
    img = Image.open(img_file)
    st.image(img, use_container_width=True)
    
    with st.spinner("Analizando..."):
        try:
            prompt = "Identifica este objeto, di su valor en euros de segunda mano y una curiosidad corta."
            response = model.generate_content([prompt, img])
            st.success("¡Analizado!")
            st.markdown(f"**Resultado:**\n{response.text}")
        except Exception as e:
            st.error(f"Error: {e}")
