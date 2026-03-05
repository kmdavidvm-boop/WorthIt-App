import streamlit as st
import google.generativeai as genai

st.title("🔍 WorthIt - Test de Conexión")

try:
    # 1. Intentar leer la llave
    llave = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=llave)
    
    # 2. Intentar listar los modelos para ver si la llave funciona
    st.write("Verificando llave...")
    modelos = genai.list_models()
    
    # Si llega aquí, la llave es correcta
    st.success("✅ ¡Llave válida detectada!")
    
    # 3. Mostrar el primer modelo disponible
    lista = [m.name for m in modelos if 'generateContent' in m.supported_generation_methods]
    st.write(f"Modelos que puedes usar: {lista}")
    
    st.info("Ahora puedes volver a poner el código de la cámara, ¡ya sabemos que funciona!")

except Exception as e:
    st.error("❌ Error de conexión")
    st.code(str(e)) # Esto nos dirá el error real de Google
    st.warning("Si el error dice 'API key not valid', es que la copia de la llave falló.")
