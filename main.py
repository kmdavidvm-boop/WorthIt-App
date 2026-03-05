import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="WorthIt", page_icon="🔍")

# 1. Configuración ULTRA-ESTRICTA
try:
    # Leemos la clave de tus Secrets
    llave = st.secrets["GOOGLE_API_KEY"].strip() # .strip() quita espacios invisibles
    genai.configure(api_key=llave)
    
    # FORZAMOS el nombre técnico completo del modelo
    # En Europa a veces solo funciona con el prefijo 'models/'
    model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')
except Exception as e:
    st.error(f"Error de configuración: {e}")

st.title("🔍 WorthIt")

# 2. El botón que querías (Menú nativo de Apple)
img_file = st.file_uploader("📸 TOCA AQUÍ PARA HACER FOTO", type=['jpg', 'png', 'jpeg'])

if img_file:
    img = Image.open(img_file)
    st.image(img, use_container_width=True)
    
    if st.button("💰 ¿CUÁNTO VALE?"):
        with st.spinner("Analizando..."):
            try:
                # Prompt directo
                prompt = "Identifica este objeto y dime su precio de segunda mano en euros. Sé muy breve."
                
                # Llamada directa
                response = model.generate_content([prompt, img])
                
                if response:
                    st.success("¡Resultado!")
                    st.write(response.text)
            except Exception as e:
                # Si esto falla, el error que salga aquí nos dirá la verdad absoluta
                st.error(f"Error de Google: {e}")
                st.info("Si pone 'User location not supported', avísame, es un ajuste regional.")
