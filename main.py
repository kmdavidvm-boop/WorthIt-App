import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# 1. Configuración de la ventana
st.set_page_config(page_title="WorthIt", page_icon="🔍")

# 2. Conexión con la IA (Usa tu secreto de Streamlit)
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    # Usamos el modelo más rápido y compatible
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Error: No se encontró la API Key en los Secrets de Streamlit.")

# 3. Interfaz de la App
st.title("🔍 WorthIt")
st.write("Haz una foto a un objeto para saber su valor.")

# Cargador de archivos (En iPhone/iPad abre el menú de Cámara/Fototeca)
img_file = st.file_uploader("📸 TOCA AQUÍ PARA HACER FOTO O SUBIR", type=['jpg', 'png', 'jpeg'])

if img_file:
    # Procesar imagen
    img = Image.open(img_file)
    
    # Mostrar la imagen que el usuario acaba de subir
    st.image(img, use_container_width=True)
    
    # Botón para activar la IA
    if st.button("💰 ¿CUÁNTO VALE?"):
        with st.spinner("Analizando con IA..."):
            try:
                # El mensaje que le enviamos a la IA
                prompt = "Identifica este objeto. Dime su nombre, su valor aproximado en euros en el mercado de segunda mano en España y un dato curioso."
                
                # Generar respuesta
                response = model.generate_content([prompt, img])
                
                if response.text:
                    st.success("¡Análisis completado!")
                    st.markdown("---")
                    st.markdown(response.text)
                else:
                    st.warning("La IA no pudo identificar el objeto. Intenta con otra foto.")
            
            except Exception as e:
                st.error(f"Hubo un error al conectar con Google: {e}")
                st.info("Asegúrate de que tu API Key sea válida y no tenga espacios.")

# Pie de página
st.caption("WorthIt App | Powered by Gemini 1.5 Flash")
