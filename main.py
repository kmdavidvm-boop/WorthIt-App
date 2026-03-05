import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="WorthIt", layout="centered")

st.title("🔍 WorthIt")

api_key = st.sidebar.text_input("API Key de Google", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Quitamos el facing_mode para evitar el error de versión
        img_file = st.camera_input("Captura el objeto")

        if img_file:
            img = Image.open(img_file)
            st.image(img, use_container_width=True)
            
            prompt = "Identifica este objeto. Dime su nombre, precio aproximado de mercado y un dato curioso."
            
            with st.spinner("Analizando..."):
                response = model.generate_content([prompt, img])
                st.write(response.text)
                
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("Introduce tu API Key en el menú de la izquierda.")
