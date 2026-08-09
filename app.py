import streamlit as st
from PIL import Image
import io

# Configuración de página con diseño ancho y tema oscuro
st.set_page_config(
    page_title="Pixel Thread - Estudio de Diseño y Maquetas 3D",
    page_icon="👕",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilos CSS avanzados para imitar exactamente la interfaz oscura de la captura
st.markdown("""
    <style>
    /* Fondo general oscuro */
    .stApp {
        background-color: #1e1e1e;
        color: #ffffff;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Ocultar elementos predeterminados de Streamlit para limpieza de interfaz */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Contenedor principal estilo estudio */
    .studio-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #191919;
        padding: 12px 24px;
        border-bottom: 1px solid #333;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    
    .panel-box {
        background-color: #262626;
        border: 1px solid #3b3b3b;
        border-radius: 12px;
        padding: 16px;
        height: 720px;
        overflow-y: auto;
    }
    
    .canvas-box {
        background-color: #191919;
        border: 1px solid #3b3b3b;
        border-radius: 12px;
        padding: 24px;
        height: 720px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
    }
    
    .preview-box {
        background-color: #262626;
        border: 1px solid #3b3b3b;
        border-radius: 12px;
        padding: 16px;
        height: 720px;
    }
    
    .stButton>button {
        background-color: #00cec9;
        color: #111;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        padding: 8px 16px;
    }
    .stButton>button:hover {
        background-color: #01a3a4;
        color: #fff;
    }
    </style>
""", unsafe_allow_html=True)

# Barra superior estilo app profesional
col_top1, col_top2, col_top3 = st.columns([2, 6, 2])
with col_top1:
    if st.button("✕  Subir y Diseñar"):
        st.toast("Panel de herramientas activo")
with col_top2:
    st.markdown("<h3 style='text-align: center; margin: 0; color: #fff;'>Pixel Thread Studio 3D</h3>", unsafe_allow_html=True)
with col_top3:
    if st.button("Guardar Proyecto", use_container_width=True):
        st.success("¡Proyecto guardado con éxito!")

st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)

# Layout de 3 columnas principales
col_left, col_center, col_right = st.columns([1.2, 2.2, 1.4], gap="medium")

# --- PANEL IZQUIERDO: Biblioteca de Archivos y Elementos ---
with col_left:
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    st.markdown("#### 📁 Archivos y Recursos")
    
    uploaded_file = st.file_uploader("Subir JPG, PNG, SVG", type=["png", "jpg", "jpeg", "svg"])
    
    st.markdown("---")
    st.markdown("**Diseños Recientes:**")
    
    # Galería de recursos precargados (como el oso Pixel Thread y elementos vectoriales)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
            <div style='background: #333; padding: 10px; border-radius: 8px; text-align: center;'>
                <p style='font-size: 11px; margin-bottom: 5px;'>Logotipo PT</p>
                🐻‍❄️
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
            <div style='background: #333; padding: 10px; border-radius: 8px; text-align: center;'>
                <p style='font-size: 11px; margin-bottom: 5px;'>Vectorial</p>
                🎨
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**Herramientas de Texto y IA:**")
    text_input = st.text_input("Añadir Texto al Diseño", "Pixel Thread")
    font_style = st.selectbox("Estilo de fuente", ["Urbano / Bold", "Cursiva", "Clásica"])
    
    if st.button("Generar con IA (Logo)", use_container_width=True):
        st.info("Generador IA activado para estilos de bordado urbano.")
        
    st.markdown('</div>', unsafe_allow_html=True)

# --- PANEL CENTRAL: Lienzo de Patrones (Frente, Espalda, Mangas) ---
with col_center:
    st.markdown('<div class="canvas-box">', unsafe_allow_html=True)
    st.markdown("<h4 style='color: #ccc; margin-bottom: 10px;'>Plantilla de Despiece de Camiseta</h4>", unsafe_allow_html=True)
    
    # Representación visual de los patrones de tela (Frente y Espalda planos con diseño colocado)
    pattern_col1, pattern_col2, pattern_col3 = st.columns([2, 2, 1])
    
    with pattern_col1:
        st.markdown("""
            <div style='background: #fff; color: #000; border-radius: 12px; padding: 20px; height: 380px; display: flex; flex-direction: column; align-items: center; justify-content: center; box-shadow: 0 4px 12px rgba(0,0,0,0.3);'>
                <p style='font-size: 12px; font-weight: bold; margin-bottom: 10px;'>FRENTE</p>
                <div style='border: 2px dashed #00cec9; border-radius: 50%; width: 100px; height: 100px; display: flex; align-items: center; justify-content: center; background: #f9f9f9;'>
                    <span style='font-size: 24px;'>🐻</span>
                </div>
                <p style='font-size: 10px; color: #666; margin-top: 10px;'>Pixel Thread Logo</p>
            </div>
        """, unsafe_allow_html=True)
        
    with pattern_col2:
        st.markdown("""
            <div style='background: #fff; color: #000; border-radius: 12px; padding: 20px; height: 380px; display: flex; flex-direction: column; align-items: center; justify-content: center; box-shadow: 0 4px 12px rgba(0,0,0,0.3);'>
                <p style='font-size: 12px; font-weight: bold; margin-bottom: 10px;'>ESPALDA</p>
                <div style='border: 2px dashed #ccc; border-radius: 50%; width: 100px; height: 100px; display: flex; align-items: center; justify-content: center; background: #f9f9f9;'>
                    <span style='font-size: 12px; color: #999;'>Vacío</span>
                </div>
                <p style='font-size: 10px; color: #666; margin-top: 10px;'>Área libre</p>
            </div>
        """, unsafe_allow_html=True)

    with pattern_col3:
        st.markdown("""
            <div style='background: #fff; color: #000; border-radius: 12px; padding: 10px; height: 380px; display: flex; flex-direction: column; align-items: center; justify-content: center; box-shadow: 0 4px 12px rgba(0,0,0,0.3);'>
                <p style='font-size: 10px; font-weight: bold;'>MANGAS</p>
                <div style='border: 1px solid #ccc; width: 60px; height: 40px; margin-bottom: 15px; background: #f9f9f9;'></div>
                <div style='border: 1px solid #ccc; width: 60px; height: 40px; background: #f9f9f9;'></div>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Barra de herramientas inferior del lienzo (Zoom, deshacer, etc.)
    tools_col1, tools_col2, tools_col3, tools_col4 = st.columns(4)
    with tools_col1:
        st.markdown("↩️ ↪️ Deshacer")
    with tools_col2:
        zoom_val = st.slider("Zoom", 50, 200, 100, label_visibility="collapsed")
    with tools_col3:
        st.markdown("👁️ Vista Previa")
    with tools_col4:
        st.markdown("⚡ **Créditos: 50**")
        
    st.markdown('</div>', unsafe_allow_html=True)

# --- PANEL DERECHO: Vista Previa 3D y Selector de Color ---
with col_right:
    st.markdown('<div class="preview-box">', unsafe_allow_html=True)
    st.markdown("#### 🧊 Visor 3D en Vivo")
    
    # Contenedor simulando el modelo 3D renderizado de la camiseta
    shirt_color = st.color_picker("Color Base del Producto", "#ffffff")
    
    st.markdown(f"""
        <div style='
            background: linear-gradient(135deg, {shirt_color} 0%, #e0e0e0 100%);
            border: 2px solid #444;
            border-radius: 16px;
            height: 380px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            position: relative;
            box-shadow: inset 0 0 20px rgba(0,0,0,0.1);
        '>
            <div style='position: absolute; top: 10px; right: 10px; background: #000; color: #fff; padding: 2px 8px; border-radius: 4px; font-size: 10px;'>3D Rotar</div>
            <span style='font-size: 64px;'>👕</span>
            <p style='color: #222; font-weight: bold; margin-top: 10px;'>Pixel Thread Custom</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**Paleta de Colores Rápidos:**")
    
    pal_cols = st.columns(6)
    colors = ["#ffffff", "#e0e0e0", "#333333", "#a93226", "#8e44ad", "#f5b041"]
    for i, col in enumerate(pal_cols):
        with col:
            st.markdown(f"""
                <div style='background-color: {colors[i]}; width: 28px; height: 28px; border-radius: 50%; border: 1px solid #666; margin: auto;'></div>
            """, unsafe_allow_html=True)
            
    st.markdown('</div>', unsafe_allow_html=True)
