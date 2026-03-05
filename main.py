import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configuración de la página
st.set_page_config(page_title="WorthIt - ¿Cuánto vale?", layout="centered")

st.title("🔍 WorthIt")
st.write("Haz una foto a cualquier objeto para saber su valor y curiosidades.")

# Aquí va tu llave de API (la configuraremos de forma segura en el siguiente paso)
api_key = st.sidebar.text_input("Pega aquí tu API Key de Google", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Componente de cámara
    img_file = st.camera_input("Captura el objeto")

    if img_file:
        img = Image.open(img_file)
        st.image(img, caption="Analizando objeto...", use_column_width=True)
        
        # El "prompt" o instrucción para la IA
        prompt = """
        Identifica este objeto. 
        Dime: 1. Nombre exacto. 2. Un rango de precio estimado en el mercado de segunda mano. 
        3. Un dato curioso breve. 4. Tres enlaces de búsqueda (eBay, Amazon, Google Shopping).
        Responde de forma clara y amigable.
        """
        
        with st.spinner("Buscando información..."):
            response = model.generate_content([prompt, img])
            st.subheader("Resultado:")
            st.write(response.text)
else:
    st.warning("Por favor, introduce tu API Key en la barra lateral para empezar.")
