import streamlit as st
from PIL import Image, ImageOps, ImageDraw

# Configuración de la página
st.set_page_config(
    page_title="Pixel Thread - Maquetas 3D y Diseños de Camisetas",
    page_icon="👕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados para darle un toque profesional
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #191919;
        font-weight: 700;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4C4C4C;
        margin-bottom: 30px;
    }
    .card {
        background-color: #f7f7f7;
        border: 1px solid #191919;
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Encabezado principal
st.markdown('<p class="main-header">Personaliza y descarga maquetas de camisetas</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Crea maquetas profesionales para tu marca en minutos. Personaliza colores, estilos y sube tu propio logotipo.</p>', unsafe_allow_html=True)

# Panel lateral de control
st.sidebar.header("🛠️ Panel de Personalización")

# 1. Color de la camiseta
tshirt_color = st.sidebar.color_picker("Color de la camiseta", "#191919")

# 2. Selección de estilo / vista
view_mode = st.sidebar.selectbox("Vista de la maqueta", ["Frente", "Espalda", "Lateral"])

# 3. Subida de logotipo o diseño
uploaded_logo = st.sidebar.file_uploader("Sube tu logotipo (PNG / JPG)", type=["png", "jpg", "jpeg"])

# 4. Tamaño del diseño en la camiseta
logo_scale = st.sidebar.slider("Tamaño del diseño", min_value=50, max_value=250, value=120)

# Diseño de la interfaz principal en dos columnas
col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown("### 👕 Vista Previa Interactiva")
    
    # Creación visual dinámica de la camiseta usando un contenedor estilizado
    preview_container = st.container()
    
    with preview_container:
        # Generamos una representación visual limpia mediante un cuadro interactivo
        st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, {tshirt_color}22 0%, {tshirt_color}55 100%);
                border: 2px solid #191919;
                border-radius: 24px;
                padding: 40px;
                text-align: center;
                box-shadow: 0px 10px 30px rgba(0,0,0,0.08);
                min-height: 420px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
            ">
                <h3 style="color: {tshirt_color}; margin-bottom: 10px;">Vista: {view_mode}</h3>
                <p style="color: #666; font-size: 14px;">Color activo: {tshirt_color}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Si el usuario sube un logo, lo mostramos superpuesto o referenciado
        if uploaded_logo is not None:
            image = Image.open(uploaded_logo)
            st.image(image, caption="Logotipo aplicado a la maqueta", width=logo_scale)

with col2:
    st.markdown("### 📦 Opciones de Descarga y Exportación")
    
    st.markdown("""
        <div class="card">
            <h4>Alta Calidad 4K</h4>
            <p>Exporta tu diseño en formato PNG transparente de máxima resolución listo para producción o redes sociales.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Botones de acción simulados para exportar
    if st.button("📥 Descargar Imagen PNG (4K)", use_container_width=True):
        st.success("¡Maqueta procesada con éxito! La descarga comenzará en breve.")
        
    if st.button("🎥 Exportar Video de Presentación (MP4)", use_container_width=True):
        st.info("Generando animación 3D de rotación...")

# Sección inferior de características
st.markdown("---")
col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown("#### ✨ Texturas Realistas")
    st.write("Acabados de tela de alta fidelidad optimizados para marcas de ropa y digitalización.")

with col_b:
    st.markdown("#### ⚡ Sincronización Rápida")
    st.write("Visualiza cambios de color y posición de logotipos en tiempo real.")

with col_c:
    st.markdown("#### 🚀 Listo para Producción")
    st.write("Compatible con estándares de la industria para previsualizar productos antes de bordar o estampar.")
