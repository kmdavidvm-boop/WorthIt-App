import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="WorthIt", page_icon="💰")

# --- Lógica de Estado ---
if 'total_valor' not in st.session_state: st.session_state.total_valor = 0
if 'historial' not in st.session_state: st.session_state.historial = []

# --- Configuración IA ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"].strip())
    model = genai.GenerativeModel('gemini-1.5-flash')
except: st.error("Error de configuración.")

# --- CSS para el estilo Apple ---
st.markdown("""
    <style>
    .big-font { font-size:40px !important; font-weight: bold; color: #007AFF; }
    .stButton>button { border-radius: 50%; width: 60px; height: 60px; }
    </style>
""", unsafe_allow_html=True)

# --- Interfaz Principal ---
st.title("🍎 WorthIt")

# Contador superior
st.markdown(f"### Total Acumulado")
st.markdown(f'<p class="big-font">€{st.session_state.total_valor}</p>', unsafe_allow_html=True)

# Historial reciente
st.subheader("Recently Valued")
for item in reversed(st.session_state.historial):
    st.info(f"**{item['nombre']}**: €{item['precio']}")

# --- El botón "+" para añadir ---
if st.button("➕"):
    st.session_state.modo_carga = True

if 'modo_carga' in st.session_state and st.session_state.modo_carga:
    img_file = st.file_uploader("Sube foto del objeto", type=['jpg', 'jpeg', 'png'])
    if img_file:
        img = Image.open(img_file)
        if st.button("Analizar"):
            with st.spinner("Tasando..."):
                # Aquí la IA procesa y nos da un precio numérico
                # (Nota: En un caso real, necesitarías procesar la respuesta para extraer el número)
                response = model.generate_content(["Dame solo el nombre del objeto y su precio en números, separados por una coma.", img])
                data = response.text.split(',')
                nombre = data[0]
                precio = int(''.join(filter(str.isdigit, data[1])))
                
                st.session_state.total_valor += precio
                st.session_state.historial.append({'nombre': nombre, 'precio': precio})
                st.session_state.modo_carga = False
                st.rerun()
