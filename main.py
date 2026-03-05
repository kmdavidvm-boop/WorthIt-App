import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

st.set_page_config(page_title="WorthIt", page_icon="🔍")

# Lista de posibles nombres del modelo (el 404 suele ser por esto)
MODELOS_A_PROBAR = [
    'gemini-1.5-flash',
    'gemini-1.5-flash-latest',
    'models/gemini-1.5-flash',
    'gemini-pro-vision'
]

def configurar_modelo(api_key):
    genai.configure(api_key=api_key)
    for nombre in MODELOS_A_PROBAR:
        try:
            m = genai.GenerativeModel(nombre)
            # Prueba rápida para ver si el modelo existe
            m.generate_content("hola") 
            return m, nombre
        except:
            continue
    return None, None

st.title("🔍 WorthIt")

try:
    key = st.secrets["GOOGLE_API_KEY"]
    model, modelo_funcional = configurar_modelo(key)
    
    if model:
        st.sidebar.success(f"Conectado: {modelo_funcional}")
    else:
        st.error("No se encontró un modelo compatible. Revisa tu API Key.")
except Exception as e:
    st.error(f"Error crítico: {e}")

img_file = st.file_uploader("📸 TOCA AQUÍ PARA EMPEZAR", type=['jpg', 'png', 'jpeg'])

if img_file and model:
    img = Image.open(img_file)
    img.thumbnail((500, 500))
    st.image(img)
    
    if st.button("💰 ¿CUÁNTO VALE?"):
        with st.spinner("Analizando..."):
            try:
                prompt = "Identifica este objeto, su precio de segunda mano en euros y una curiosidad. Sé breve."
                response = model.generate_content([prompt, img])
                st.write(response.text)
            except Exception as e:
                st.error(f"Error al analizar: {e}")
