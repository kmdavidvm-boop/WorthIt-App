import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configuración Apple-Style
st.set_page_config(page_title="WorthIt", page_icon="🔍", layout="centered")

# Estilos CSS para botones más elegantes
st.markdown("""
    <style>
    .stButton>button {
        background-color: #007AFF;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 10px 25px;
        font-weight: 600;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #005bb5;
    }
    </style>
""", unsafe_allow_html=True)

# Lógica de conexión
try:
    api_key = st.secrets["GOOGLE_API_KEY"].strip()
    genai.configure(api_key=api_key)
    def get_model():
        models = genai.list_models()
        for m in models:
            if 'generateContent' in m.supported_generation_methods and ('1.5' in m.name):
                return genai.GenerativeModel(m.name)
        return None
    model = get_model()
except:
    st.error("Error de conexión")

# MENÚ DESPLEGABLE (Sidebar / Tres rayas)
with st.sidebar:
    st.title("WorthIt")
    opcion = st.radio("Navegación", ["🔍 Buscador", "ℹ️ Sobre"])

# LÓGICA DE LAS OPCIONES
if opcion == "🔍 Buscador":
    st.title("¿Qué tienes ahí?")
    st.write("Sube una foto y deja que la IA valore tu objeto.")
    
    img_file = st.file_uploader("", type=['jpg', 'jpeg', 'png'])
    
    if img_file:
        img = Image.open(img_file)
        st.image(img, use_container_width=True)
        
        if st.button("Buscar"): # Botón rediseñado con CSS
            with st.spinner("Analizando..."):
                try:
                    response = model.generate_content(["Identifica este objeto y dame su precio de segunda mano en euros. Sé breve y directo.", img])
                    st.markdown("### Resultado")
                    st.write(response.text)
                except Exception as e:
                    st.error("Error al conectar con la IA.")

elif opcion == "ℹ️ Sobre":
    st.title("ℹ️ Sobre WorthIt")
    st.write("""
    **¿Cómo funciona?**
    WorthIt utiliza Inteligencia Artificial de última generación para analizar visualmente tus objetos.
    
    **¿Para qué sirve?**
    * Identificar objetos antiguos o desconocidos.
    * Obtener una estimación rápida del valor de mercado de segunda mano.
    * Aprender curiosidades sobre tus pertenencias.
    
    *Creado para dar una segunda vida a lo que ya tienes.*
    """)
