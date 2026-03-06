import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configuración inicial
st.set_page_config(page_title="WorthIt", layout="wide")

# CSS para el diseño estilo iOS (Tarjetas, sombras y colores)
st.markdown("""
    <style>
    .card { background: #FFFFFF; border-radius: 20px; padding: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
    .big-price { font-size: 32px; font-weight: 800; color: #007AFF; }
    .nav-bar { position: fixed; bottom: 0; width: 100%; background: #F8F9FA; padding: 15px; display: flex; justify-content: space-around; }
    </style>
""", unsafe_allow_html=True)

# Lógica de Estado
if 'total' not in st.session_state: st.session_state.total = 1235
if 'historial' not in st.session_state: st.session_state.historial = []

# Header
st.markdown("## 🍎 WorthIt")
st.markdown(f'<div class="card"><p>Total Acumulado</p><p class="big-price">€{st.session_state.total}</p></div>', unsafe_allow_html=True)

# Columnas tipo Apple (Current Value y Last Appraisal)
col1, col2 = st.columns(2)
with col1: st.markdown('<div class="card"><b>Current Value</b><br>€450</div>', unsafe_allow_html=True)
with col2: st.markdown('<div class="card"><b>Last Appraisal</b><br>€85</div>', unsafe_allow_html=True)

st.write("---")
st.subheader("Recently Valued")

# Historial (donde aparecerán los objetos)
for item in st.session_state.historial:
    st.write(f"✅ {item['nombre']} - €{item['precio']}")

# Botón "+" flotante (simulado abajo)
st.markdown("<br><br>", unsafe_allow_html=True)
if st.button("➕ Añadir nuevo objeto"):
    st.session_state.adding = True

if 'adding' in st.session_state:
    archivo = st.file_uploader("Sube una foto", type=['jpg', 'png'])
    if archivo:
        st.image(archivo, use_container_width=True)
        if st.button("Analizar ahora"):
            # Aquí iría la lógica de tu modelo
            st.session_state.total += 200 # Ejemplo de suma
            st.rerun()
