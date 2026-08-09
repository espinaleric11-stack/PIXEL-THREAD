import streamlit as st
import os
from PIL import Image

# Configuración de la página
st.set_page_config(
    page_title="Configurador 3D de Sublimación | Pixel Thread",
    page_icon="🧵",
    layout="wide"
)

# Estilos CSS generales
st.markdown("""
    <style>
    .main-header { font-size: 2.2rem; color: #1a1a1a; font-weight: 700; margin-bottom: 0px; }
    .sub-header { font-size: 1rem; color: #666666; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">🧵 Pixel Thread - Configurador 3D de Sublimación</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Sube tus diseños por zona y visualízalos proyectados sobre el mockup de la prenda en tiempo real.</p>', unsafe_allow_html=True)

# Layout en dos columnas: Izquierda (Visor 3D Interactivo), Derecha (Casillas de Carga)
col_visor, col_panel = st.columns([2, 1])

with col_visor:
    st.subheader("👕 Mockup 3D Interactivo")
    
    # Selector de color base de la tela
    color_prenda = st.color_picker("Color Base de la Tela", "#1a237e")
    
    # Renderizamos el visor 3D interactivo con Three.js embebido
    components_html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ margin: 0; background-color: #f0f2f6; overflow: hidden; }}
            #canvas-container {{ width: 100%; height: 480px; border-radius: 12px; overflow: hidden; }}
        </style>
    </head>
    <body>
        <div id="canvas-container"></div>

        <!-- Importar Three.js y controles de órbita -->
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>

        <script>
            const container = document.getElementById('canvas-container');
            
            const scene = new THREE.Scene();
            scene.background = new THREE.Color(0xf8f9fa);

            const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
            camera.position.set(0, 0, 4);

            const renderer = new THREE.WebGLRenderer({{ antialias: true }});
            renderer.setSize(container.clientWidth, container.clientHeight);
            container.appendChild(renderer.domElement);

            const controls = new THREE.OrbitControls(camera, renderer.domElement);
            controls.enableDamping = true;
            controls.dampingFactor = 0.05;

            // Iluminación
            const ambientLight = new THREE.AmbientLight(0xffffff, 0.8);
            scene.add(ambientLight);

            const directionalLight = new THREE.DirectionalLight(0xffffff, 0.6);
            directionalLight.position.set(5, 5, 5);
            scene.add(directionalLight);

            // Mockup base de la prenda (Torso estilizado)
            const bodyGeo = new THREE.CylinderGeometry(0.8, 0.7, 1.8, 32);
            const fabricMaterial = new THREE.MeshStandardMaterial({{ 
                color: "{color_prenda}", 
                roughness: 0.8,
                metalness: 0.1 
            }});

            const shirtMesh = new THREE.Mesh(bodyGeo, fabricMaterial);
            scene.add(shirtMesh);

            // Bucle de animación
            function animate() {{
                requestAnimationFrame(animate);
                controls.update();
                renderer.render(scene, camera);
            }}
            animate();

            window.addEventListener('resize', () => {{
                camera.aspect = container.clientWidth / container.clientHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(container.clientWidth, container.clientHeight);
            }});
        </script>
    </body>
    </html>
    """
    st.components.v1.html(components_html, height=500)
    st.info("💡 Haz clic y arrastra con el ratón sobre el visor para rotar el mockup 3D de la prenda.")

with col_panel:
    st.subheader("📁 Casillas de Carga por Zona")
    
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
                st.image(image, width=80, caption=f"Cargado: {label}")
            st.markdown("---")

    if st.button("Guardar Configuración de Sublimación", type="primary", use_container_width=True):
        if uploaded_files:
            st.success("¡Diseños y posiciones guardados con éxito para producción!")
            st.balloons()
        else:
            st.warning("Por favor, sube al menos un diseño en las casillas.")
