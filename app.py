import streamlit as st
from PIL import Image
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Pixel Thread - Portal de Clientes", layout="centered")

# --- ACTUALIZACIÓN AUTOMÁTICA CADA 2 SEGUNDOS ---
st_autorefresh(interval=2000, limit=None, key="autorefresh_global")

# --- INICIALIZAR DATOS GLOBALES EN LA SESIÓN ---
if "logos" not in st.session_state or "imagen_obj" not in st.session_state.logos[0]:
    st.session_state.logos = [
        {"id": 1, "cliente": "Cliente A", "nombre": "Logo León Dorado", "precio_usd": 5.0, "precio_dop": 300.0, "estado": "Pendiente", "tipo": "Tela", "ubicacion_gorra": "N/A", "detalle_gorra": "N/A", "comentario": "Urgente", "archivo": "leon.png", "imagen_obj": None},
        {"id": 2, "cliente": "Cliente A", "nombre": "Logo Cafetería", "precio_usd": 5.0, "precio_dop": 300.0, "estado": "Pendiente", "tipo": "Gorra", "ubicacion_gorra": "Frontal", "detalle_gorra": "3D (Puff)", "comentario": "Centrado", "archivo": "cafe.png", "imagen_obj": None},
        {"id": 3, "cliente": "Cliente B", "nombre": "Escudo Deportivo", "precio_usd": 5.0, "precio_dop": 300.0, "estado": "Pendiente", "tipo": "Tela", "ubicacion_gorra": "N/A", "detalle_gorra": "N/A", "comentario": "Ninguno", "archivo": "escudo.png", "imagen_obj": None},
    ]

# --- MENÚ DE NAVEGACIÓN RÁPIDA (Simulador de vistas) ---
st.sidebar.title("Pixel Thread 🧵")
modo = st.sidebar.radio("Selecciona la Vista:", ["Panel Administrador (Tú)", "Portal Cliente A", "Portal Cliente B"])

st.sidebar.divider()
st.sidebar.info("💡 Tarifa oficial: $5.00 USD / $300.00 DOP por logo digitalizado.")
st.sidebar.caption("🔄 Actualización automática activa (cada 2 seg)")

# ==========================================
# 1. VISTA ADMINISTRADOR (Tú controlas todo)
# ==========================================
if modo == "Panel Administrador (Tú)":
    st.title("🎛️ Panel de Control - Pixel Thread")
    st.write("Gestiona el estado de los logos. Al marcar un logo como **En Progreso**, se encenderá la luz verde y se bloquearán las opciones para el cliente.")

    total_usd = sum(l.get('precio_usd', 5.0) for l in st.session_state.logos if l['estado'] == "Terminado")
    total_dop = sum(l.get('precio_dop', 300.0) for l in st.session_state.logos if l['estado'] == "Terminado")
    
    col1, col2 = st.columns(2)
    col1.metric("Total Facturable (USD)", f"${total_usd:.2f} USD")
    col2.metric("Total Facturable (DOP)", f"RD$ {total_dop:,.2f}")

    st.divider()
    st.subheader("Lista de Todos los Trabajos")

    for i, logo in enumerate(st.session_state.logos):
        with st.container():
            col_img, col_info = st.columns([1, 3])
            
            with col_img:
                if logo.get('imagen_obj') is not None:
                    st.image(logo['imagen_obj'], caption="Miniatura", width=100)
                else:
                    st.info("Sin miniatura visual")

            with col_info:
                st.markdown(f"### 🧵 {logo['nombre']} *({logo['cliente']})*")
                st.write(f"**Tipo:** {logo.get('tipo', 'Tela')} | **Ubicación:** {logo.get('ubicacion_gorra', 'N/A')} | **Estilo:** {logo.get('detalle_gorra', 'N/A')}")
                st.write(f"**Comentario:** {logo.get('comentario', 'Ninguno')}")
                st.write(f"**Archivo:** `📁 {logo.get('archivo', 'Sin archivo')}`")
                st.write(f"**Precio:** ${logo.get('precio_usd', 5.0):.2f} USD / RD${logo.get('precio_dop', 300.0):.2f}")
            
            estado_actual = logo['estado']
            
            c1, c2 = st.columns(2)
            if estado_actual == "Pendiente":
                if c1.button("▶ Iniciar (Luz Verde)", key=f"iniciar_{i}"):
                    st.session_state.logos[i]['estado'] = "En Progreso"
                    st.rerun()
            elif estado_actual == "En Progreso":
                c1.warning("🟢 En Progreso (Bloqueado para el cliente)")
                if c2.button("✓ Terminar", key=f"terminar_{i}"):
                    st.session_state.logos[i]['estado'] = "Terminado"
                    st.rerun()
            else:
                c1.success("✅ Completado / Agregado a factura")

            st.divider()

    if st.button("📄 Simular Corte y Factura de Lunes"):
        st.success("¡Corte semanal generado con éxito!")
        st.write(f"**Total a cobrar esta semana:** ${total_usd:.2f} USD (RD$ {total_dop:,.2f} DOP)")


# ==========================================
# FUNCIÓN GENÉRICA PARA EL PORTAL DE CLIENTES
# ==========================================
def render_portal_cliente(nombre_cliente):
    st.title(f"👤 Portal de Cliente: {nombre_cliente}")
    st.write("Bienvenido a Pixel Thread. Sube tus diseños y consulta el estado de tus digitalizaciones en tiempo real.")
    
    divisa = st.radio("Selecciona tu moneda de preferencia:", ["Dólares (USD - $)", "Pesos Dominicanos (DOP - RD$)"], horizontal=True, key=f"divisa_{nombre_cliente}")
    
    logos_cliente = [l for l in st.session_state.logos if l['cliente'] == nombre_cliente]
    
    if "Dólares" in divisa:
        total_cliente = sum(l.get('precio_usd', 5.0) for l in logos_cliente if l['estado'] == "Terminado")
        st.metric("Tu Acumulado Actual (Semana)", f"${total_cliente:.2f} USD")
    else:
        total_cliente = sum(l.get('precio_dop', 300.0) for l in logos_cliente if l['estado'] == "Terminado")
        st.metric("Tu Acumulado Actual (Semana)", f"RD$ {total_cliente:,.2f}")

    st.divider()

    # --- SECCIÓN PARA NUEVO PEDIDO ---
    with st.expander("➕ Enviar un Nuevo Logo a Digitalizar"):
        with st.form(key=f"form_{nombre_cliente}"):
            nombre_logo = st.text_input("Nombre del Logo / Diseño")
            archivo_subido = st.file_uploader("Sube tu archivo de imagen (PNG, JPG)", type=["png", "jpg", "jpeg"])
            
            tipo_aplicacion = st.radio("¿Para qué tipo de soporte es el bordado?", ["Tela (Camisetas, Polos, etc.)", "Gorra"], key=f"tipo_app_{nombre_cliente}")
            
            ubicacion_gorra = "N/A"
            detalle_gorra = "N/A"
            
            if tipo_aplicacion == "Gorra":
                ubicacion_gorra = st.radio("Selecciona la ubicación en la gorra:", ["Frontal", "Trasero", "Lateral"], key=f"ubicacion_{nombre_cliente}")
                
                if ubicacion_gorra == "Frontal":
                    detalle_gorra = st.radio("Selecciona el estilo:", ["3D (Puff)", "Plano (Flat)"], key=f"detalle_{nombre_cliente}")
                else:
                    detalle_gorra = "Plano (Flat)"
            
            comentario_cliente = st.text_area("Comentarios o instrucciones adicionales (opcional)")
            
            submitted = st.form_submit_button("Enviar Logo a Pixel Thread")
            if submitted:
                if nombre_logo:
                    nombre_archivo = archivo_subido.name if archivo_subido else "Sin archivo adjunto"
                    
                    img_obj = None
                    if archivo_subido is not None:
                        try:
                            img_obj = Image.open(archivo_subido)
                        except Exception:
                            pass

                    nuevo_logo = {
                        "id": len(st.session_state.logos) + 1,
                        "cliente": nombre_cliente,
                        "nombre": nombre_logo,
                        "precio_usd": 5.0,
                        "precio_dop": 300.0,
                        "estado": "Pendiente",
                        "tipo": tipo_aplicacion,
                        "ubicacion_gorra": ubicacion_gorra,
                        "detalle_gorra": detalle_gorra,
                        "comentario": comentario_cliente if comentario_cliente else "Ninguno",
                        "archivo": nombre_archivo,
                        "imagen_obj": img_obj
                    }
                    st.session_state.logos.append(nuevo_logo)
                    st.success("¡Logo enviado exitosamente!")
                    st.rerun()
                else:
                    st.error("Por favor, ingresa un nombre para el logo.")

    st.subheader("📋 Tus Trabajos Activos e Historial")

    if not logos_cliente:
        st.info("No tienes logos registrados actualmente.")

    for logo in logos_cliente:
        col_img, col_info = st.columns([1, 3])
        
        with col_img:
            if logo.get('imagen_obj') is not None:
                st.image(logo['imagen_obj'], caption="Tu Diseño", width=100)
            else:
                st.info("Sin miniatura")
                
        with col_info:
            st.markdown(f"### 🧵 {logo['nombre']}")
            st.write(f"**Aplicación:** {logo.get('tipo', 'Tela')} | **Ubicación:** {logo.get('ubicacion_gorra', 'N/A')} | **Estilo:** {logo.get('detalle_gorra', 'N/A')}")
            st.write(f"**Tus notas:** {logo.get('comentario', 'Ninguno')}")
            st.write(f"**Archivo:** `📁 {logo.get('archivo', 'N/A')}`")
        
        # MOSTRAR ESTADO Y LUZ VERDE
        if logo['estado'] == "Pendiente":
            st.info("⏳ Estado: En espera de turno")
            
            # --- OPCIONES DE MODIFICAR O ELIMINAR (SOLO SI ESTÁ PENDIENTE) ---
            col_mod, col_elim = st.columns(2)
            
            with col_mod:
                with st.popover("✏️ Modificar Orden"):
                    with st.form(key=f"edit_form_{logo['id']}"):
                        nuevo_nombre = st.text_input("Nuevo nombre", value=logo['nombre'])
                        nuevo_comentario = st.text_area("Nuevas notas", value=logo['comentario'])
                        btn_guardar = st.form_submit_button("Guardar Cambios")
                        if btn_guardar:
                            logo['nombre'] = nuevo_nombre
                            logo['comentario'] = nuevo_comentario
                            st.success("¡Orden modificada con éxito!")
                            st.rerun()
            
            with col_elim:
                if st.button("🗑️ Eliminar Orden", key=f"del_{logo['id']}"):
                    st.session_state.logos.remove(logo)
                    st.warning("Orden eliminada.")
                    st.rerun()
                    
        elif logo['estado'] == "En Progreso":
            # LA LUZ VERDE SOLICITADA (BLOQUEA MODIFICAR/ELIMINAR)
            st.markdown(
                """
                <div style="background-color: #d1fae5; border-left: 6px solid #10b981; padding: 10px; border-radius: 5px; color: #065f46; font-weight: bold;">
                    🟢 ¡TRABAJANDO EN ESTE LOGO! (En Progreso - No se puede modificar ni eliminar)
                </div>
                """, 
                unsafe_allow_html=True
            )
        else:
            st.success("✅ Estado: Logo Terminado / Agregado a la factura")
        
        precio_mostrar = f"${logo.get('precio_usd', 5.0):.2f} USD" if "Dólares" in divisa else f"RD$ {logo.get('precio_dop', 300.0):.2f} DOP"
        st.write(f"Precio unitario: **{precio_mostrar}**")
        st.divider()


# ==========================================
# 2. VISTAS DE CLIENTES
# ==========================================
if modo == "Portal Cliente A":
    render_portal_cliente("Cliente A")
elif modo == "Portal Cliente B":
    render_portal_cliente("Cliente B")
