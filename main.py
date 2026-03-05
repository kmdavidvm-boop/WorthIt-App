import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Configuración de la página e icono
st.set_page_config(page_title="WorthIt", page_icon="🔍")

# 2. Conexión invisible con tu llave (Secrets)
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Error de configuración: Revisa los Secrets en Streamlit.")

# 3. Diseño de la App
st.title("🔍 WorthIt")
st.write("Pulsa el botón para empezar a tasar objetos.")

# Inicializamos el estado de la sesión si no existe
if "ver_opciones" not in st.session_state:
    st.session_state.ver_opciones = False

# Función para cambiar el estado al pulsar el botón
def activar_menu():
    st.session_state.ver_opciones = True

# LÓGICA DE LA INTERFAZ
if not st.session_state.ver_opciones:
    # Botón inicial grande
    st.button("📸 FOTO", on_click=activar_menu, use_container_width=True)
else:
    # Menú de selección
    opcion = st.radio("¿Cómo quieres subir la imagen?", 
                      ("Cámara", "Seleccionar archivo de la galería"),
                      index=None)

    img_file = None
    if opcion == "Cámara":
        img_file = st.camera_input("Enfoca el objeto")
    elif opcion == "Seleccionar archivo de la galería":
        img_file = st.file_uploader("Elige una imagen", type=['jpg', 'png', 'jpeg'])

    # Si hay una imagen, la procesamos
    if img_file:
        img = Image.open(img_file)
        st.image(img, use_container_width=True)
        
        with st.spinner("Analizando precio..."):
            try:
                prompt = "Identifica este objeto. Dime su nombre, su valor aproximado en euros en el mercado de segunda mano y una curiosidad."
                response = model.generate_content([prompt, img])
                st.success("¡Hecho!")
                st.markdown(f"### Resultado:\n{response.text}")
                
                # Botón para reiniciar la app y volver al botón de "FOTO"
                if st.button("Hacer otra consulta"):
                    st.session_state.ver_opciones = False
                    st.rerun()
            except Exception as e:
                st.error(f"Hubo un problema con el análisis: {e}")
