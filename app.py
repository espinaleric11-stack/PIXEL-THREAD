# --- PANEL DERECHO: Vista Previa 3D y Selector de Color ---
with col_right:
    st.markdown('<div class="preview-box">', unsafe_allow_html=True)
    st.markdown("#### 🧊 Visor 3D en Vivo")
    
    shirt_color = st.color_picker("Color Base del Producto", "#ffffff")
    
    # Usamos el componente HTML5 <model-viewer> optimizado para cargar modelos 3D reales (.glb / .gltf)
    # Puedes cambiar la URL del src por la ruta de tu propio archivo 3D alojado en GitHub o un CDN.
    model_viewer_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script type="module" src="https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js"></script>
        <style>
            body {{ margin: 0; background-color: #262626; }}
            model-viewer {{
                width: 100%;
                height: 360px;
                background-color: #1e1e1e;
                border-radius: 12px;
            }}
        </style>
    </head>
    <body>
        <model-viewer 
            src="https://modelviewer.dev/shared-assets/models/Astronaut.glb" 
            alt="Maqueta 3D de Camiseta" 
            auto-rotate 
            camera-controls 
            ar>
        </model-viewer>
    </body>
    </html>
    """
    
    # Renderizamos el visor 3D interactivo dentro de Streamlit usando componentes HTML
    st.components.v1.html(model_viewer_html, height=380)
    
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
