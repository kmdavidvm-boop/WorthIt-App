import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Configuración rápida
st.set_page_config(page_title="WorthIt", page_icon="🔍")

# 2. Conexión (Asegúrate de que GOOGLE_API_KEY esté en Secrets)
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Error de configuración.")

st.title("🔍 WorthIt")

# 3. Cargador de archivos
img_file = st.file_uploader("📸 TOCA AQUÍ PARA BUSCAR PRECIO", type=['jpg', 'png', 'jpeg'])

if img_file:
    # Mostramos miniatura rápida
    img = Image.open(img_file)
    st.image(img, use_container_width=True)
    
    # Botón de acción
    if st.button("💰 ANALIZAR AHORA"):
        with st.spinner("Conectando con Google..."):
            try:
                # ENVIAR DIRECTAMENTE (Sin procesamientos extra que den lag)
                prompt = "Dime qué es esto, su precio de segunda mano en euros y una curiosidad. Sé muy breve."
                
                # Esta es la forma más estable de enviar archivos en Streamlit
                response = model.generate_content([prompt, img])
                
                if response:
                    st.subheader("Resultado:")
                    st.write(response.text)
                else:
                    st.error("Google no respondió. Intenta otra vez.")
            
            except Exception as e:
                st.error(f"Error técnico: {e}")
                st.info("Si el error persiste, revisa que tu API Key sea válida.")
