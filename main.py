import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# 1. Configuración de la página
st.set_page_config(page_title="WorthIt", page_icon="🔍")

# 2. Conexión invisible con tu llave
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    # Usamos gemini-1.5-flash que es el más rápido para evitar esperas
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Error en Secrets: {e}")

# 3. Diseño de la App
st.title("🔍 WorthIt")
st.write("Sube una foto para saber el precio de mercado.")

# 4. El cargador de archivos (Menú nativo de Apple)
img_file = st.file_uploader("📸 PULSA AQUÍ PARA HACER FOTO O SUBIR", type=['jpg', 'png', 'jpeg'])

if img_file:
    # Mostramos la imagen inmediatamente para que el usuario sepa que se ha subido
    img = Image.open(img_file)
    st.image(img, caption="Imagen recibida", use_container_width=True)
    
    # Botón para confirmar el análisis (esto evita que se ejecute solo si hay lag)
    if st.button("💰 CALCULAR PRECIO"):
        with st.spinner("Buscando en bases de datos..."):
            try:
                # TRUCO: Reducimos el tamaño de la imagen internamente para que vuele por internet
                img.thumbnail((800, 800)) 
                
                prompt = "Identifica este objeto. Dime: 1. Nombre exacto. 2. Precio estimado de segunda mano en España (en euros). 3. Un dato curioso. Responde de forma esquemática y rápida."
                
                # Llamada a la IA
                response = model.generate_content([prompt, img])
                
                if response.text:
                    st.success("¡Análisis listo!")
                    st.markdown(f"### {response.text}")
                else:
                    st.warning("La IA no ha podido generar una respuesta. Prueba con otra foto.")
                    
            except Exception as e:
                # Si hay un error de "Quota" o de "API Key", aquí nos lo dirá
                st.error(f"Vaya, algo ha fallado: {e}")
                st.info("Prueba a refrescar la página o espera 1 minuto.")
