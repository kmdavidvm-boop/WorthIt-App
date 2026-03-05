import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configuración de la página
st.set_page_config(page_title="WorthIt - ¿Cuánto vale?", layout="centered")

st.title("🔍 WorthIt")
st.write("Apunta con la cámara trasera a un objeto para saber su valor.")

# Barra lateral para la API Key
api_key = st.sidebar.text_input("Pega aquí tu API Key de Google", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # Usamos gemini-1.5-flash que es el más rápido y compatible
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Cámara configurada para usar la trasera (facing_mode="environment")
        img_file = st.camera_input("Captura el objeto", facing_mode="environment")

        if img_file:
            img = Image.open(img_file)
            st.image(img, caption="Analizando...", use_container_width=True)
            
            prompt = """
            Identifica este objeto de la foto. 
            Responde con este formato:
            - **Nombre:** [Nombre del objeto]
            - **Valor estimado:** [Rango de precio en euros/dólares]
            - **Curiosidad:** [Un dato interesante corto]
            - **Dónde encontrarlo:** [Nombres de tiendas o plataformas]
            """
            
            with st.spinner("La IA está pensando..."):
                # Enviamos la imagen y el texto
                response = model.generate_content([prompt, img])
                st.subheader("Resultado:")
                st.write(response.text)
                
    except Exception as e:
        st.error(f"Hubo un error: {e}")
else:
    st.warning("👈 Introduce tu API Key en la barra lateral para empezar.")
