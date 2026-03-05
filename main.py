import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="WorthIt", page_icon="🔍")

# Configurar la API
try:
    # El .strip() elimina cualquier espacio que se cuele al copiar
    key = st.secrets["GOOGLE_API_KEY"].strip()
    genai.configure(api_key=key)
    # Forzamos el modelo más nuevo
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Error con la llave: {e}")

st.title("🔍 WorthIt")

# Subida de imagen nativa (Apple Style)
img_file = st.file_uploader("📸 TOCA PARA HACER FOTO O SUBIR", type=['jpg', 'jpeg', 'png'])

if img_file:
    img = Image.open(img_file)
    st.image(img, use_container_width=True)
    
    if st.button("💰 ¿CUÁNTO VALE?"):
        with st.spinner("Consultando a la IA..."):
            try:
                # El comando para la IA
                response = model.generate_content(["Dime qué es este objeto y su precio aproximado de segunda mano en euros. Sé muy breve.", img])
                
                if response.text:
                    st.success("¡Hecho!")
                    st.write(response.text)
            except Exception as e:
                st.error(f"Error de Google: {e}")
                st.info("Si pone 'API_KEY_INVALID', es que la nueva llave aún no se ha guardado bien.")
