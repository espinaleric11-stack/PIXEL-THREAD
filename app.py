import streamlit as st
from PIL import Image
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Pixel Thread - Portal Profesional", layout="centered")

# --- ACTUALIZACIÓN AUTOMÁTICA CADA 2 SEGUNDOS ---
st_autorefresh(interval=2000, limit=None, key="autorefresh_global")

# --- INICIALIZAR DATOS GLOBALES EN LA SESIÓN ---
if "logos" not in st.session_state or "imagen_obj" not in st.session_state.logos[0]:
    st.session_state.logos = [
        {"id": 1, "cliente": "Cliente A", "nombre": "Logo León Dorado", "precio_usd": 5.0, "precio_dop": 300.0, "estado": "Pendiente", "pago": "Pendiente", "tipo": "Tela", "ubicacion_gorra": "N/A", "detalle_gorra": "N/A", "comentario": "Urgente", "archivo": "leon.png", "imagen_obj": None},
        {"id": 2, "cliente": "Cliente A", "nombre": "Logo Cafetería", "precio_usd": 5.0, "precio_dop": 300.0, "estado": "En Revisión", "pago": "Pendiente", "tipo": "Gorra", "ubicacion_gorra": "Frontal", "detalle_gorra": "3D (Puff)", "comentario": "Centrado", "archivo": "cafe.png", "imagen_obj": None},
        {"id": 3, "cliente": "Cliente B", "nombre": "Escudo Deportivo", "precio_usd": 5.0, "precio_dop": 300.0, "estado": "Terminado", "pago": "Pagado", "tipo": "Tela", "ubicacion_gorra": "N/A", "detalle_gorra": "N/A", "comentario": "Ninguno", "archivo": "escudo.png", "imagen_obj": None},
    ]

# Control de estado para el formulario
if "form_enviado" not in st.session_state:
    st.session_state.form_enviado = False

# --- MENÚ DE NAVEGACIÓN RÁPIDA ---
st.sidebar.title("Pixel Thread 🧵")
modo = st.sidebar.radio("Selecciona la Vista:", ["Panel Administrador (Tú)", "Portal Cliente A", "Portal Cliente B"])

st.sidebar.divider()
st.sidebar.info("💡 Tarifa oficial: $5.00 USD / $300.00 DOP por logo digitalizado.")
st.sidebar.caption("🔄 Actualización automática activa (cada 2 seg)")

# ==========================================
# 1. VISTA ADMINISTRADOR
# ==========================================
if modo == "Panel Administrador (Tú)":
    st.title("🎛️ Panel de Control - Pixel Thread")
    st.write("Administra el flujo de trabajo industrial, el estado de pagos y la entrega de archivos de bordado (.DST/.EMB).")

    total_usd = sum(l.get('precio_usd', 5.0) for l in st.session_state.logos if l['pago'] == "Pagado")
    total_dop = sum(l.get('precio_dop', 300.0) for l in st.session_state.logos if l['pago'] == "Pagado")
    
    col1, col2 = st.columns(2)
    col1.metric("Ingresos Cobrados (USD)", f"${total_usd:.2f} USD")
    col2.metric("Ingresos Cobrados (DOP)", f"RD$ {total_dop:,.2f}")

    st.divider()

    # Organizar listas: Pendientes/En revisión/En progreso arriba, terminados abajo
    logos_por_hacer = [l for l in st.session_state.logos if l['estado'] != "Terminado"]
    logos_terminados = [l for l in st.session_state.logos if l['estado'] == "Terminado"]
    logos_ordenados_admin = logos_por_hacer + logos_terminados

    st.subheader("📋 Gestión de Trabajos")

    for logo in logos_ordenados_admin:
        i = st.session_state.logos.index(logo)
        
        with st.container():
            col_img, col_info = st.columns([1, 3])
            
            with col_img:
                if logo.get('imagen_obj') is not None:
                    st.image(logo['imagen_obj'], caption="Diseño Original", width=100)
                else:
                    st.info("Sin miniatura")

            with col_info:
                st.markdown(f"### 🧵 {logo['nombre']} *({logo['cliente']})*")
                st.write(f"**Tipo:** {logo.get('tipo', 'Tela')} | **Ubicación:** {logo.get('ubicacion_gorra', 'N/A')} | **Estilo:** {logo.get('detalle_gorra', 'N/A')}")
                st.write(f"**Comentario:** {logo.get('comentario', 'Ninguno')}")
                st.write(f"**Archivo cliente:** `📁 {logo.get('archivo', 'Sin archivo')}`")
                st.write(f"**Precio:** ${logo.get('precio_usd', 5.0):.2f} USD / RD${logo.get('precio_dop', 300.0):.2f}")
            
            estado_actual = logo['estado']
            
            # --- CONTROLES DE ESTADO PROFESIONAL ---
            c1, c2, c3 = st.columns(3)
            
            if estado_actual == "Pendiente":
                if c1.button("🔍 Pasar a Revisión", key=f"rev_{logo['id']}"):
                    st.session_state.logos[i]['estado'] = "En Revisión"
                    st.rerun()
            elif estado_actual == "En Revisión":
                c1.info("🔍 En Revisión")
                if c2.button("▶ Iniciar (Luz Verde)", key=f"iniciar_{logo['id']}"):
                    st.session_state.logos[i]['estado'] = "En Progreso"
                    st.rerun()
            elif estado_actual == "En Progreso":
                c1.warning("🟢 En Progreso")
                if c2.button("✓ Marcar Terminado", key=f"terminar_{logo['id']}"):
                    st.session_state.logos[i]['estado'] = "Terminado"
                    st.rerun()
            else:
                c1.success("✅ Terminado")
                # Control de Estado de Pago
                pago_actual = logo.get('pago', 'Pendiente')
                nuevo_pago = c2.selectbox("Estado de Pago", ["Pendiente", "Pagado"], index=0 if pago_actual=="Pendiente" else 1, key=f"pago_{logo['id']}")
                if nuevo_pago != pago_actual:
                    st.session_state.logos[i]['pago'] = nuevo_pago
                    st.rerun()

            # Simulación de subida de archivo de bordado final (.dst / .emb) por parte del administrador
            with st.expander("📤 Subir archivo de bordado final (.DST / .EMB)"):
                archivo_bordado = st.file_uploader("Sube el archivo listo para bordar", type=["dst", "emb", "pes", "jef"], key=f"bordado_{logo['id']}")
                if archivo_bordado:
                    logo['archivo_bordado_nombre'] = archivo_bordado.name
                    logo['archivo_bordado_bytes'] = archivo_bordado.getvalue()
                    st.success(f"Archivo {archivo_bordado.name} guardado para descarga del cliente.")

            st.divider()

    if st.button("📄 Generar Corte Semanal"):
        st.success("¡Corte y reporte contable generado con éxito!")


# ==========================================
# FUNCIÓN GENÉRICA PARA EL PORTAL DE CLIENTES
# ==========================================
def render_portal_cliente(nombre_cliente):
    st.title(f"👤 Portal de Cliente: {nombre_cliente}")
    st.write("Bienvenido a Pixel Thread. Gestiona tus solicitudes y descarga tus archivos de bordado digitalizados.")
    
    divisa = st.radio("Selecciona tu moneda:", ["Dólares (USD - $)", "Pesos Dominicanos (DOP - RD$)"], horizontal=True, key=f"divisa_{nombre_cliente}")
    
    logos_cliente = [l for l in st.session_state.logos if l['cliente'] == nombre_cliente]
    
    if "Dólares" in divisa:
        total_cliente = sum(l.get('precio_usd', 5.0) for l in logos_cliente if l['pago'] == "Pagado")
        st.metric("Total Pagado (Semana)", f"${total_cliente:.2f} USD")
    else:
        total_cliente = sum(l.get('precio_dop', 300.0) for l in logos_cliente if l['pago'] == "Pagado")
        st.metric("Total Pagado (Semana)", f"RD$ {total_cliente:,.2f}")

    st.divider()

    # --- SECCIÓN PARA NUEVO PEDIDO ---
    with st.expander("➕ Enviar un Nuevo Logo a Digitalizar", expanded=not st.session_state.form_enviado):
        if st.session_state.form_enviado:
            st.success("✅ ¡ORDEN AGREGADA CORRECTAMENTE!")
            if st.button("Enviar otro diseño", key=f"otro_{nombre_cliente}"):
                st.session_state.form_enviado = False
                st.rerun()
        else:
            nombre_logo = st.text_input("Nombre del Logo / Diseño", key=f"inp_nom_{nombre_cliente}")
            archivo_subido = st.file_uploader("Sube tu archivo original (PNG, JPG, Vector)", type=["png", "jpg", "jpeg", "ai", "pdf"], key=f"inp_file_{nombre_cliente}")
            
            tipo_aplicacion = st.radio("¿Para qué tipo de soporte es el bordado?", ["Tela (Camisetas, Polos, etc.)", "Gorra"], key=f"tipo_app_{nombre_cliente}")
            
            ubicacion_gorra = "N/A"
            detalle_gorra = "N/A"
            
            if tipo_aplicacion == "Gorra":
                ubicacion_gorra = st.radio("Selecciona la ubicación en la gorra:", ["Frontal", "Trasero", "Lateral"], key=f"ubicacion_{nombre_cliente}")
                if ubicacion_gorra == "Frontal":
                    detalle_gorra = st.radio("Selecciona el estilo:", ["3D (Puff)", "Plano (Flat)"], key=f"detalle_{nombre_cliente}")
                else:
                    detalle_gorra = "Plano (Flat)"
            
            comentario_cliente = st.text_area("Comentarios o instrucciones especiales", key=f"inp_com_{nombre_cliente}")
            
            if st.button("Enviar Logo a Pixel Thread", key=f"btn_enviar_{nombre_cliente}"):
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
                        "pago": "Pendiente",
                        "tipo": tipo_aplicacion,
                        "ubicacion_gorra": ubicacion_gorra,
                        "detalle_gorra": detalle_gorra,
                        "comentario": comentario_cliente if comentario_cliente else "Ninguno",
                        "archivo": nombre_archivo,
                        "imagen_obj": img_obj
                    }
                    st.session_state.logos.append(nuevo_logo)
                    st.session_state.form_enviado = True
                    st.toast("¡Orden agregada con éxito!", icon="🎉")
                    st.rerun()
                else:
                    st.error("Por favor, ingresa un nombre para el logo.")

    # --- SEPARAR LISTAS CLIENTE: POR REALIZAR VS REALIZADOS ---
    logos_por_realizar = [l for l in logos_cliente if l['estado'] != "Terminado"]
    logos_realizados = [l for l in logos_cliente if l['estado'] == "Terminado"]

    st.subheader("⏳ Trabajos por Realizar")
    if not logos_por_realizar:
        st.info("No tienes trabajos pendientes actualmente.")

    for logo in logos_por_realizar:
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
        
        # Estado visual detallado
        if logo['estado'] == "Pendiente":
            st.info("⏳ Estado: Recibido / En espera de revisión")
            col_mod, col_elim = st.columns(2)
            with col_mod:
                with st.popover("✏️ Modificar Orden"):
                    with st.form(key=f"edit_form_{logo['id']}"):
                        nuevo_nombre = st.text_input("Nuevo nombre", value=logo['nombre'])
                        nuevo_comentario = st.text_area("Nuevas notas", value=logo['comentario'])
                        if st.form_submit_button("Guardar Cambios"):
                            logo['nombre'] = nuevo_nombre
                            logo['comentario'] = nuevo_comentario
                            st.success("¡Modificado!")
                            st.rerun()
            with col_elim:
                if st.button("🗑️ Eliminar", key=f"del_{logo['id']}"):
                    st.session_state.logos.remove(logo)
                    st.warning("Orden eliminada.")
                    st.rerun()
        elif logo['estado'] == "En Revisión":
            st.info("🔍 Estado: Verificando calidad del archivo para digitalización")
        elif logo['estado'] == "En Progreso":
            st.markdown(
                """
                <div style="background-color: #d1fae5; border-left: 6px solid #10b981; padding: 10px; border-radius: 5px; color: #065f46; font-weight: bold;">
                    🟢 ¡DIGITALIZANDO EN PROGRESO! (Bloqueado para cambios)
                </div>
                """, 
                unsafe_allow_html=True
            )
        
        precio_mostrar = f"${logo.get('precio_usd', 5.0):.2f} USD" if "Dólares" in divisa else f"RD$ {logo.get('precio_dop', 300.0):.2f} DOP"
        st.write(f"Precio estimado: **{precio_mostrar}**")
        st.divider()

    # TRABAJOS REALIZADOS E HISTORIAL CON DESCARGA DE ARCHIVO BORDADO
    if logos_realizados:
        st.subheader("✅ Trabajos Realizados y Descargas")
        for logo in logos_realizados:
            col_img, col_info = st.columns([1, 3])
            with col_img:
                if logo.get('imagen_obj') is not None:
                    st.image(logo['imagen_obj'], caption="Diseño", width=100)
                else:
                    st.info("Sin miniatura")
                    
            with col_info:
                st.markdown(f"### 🧵 {logo['nombre']}")
                st.write(f"**Aplicación:** {logo.get('tipo', 'Tela')} | **Ubicación:** {logo.get('ubicacion_gorra', 'N/A')} | **Estilo:** {logo.get('detalle_gorra', 'N/A')}")
                st.write(f"**Notas:** {logo.get('comentario', 'Ninguno')}")
            
            st.success("✅ Estado: Digitalización Finalizada")
            
            # Área de descarga del archivo de máquina de bordar
            if 'archivo_bordado_bytes' in logo and logo['archivo_bordado_bytes']:
                st.download_button(
                    label=f"⬇️ Descargar Archivo Listo: {logo.get('archivo_bordado_nombre', 'bordado.dst')}",
                    data=logo['archivo_bordado_bytes'],
                    file_name=logo.get('archivo_bordado_nombre', 'bordado.dst'),
                    mime="application/octet-stream",
                    key=f"dl_{logo['id']}"
                )
            else:
                st.info("📁 El archivo de bordado estará disponible para descarga en breve.")
            
            precio_mostrar = f"${logo.get('precio_usd', 5.0):.2f} USD" if "Dólares" in divisa else f"RD$ {logo.get('precio_dop', 300.0):.2f} DOP"
            st.write(f"Precio final: **{precio_mostrar}** | Pago: **{logo.get('pago', 'Pendiente')}**")
            st.divider()


# ==========================================
# 2. VISTAS DE CLIENTES
# ==========================================
if modo == "Panel Administrador (Tú)":
    pass # Ya renderizado arriba
elif modo == "Portal Cliente A":
    render_portal_cliente("Cliente A")
elif modo == "Portal Cliente B":
    render_portal_cliente("Cliente B")
