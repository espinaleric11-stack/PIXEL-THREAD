import streamlit as st
from PIL import Image
from streamlit_autorefresh import st_autorefresh
from datetime import datetime

st.set_page_config(page_title="Pixel Thread - Portal Profesional", layout="centered")

# --- ACTUALIZACIÓN AUTOMÁTICA CADA 2 SEGUNDOS ---
st_autorefresh(interval=2000, limit=None, key="autorefresh_global")

# --- INICIALIZAR LISTA DE CLIENTES Y DIVISAS ---
if "clientes_registrados" not in st.session_state:
    st.session_state.clientes_registrados = {
        "Cliente A": "Dólares (USD - $)",
        "Cliente B": "Pesos Dominicanos (DOP - RD$)"
    }

# --- CONTROL DE SESIÓN DE CLIENTE (SOLO POR USUARIO) ---
if "cliente_logeado" not in st.session_state:
    st.session_state.cliente_logeado = None

# --- INICIALIZAR DATOS GLOBALES EN LA SESIÓN ---
if "logos" not in st.session_state or not st.session_state.logos or "pago" not in st.session_state.logos[0]:
    st.session_state.logos = [
        {"id": 1, "cliente": "Cliente A", "nombre": "Logo León Dorado", "precio_usd": 5.0, "precio_dop": 300.0, "estado": "Pendiente", "pago": "Pendiente", "tipo": "Tela", "ubicacion_gorra": "N/A", "detalle_gorra": "N/A", "posicion_logo": "Pecho Izquierdo", "comentario": "Urgente", "archivo": "leon.png", "imagen_obj": None},
        {"id": 2, "cliente": "Cliente A", "nombre": "Logo Cafetería", "precio_usd": 5.0, "precio_dop": 300.0, "estado": "En Revisión", "pago": "Pendiente", "tipo": "Gorra", "ubicacion_gorra": "Frontal", "detalle_gorra": "3D (Puff)", "posicion_logo": "Frontal", "comentario": "Centrado", "archivo": "cafe.png", "imagen_obj": None},
        {"id": 3, "cliente": "Cliente B", "nombre": "Escudo Deportivo", "precio_usd": 5.0, "precio_dop": 300.0, "estado": "Terminado", "pago": "Pagado", "tipo": "Tela", "ubicacion_gorra": "N/A", "detalle_gorra": "N/A", "posicion_logo": "Espalda", "comentario": "Ninguno", "archivo": "escudo.png", "imagen_obj": None},
    ]

if "recibos_pago" not in st.session_state:
    st.session_state.recibos_pago = {}

if "form_enviado" not in st.session_state:
    st.session_state.form_enviado = False

# --- MENÚ DE NAVEGACIÓN RÁPIDA ---
st.sidebar.title("Pixel Thread 🧵")
modo = st.sidebar.radio("Selecciona el Modo:", ["Panel Administrador (Tú)", "Portal de Clientes"])

st.sidebar.divider()
st.sidebar.info("💡 Tarifa oficial: $5.00 USD / $300.00 DOP por logo digitalizado.")
st.sidebar.caption("🔄 Actualización automática activa (cada 2 seg)")

# ==========================================
# 1. VISTA ADMINISTRADOR
# ==========================================
if modo == "Panel Administrador (Tú)":
    st.title("🎛️ Panel de Control - Pixel Thread")
    st.write("Administra el flujo de trabajo industrial, el estado de pagos y la entrega de archivos de bordado (.DST/.EMB/.PDF).")

    total_usd = sum(l.get('precio_usd', 5.0) for l in st.session_state.logos if l.get('pago', 'Pendiente') == "Pagado")
    total_dop = sum(l.get('precio_dop', 300.0) for l in st.session_state.logos if l.get('pago', 'Pendiente') == "Pagado")
    
    col1, col2 = st.columns(2)
    col1.metric("Ingresos Cobrados (USD)", f"${total_usd:.2f} USD")
    col2.metric("Ingresos Cobrados (DOP)", f"RD$ {total_dop:,.2f}")

    st.divider()

    # --- SECCIÓN PRINCIPAL: AGREGAR NUEVOS CLIENTES ---
    st.subheader("➕ Registrar Nuevo Cliente y su Moneda")
    with st.form(key="form_nuevo_cliente"):
        col_nc1, col_nc2 = st.columns(2)
        with col_nc1:
            nuevo_nombre_cli = st.text_input("Nombre de Usuario / Cliente")
        with col_nc2:
            nueva_divisa_cli = st.selectbox("Moneda Principal", ["Dólares (USD - $)", "Pesos Dominicanos (DOP - RD$)"])
        
        btn_crear_cli = st.form_submit_button("Registrar Cliente")
        if btn_crear_cli:
            if nuevo_nombre_cli:
                usuario_limpio = nuevo_nombre_cli.strip()
                if usuario_limpio in st.session_state.clientes_registrados:
                    st.error("¡Este usuario ya está registrado!")
                else:
                    st.session_state.clientes_registrados[usuario_limpio] = nueva_divisa_cli
                    st.success(f"¡Cliente '{usuario_limpio}' registrado con éxito y habilitado para entrar!")
                    st.rerun()
            else:
                st.error("Por favor, ingresa un nombre para el cliente.")

    st.divider()

    # --- SECCIÓN DE CONTROL Y REINICIO POR CLIENTE ---
    st.subheader("👥 Control y Cierre de Ciclo por Cliente")
    for cli in st.session_state.clientes_registrados.keys():
        logos_cli_term = [l for l in st.session_state.logos if l.get('cliente') == cli and l.get('estado', 'Pendiente') == "Terminado"]
        sub_usd = sum(l.get('precio_usd', 5.0) for l in logos_cli_term)
        sub_dop = sum(l.get('precio_dop', 300.0) for l in logos_cli_term)
        
        with st.expander(f"👤 Cliente: {cli} — Acumulado Terminado: ${sub_usd:.2f} USD / RD$ {sub_dop:,.2f}"):
            c_info, c_btn = st.columns([2, 1])
            with c_info:
                st.write(f"Trabajos terminados pendientes de cerrar ciclo: **{len(logos_cli_term)}**")
            with c_btn:
                if st.button(f"🔄 Reiniciar Ciclo de {cli}", key=f"reset_cli_{cli}"):
                    for logo in st.session_state.logos:
                        if logo.get('cliente') == cli and logo.get('estado', 'Pendiente') == "Terminado":
                            logo['pago'] = "Pagado"
                            logo['estado'] = "Archivado/Pagado"
                    st.success(f"¡Ciclo de {cli} reiniciado con éxito!")
                    st.rerun()

    st.divider()

    # --- SECCIÓN DE RECIBOS DE PAGO ENVIADOS POR CLIENTES ---
    st.subheader("🧾 Recibos de Pago Subidos por Clientes")
    if st.session_state.recibos_pago:
        for cli, recibo_info in st.session_state.recibos_pago.items():
            with st.expander(f"📥 Ver Recibo de Pago de: {cli} ({recibo_info['nombre_archivo']})"):
                st.download_button(
                    label=f"Descargar comprobante de {cli}",
                    data=recibo_info['bytes'],
                    file_name=recibo_info['nombre_archivo'],
                    mime="application/octet-stream",
                    key=f"dl_recibo_{cli}"
                )
    else:
        st.info("No hay recibos de pago subidos por los clientes todavía.")

    st.divider()

    logos_activos_admin = [l for l in st.session_state.logos if l.get('estado') != "Archivado/Pagado"]
    logos_por_hacer = [l for l in logos_activos_admin if l.get('estado', 'Pendiente') != "Terminado"]
    logos_terminados = [l for l in logos_activos_admin if l.get('estado', 'Pendiente') == "Terminado"]
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
                st.markdown(f"### 🧵 {logo.get('nombre', 'Sin nombre')} *({logo.get('cliente', 'Cliente')})*")
                st.write(f"**Tipo:** {logo.get('tipo', 'Tela')} | **Posición:** {logo.get('posicion_logo', 'No especificada')} | **Ubicación Gorra:** {logo.get('ubicacion_gorra', 'N/A')} ({logo.get('detalle_gorra', 'N/A')})")
                st.write(f"**Comentario:** {logo.get('comentario', 'Ninguno')}")
                st.write(f"**Archivo cliente:** `📁 {logo.get('archivo', 'Sin archivo')}`")
                st.write(f"**Precio:** ${logo.get('precio_usd', 5.0):.2f} USD / RD${logo.get('precio_dop', 300.0):.2f}")
            
            estado_actual = logo.get('estado', 'Pendiente')
            
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
                pago_actual = logo.get('pago', 'Pendiente')
                nuevo_pago = c2.selectbox("Estado de Pago", ["Pendiente", "Pagado"], index=0 if pago_actual=="Pendiente" else 1, key=f"pago_{logo['id']}")
                if nuevo_pago != pago_actual:
                    st.session_state.logos[i]['pago'] = nuevo_pago
                    st.rerun()

            with st.expander("📤 Subir múltiples archivos de bordado (.DST / .EMB / .PDF)"):
                archivos_bordado = st.file_uploader(
                    "Sube los archivos listos para bordar", 
                    type=["dst", "emb", "pes", "jef", "pdf"], 
                    accept_multiple_files=True, 
                    key=f"bordado_{logo['id']}"
                )
                if archivos_bordado:
                    logo['archivos_multiples'] = [{"nombre": f.name, "bytes": f.getvalue()} for f in archivos_bordado]
                    nombres_str = ", ".join([f.name for f in archivos_bordado])
                    st.success(f"Archivos guardados correctamente: {nombres_str}")

            st.divider()


# ==========================================
# 2. PORTAL DE CLIENTES (SOLO ACCESO CON USUARIOS CREADOS POR EL ADMIN)
# ==========================================
elif modo == "Portal de Clientes":
    
    if st.session_state.cliente_logeado is None:
        st.title("👤 Portal de Clientes - Pixel Thread")
        st.write("Ingresa tu nombre de usuario autorizado para acceder a tu portal:")
        
        with st.form(key="form_login_cliente"):
            usuario_ingresado = st.text_input("Tu Nombre de Usuario")
            btn_entrar = st.form_submit_button("Entrar a mi Portal")
            
            if btn_entrar:
                usuario_limpio = usuario_ingresado.strip()
                # Verificar si el usuario existe en los registros creados por el administrador
                if usuario_limpio in st.session_state.clientes_registrados:
                    st.session_state.cliente_logeado = usuario_limpio
                    st.success(f"¡Bienvenido, {usuario_limpio}!")
                    st.rerun()
                else:
                    st.error("❌ Este usuario no está registrado o autorizado. Por favor, comunícate con el administrador para que cree tu cuenta.")
    
    else:
        nombre_cliente = st.session_state.cliente_logeado
        
        col_title, col_logout = st.columns([3, 1])
        with col_title:
            st.title(f"👤 Portal Privado de: {nombre_cliente}")
        with col_logout:
            st.write("")
            if st.button("🚪 Cerrar Sesión"):
                st.session_state.cliente_logeado = None
                st.rerun()

        st.write("Gestiona tus solicitudes de bordado y descarga tus archivos finalizados de manera segura.")
        
        divisa_default = st.session_state.clientes_registrados.get(nombre_cliente, "Dólares (USD - $)")
        divisa = st.radio("Selecciona tu moneda:", ["Dólares (USD - $)", "Pesos Dominicanos (DOP - RD$)"], index=0 if "Dólares" in divisa_default else 1, horizontal=True, key=f"divisa_{nombre_cliente}")
        
        logos_cliente = [l for l in st.session_state.logos if l.get('cliente') == nombre_cliente and l.get('estado') != "Archivado/Pagado"]
        
        col_metrica, col_recibo = st.columns(2)

        with col_metrica:
            if "Dólares" in divisa:
                total_cliente = sum(l.get('precio_usd', 5.0) for l in logos_cliente if l.get('estado', 'Pendiente') == "Terminado")
                st.metric("Total Acumulado (Semana)", f"${total_cliente:.2f} USD")
            else:
                total_cliente = sum(l.get('precio_dop', 300.0) for l in logos_cliente if l.get('estado', 'Pendiente') == "Terminado")
                st.metric("Total Acumulado (Semana)", f"RD$ {total_cliente:,.2f}")

        with col_recibo:
            st.write("🧾 **Subir Recibo de Pago**")
            recibo_subido = st.file_uploader("Sube tu comprobante", type=["png", "jpg", "jpeg", "pdf"], key=f"recibo_file_{nombre_cliente}")
            if recibo_subido:
                st.session_state.recibos_pago[nombre_cliente] = {
                    "nombre_archivo": recibo_subido.name,
                    "bytes": recibo_subido.getvalue()
                }
                st.success("¡Recibo enviado al administrador con éxito!")

        st.divider()

        with st.expander("➕ Enviar un Nuevo Logo a Digitalizar", expanded=not st.session_state.form_enviado):
            if st.session_state.form_enviado:
                st.success("✅ ¡ORDEN AGREGADA CORRECTAMENTE!")
                if st.button("Enviar otro diseño", key=f"otro_{nombre_cliente}"):
                    st.session_state.form_enviado = False
                    st.rerun()
            else:
                nombre_logo = st.text_input("Nombre del Logo / Diseño", key=f"inp_nom_{nombre_cliente}")
                
                archivos_subidos = st.file_uploader(
                    "Sube tus archivos originales (puedes seleccionar varios a la vez)", 
                    type=["png", "jpg", "jpeg", "ai", "pdf"], 
                    accept_multiple_files=True, 
                    key=f"inp_file_{nombre_cliente}"
                )
                
                tipo_aplicacion = st.radio("¿Para qué tipo de soporte es el bordado?", ["Tela (Camisetas, Polos, etc.)", "Gorra"], key=f"tipo_app_{nombre_cliente}")
                
                posicion_logo = st.selectbox(
                    "Posición del logo en la prenda:", 
                    ["Pecho Izquierdo", "Pecho Derecho", "Centro Pecho", "Espalda Alta", "Espalda Centro", "Manga Izquierda", "Manga Derecha", "Gorra Frontal", "Gorra Lateral", "Gorra Trasera", "Otra posición"],
                    key=f"posicion_{nombre_cliente}"
                )
                
                ubicacion_gorra = "N/A"
                detalle_gorra = "N/A"
                
                if tipo_aplicacion == "Gorra":
                    ubicacion_gorra = st.radio("Selecciona la ubicación específica en la gorra:", ["Frontal", "Trasero", "Lateral"], key=f"ubicacion_{nombre_cliente}")
                    if ubicacion_gorra == "Frontal":
                        detalle_gorra = st.radio("Selecciona el estilo:", ["3D (Puff)", "Plano (Flat)"], key=f"detalle_{nombre_cliente}")
                    else:
                        detalle_gorra = "Plano (Flat)"
                
                comentario_cliente = st.text_area("Comentarios o instrucciones especiales", key=f"inp_com_{nombre_cliente}")
                
                if st.button("Enviar Logo a Pixel Thread", key=f"btn_enviar_{nombre_cliente}"):
                    if nombre_logo:
                        nombre_archivo = ", ".join([f.name for f in archivos_subidos]) if archivos_subidos else "Sin archivo adjunto"
                        img_obj = None
                        if archivos_subidos:
                            try:
                                img_obj = Image.open(archivos_subidos[0])
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
                            "posicion_logo": posicion_logo,
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

        logos_por_realizar = [l for l in logos_cliente if l.get('estado', 'Pendiente') != "Terminado"]
        
        st.subheader("⏳ Trabajos por Realizar y Turno en Cola")
        if not logos_por_realizar:
            st.info("No tienes trabajos pendientes actualmente.")

        cola_global_activa = [l for l in st.session_state.logos if l.get('estado', 'Pendiente') != "Terminado" and l.get('estado') != "Archivado/Pagado"]

        for logo in logos_por_realizar:
            if logo in cola_global_activa:
                posicion_en_cola = cola_global_activa.index(logo) + 1
            else:
                posicion_en_cola = "?"

            col_img, col_info = st.columns([1, 3])
            with col_img:
                if logo.get('imagen_obj') is not None:
                    st.image(logo['imagen_obj'], caption="Tu Diseño", width=100)
                else:
                    st.info("Sin miniatura")
                    
            with col_info:
                st.markdown(f"### 🧵 {logo.get('nombre', 'Logo')}")
                st.markdown(f"🎟️ **Posición en la cola de producción: #{posicion_en_cola}**")
                st.write(f"**Aplicación:** {logo.get('tipo', 'Tela')} | **Posición prenda:** {logo.get('posicion_logo', 'No especificada')}")
                if logo.get('tipo') == "Gorra":
                    st.write(f"**Detalle Gorra:** {logo.get('ubicacion_gorra', 'N/A')} ({logo.get('detalle_gorra', 'N/A')})")
                st.write(f"**Tus notas:** {logo.get('comentario', 'Ninguno')}")
                st.write(f"**Archivos:** `📁 {logo.get('archivo', 'N/A')}`")
            
            estado_logo = logo.get('estado', 'Pendiente')
            if estado_logo == "Pendiente":
                st.info(f"⏳ Estado: Recibido / Turno #{posicion_en_cola} en espera de revisión")
                col_mod, col_elim = st.columns(2)
                with col_mod:
                    with st.popover("✏️ Modificar Orden"):
                        with st.form(key=f"edit_form_{logo['id']}"):
                            nuevo_nombre = st.text_input("Nuevo nombre", value=logo.get('nombre', ''))
                            nueva_pos = st.selectbox("Nueva posición prenda", ["Pecho Izquierdo", "Pecho Derecho", "Centro Pecho", "Espalda Alta", "Espalda Centro", "Manga Izquierda", "Manga Derecha", "Gorra Frontal", "Gorra Lateral", "Gorra Trasera", "Otra posición"], index=0)
                            nuevo_comentario = st.text_area("Nuevas notas", value=logo.get('comentario', ''))
                            if st.form_submit_button("Guardar Cambios"):
                                logo['nombre'] = nuevo_nombre
                                logo['posicion_logo'] = nueva_pos
                                logo['comentario'] = nuevo_comentario
                                st.success("¡Modificado!")
                                st.rerun()
                with col_elim:
                    if st.button("🗑️ Eliminar", key=f"del_{logo['id']}"):
                        st.session_state.logos.remove(logo)
                        st.warning("Orden eliminada.")
                        st.rerun()
            elif estado_logo == "En Revisión":
                st.info(f"🔍 Estado: Verificando calidad (Turno #{posicion_en_cola})")
            elif estado_logo == "En Progreso":
                st.markdown(
                    f"""
                    <div style="background-color: #d1fae5; border-left: 6px solid #10b981; padding: 10px; border-radius: 5px; color: #065f46; font-weight: bold;">
                        🟢 ¡DIGITALIZANDO EN PROGRESO! (Tu turno #{posicion_en_cola} se está trabajando ahora mismo - Bloqueado para cambios)
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
            
            precio_mostrar = f"${logo.get('precio_usd', 5.0):.2f} USD" if "Dólares" in divisa else f"RD$ {logo.get('precio_dop', 300.0):.2f} DOP"
            st.write(f"Precio estimado: **{precio_mostrar}**")
            st.divider()

        logos_realizados = [l for l in logos_cliente if l.get('estado', 'Pendiente') == "Terminado"]
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
                    st.markdown(f"### 🧵 {logo.get('nombre', 'Logo')}")
                    st.write(f"**Aplicación:** {logo.get('tipo', 'Tela')} | **Posición prenda:** {logo.get('posicion_logo', 'No especificada')}")
                    st.write(f"**Notas:** {logo.get('comentario', 'Ninguno')}")
                
                st.success("✅ Estado: Digitalización Finalizada")
                
                if 'archivos_multiples' in logo and logo['archivos_multiples']:
                    st.write("⬇️ **Descarga tus archivos listos:**")
                    for idx, arch in enumerate(logo['archivos_multiples']):
                        st.download_button(
                            label=f"Descargar: {arch['nombre']}",
                            data=arch['bytes'],
                            file_name=arch['nombre'],
                            mime="application/octet-stream",
                            key=f"dl_multi_{logo['id']}_{idx}"
                        )
                elif 'archivo_bordado_bytes' in logo and logo['archivo_bordado_bytes']:
                    st.download_button(
                        label=f"⬇️ Descargar Archivo Listo: {logo.get('archivo_bordado_nombre', 'bordado.dst')}",
                        data=logo['archivo_bordado_bytes'],
                        file_name=logo.get('archivo_bordado_nombre', 'bordado.dst'),
                        mime="application/octet-stream",
                        key=f"dl_{logo['id']}"
                    )
                else:
                    st.info("📁 Los archivos de bordado estarán disponibles para descarga en breve.")
                
                precio_mostrar = f"${logo.get('precio_usd', 5.0):.2f} USD" if "Dólares" in divisa else f"RD$ {logo.get('precio_dop', 300.0):.2f} DOP"
                st.write(f"Precio final: **{precio_mostrar}** | Pago: **{logo.get('pago', 'Pendiente')}**")
                st.divider()
