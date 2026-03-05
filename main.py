import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

st.set_page_config(page_title="WorthIt", page_icon="🔍")

try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("Error en la configuración de la llave.")

st.title("🔍 WorthIt")

img_file = st.file_uploader("📸 TOCA AQUÍ PARA EMPEZAR", type=['jpg', 'png', 'jpeg'])

if img_file:
    # Procesamos la imagen para que pese MUCHO menos
    img = Image.open(img_file)
    
    # Reducir tamaño a 500px (suficiente para la IA)
    img.thumbnail((500, 500))
    
    st.image(img, caption="Imagen optimizada")
    
    if st.button("💰 ¿CUÁNTO VALE?"):
        with st.spinner("Analizando..."):
            try:
                # Convertimos la imagen a un formato ultraligero
                buf = io.BytesIO()
                img.save(buf, format='JPEG', quality=70)
                byte_im = buf.getvalue()
                
                # Enviamos los bytes directamente
                response = model.generate_content([
                    "Identifica este objeto. Dime nombre, precio aproximado de segunda mano y una curiosidad. Sé muy breve.",
                    {"mime_type": "image/jpeg", "data": byte_im}
                ])
                
                st.subheader("Resultado:")
                st.write(response.text)
            except Exception as e:
                st.error(f"Error: {e}")
