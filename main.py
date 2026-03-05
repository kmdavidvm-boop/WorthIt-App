import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Configuración de la página
st.set_page_config(page_title="WorthIt", page_icon="🔍")

# 2. Conexión invisible con tu llave (Secrets)
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("Error de configuración: La llave no está en los Secrets.")

# 3. Diseño de la App
st.title("🔍 WorthIt")
st.write("Identifica y tasa cualquier objeto al instante.")

# Creamos un botón principal
if "ver_opciones" not in st.session_state:
    st.session_state.ver_opciones = False

def mostrar_menu():
    st.session_state.ver_opciones = True

# Si no ha pulsado el botón, mostramos el botón grande de "FOTO"
if not st.session_state.ver_opciones:
    st.button("📸 HACER FOTO / SUBIR IMAGEN", on_click=mostrar_menu, use_container_width=True)

# Si ya pulsó el botón, mostramos las dos opciones
else:
    opcion = st.radio("¿Qué quieres hacer?", ("Abrir Cámara", "Seleccionar Archivo / Imagen"), index=None)

    img_file = None
    
    if opcion == "Abrir Cámara":
        img_file = st.camera_input("Enfoca el objeto")
    elif opcion == "Seleccionar Archivo / Imagen":
        img_file = st.file_uploader("Elige una imagen de tu galería", type=['jpg', 'png', 'jpeg'])

    # Si se captura o sube una imagen, procesamos
    if img_file:
        img = Image.open(img_file)
        st.image(img, caption="Imagen cargada", use_container_width=True)
        
        with st.spinner("Analizando objeto y buscando valor..."):
            try:
                prompt = "Identifica este objeto. Dime su nombre, su valor aproximado en euros en el mercado de segunda mano y un dato curioso."
                response = model.generate_content([prompt, img])
                st.success("¡Análisis completado!")
                st.markdown(f"### Resultado:\n{response.text}")
