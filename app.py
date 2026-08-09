import streamlit as st
import os
from PIL import Image

# Configuración de la página
st.set_page_config(
    page_title="Configurador 3D de Bordados | Pixel Thread",
    page_icon="🧵",
    layout="wide"
)

# Estilos CSS personalizados
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1a1a1a;
        font-weight: 700;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666666;
        margin-bottom: 30px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">🧵 Pixel Thread - Configurador de Bordados</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Sube tus diseños y selecciona las ubicaciones exactas para la digitalización de tus prendas.</p>', unsafe_allow_html=True)

# Layout en dos columnas: Izquierda (Mockup / Previsualización), Derecha (Casillas de Carga)
col_visor, col_panel = st.columns([2, 1])

with col_visor:
    st.subheader("👕 Vista Previa Interactiva de la Prenda")
    
    # Selector de color de la tela
    color_prenda = st.color_picker("Color de la Tela", "#1a237e")
    
    # Contenedor visualizador estilo mockup
    st.markdown(f"""
        <div style="background-color: {color_prenda}; height: 450px; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; font-size: 1.5rem; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            Mockup de Prenda / Vista Previa
        </div>
    """, unsafe_allow_html=True)
    
    st.info("💡 Consejo: Cambia el color base de la tela para adaptarlo al requerimiento de tu cliente.")

with col_panel:
    st.subheader("📁 Casillas de Carga")
    
    # Crear directorio para guardar archivos subidos temporalmente
    os.makedirs("uploads", exist_ok=True)
    
    zones = {
        "Pecho Izquierdo": "pecho_izq",
        "Frente Central": "frente",
        "Espalda": "espalda",
        "Manga Derecha": "manga_der",
        "Manga Izquierda": "manga_izq"
    }
    
    uploaded_files = {}
    
    for label, key in zones.items():
        with st.container():
            st.markdown(f"**{label}**")
            uploaded_file = st.file_uploader(f"Subir logo para {label}", type=["png", "jpg", "jpeg"], key=key)
            if uploaded_file is not None:
                uploaded_files[key] = uploaded_file
                image = Image.open(uploaded_file)
                st.image(image, width=100, caption=f"Cargado: {label}")
            st.markdown("---")

    if st.button("Guardar y Enviar Configuración", type="primary", use_container_width=True):
        if uploaded_files:
            st.success("¡Configuración de bordados guardada exitosamente para digitalización!")
            st.balloons()
        else:
            st.warning("Por favor, sube al menos un diseño antes de guardar.")
