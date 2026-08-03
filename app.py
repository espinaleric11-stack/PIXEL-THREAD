import streamlit as st
import json
import os
from PIL import Image
import io
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Pixel Thread - Portal Profesional", layout="centered")

# --- ACTUALIZACIÓN AUTOMÁTICA CADA 2 SEGUNDOS ---
st_autorefresh(interval=2000, limit=None, key="autorefresh_global")

ARCHIVO_DATOS = "pixel_thread_data.json"

# --- FUNCIONES DE PERSISTENCIA EN DISCO ---
def guardar_datos():
    """Guarda todos los estados críticos en un archivo JSON local."""
    try:
        with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
            json.dump({
                "clientes_registrados": st.session_state.clientes_registrados,
                "logos_meta": [{k: v for k, v in l.items() if k not in ['imagen_obj', 'archivos_multiples', 'archivo_bordado_bytes']} for l in st.session_state.logos],
            }, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error al guardar: {e}")

def cargar_datos():
    """Carga los datos persistidos al iniciar la aplicación."""
    if os.path.exists(ARCHIVO_DATOS):
        try:
            with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
                contenido = json.load(f)
                if "clientes_registrados" in contenido:
                    st.session_state.clientes_registrados = contenido["clientes_registrados"]
                if "logos_meta" in contenido:
                    logos_restaurados = []
                    for lm in contenido["logos_meta"]:
                        lm['imagen_obj'] = None
                        lm['archivos_multiples'] = []
                        logos_restaurados.append(lm)
                    st.session_state.logos = logos_restaurados
                    return True
        except Exception as e:
            print(f"Error al cargar: {e}")
    return False

# --- INICIALIZAR ESTADO PERSISTENTE ---
if "clientes_registrados" not in st.session_state:
    st.session_state.clientes_registrados = {
        "Cliente A": "Dólares (USD - $)",
        "Cliente B": "Pesos Dominicanos (DOP - RD$)"
    }

if "cliente_logeado" not in st.session_state:
    st.session_state.cliente_logeado = None

if "admin_logeado" not in st.session_state:
    st.session_state.admin_logeado = False

if "logos" not in st.session_state:
    if not cargar_datos():
        st.session_state.logos = [
            {"id": 1, "cliente": "Cliente A", "nombre": "Logo León Dorado", "precio_usd": 5.0, "precio_dop": 300.0, "estado": "Pendiente", "pago": "Pendiente", "tipo": "Tela", "ubicacion_gorra": "N/A", "detalle_gorra": "N/A", "posicion_logo": "Pecho Izquierdo", "comentario": "Urgente", "archivo": "leon.png", "imagen_obj": None, "archivos_multiples": []},
            {"id": 2, "cliente": "Cliente A", "nombre": "Logo Cafetería", "precio_usd": 5.0, "precio_dop": 300.0, "estado": "En Progreso", "pago": "Pendiente", "tipo": "Gorra", "ubicacion_gorra": "Frontal", "detalle_gorra": "3D (Puff)", "posicion_logo": "Frontal", "comentario": "Centrado", "archivo": "cafe.png", "imagen_obj": None, "archivos_multiples": []},
            {"id": 3, "cliente": "Cliente B", "nombre": "Escudo Deportivo", "precio_usd": 5.0, "precio_dop": 300.0, "estado": "Terminado", "pago": "Pagado", "tipo": "Tela", "ubicacion_gorra": "N/A", "detalle_gorra": "N/A", "posicion_logo": "Espalda", "comentario": "Ninguno", "archivo": "escudo.png", "imagen_obj": None, "archivos_multiples": []},
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
st.sidebar.caption("🔄 Actualización en vivo (2s) y persistencia activa.")

# ==========================================
# 1. VISTA ADMINISTRADOR (CON SEGURIDAD)
# ==========================================
if modo == "Panel Administrador (Tú)":
    
    if not st.session_state.admin_logeado:
        st.title("🔐 Acceso Restringido - Panel Administrador")
        st.write("Introduce tu usuario de administrador autorizado para continuar:")
        
        with st.form(key="form_login_admin"):
            usuario_admin_ingresado = st.text_input("Usuario Administrador", type="password")
            btn_login_admin = st.form_submit_button("Ingresar al Panel")
            
            if btn_login_admin:
                if usuario_admin_ingresado.strip() == "2580Pixel":
                    st.session_state.admin_logeado = True
                    st.success("¡Acceso concedido!")
                    st.rerun()
                else:
                    st.error("❌ Usuario de administrador incorrecto.")
    
    else:
        col_tadmin, col_btadmin = st.columns([3, 1])
        with col_tadmin:
            st.title("🎛️ Panel de Control - Pixel Thread")
        with col_btadmin:
            st.write("")
            if st.button("🔒 Cerrar Admin"):
                st.session_state.admin_logeado = False
                st.rerun()

        st.write("Administra el flujo de trabajo industrial, el estado de pagos y la entrega de archivos de bordado.")

        recibos_pendientes_count = len(st.session_state.recibos_pago)
        nuevos_logos_count = len([l for l in st.session_state.logos if l.get('estado', 'Pendiente') == "Pendiente"])
        
        if recibos_pendientes_count > 0 or nuevos_logos_count > 0:
            alerta_textos = []
            if recibos_pendientes_count > 0:
                alerta_textos.append(f"🧾 Hay **{recibos_pendientes_count}** comprobante(s) de pago nuevo(s) para revisar.")
            if nuevos_logos_count > 0:
                alerta_textos.append(f"⏳ Hay **{nuevos_logos_count}** logo(s) en cola pendientes de iniciar.")
            
            st.markdown(
                f"""
                <div style="background-color: #fef3c7; border-left: 6px solid #f59e0b; padding: 12px; border-radius: 5px; color: #92400e; margin-bottom: 20px;">
                    <strong>🔔 Atención Requerida:</strong><br>
                    {"<br>".join(alerta_textos)}
                </div>
                """,
                unsafe_allow_html=True
            )

        logos_activos_admin = [l for l in st.session_state.logos if l.get('estado') != "Archivado/Pagado"]
        logos_por_hacer_count = len([l for l in logos_activos_admin if l.get('estado', 'Pendiente') != "Terminado"])
        logos_terminados_count = len([l for l in logos_activos_admin if l.get('estado', 'Pendiente') == "Terminado"])

        total_usd = sum(l.get('precio_usd', 5.0) for l in st.session_state.logos if l.get('pago', 'Pendiente') == "Pagado")
        total_dop = sum(l.get('precio_dop', 300.0) for l in st.session_state.logos if l.get('pago', 'Pendiente') == "Pagado")
        
        c_m1, c_m2, c_m3, c_m4 = st.columns(4)
        c_m1.metric("⏳ Logos por Hacer", logos_por_hacer_count)
        c_m2.metric("✅ Logos Terminados", logos_terminados_count)
        c_m3.metric("Total Acumulado (USD)", f"${total_usd:.2f} USD")
        c_m4.metric("Total Acumulado (DOP)", f"RD$ {total_dop:,.2f}")

        st.divider()

        with st.expander("⚙️ Panel de Gestión: Clientes, Cierre de Ciclos y Recibos", expanded=False):
            st.subheader("➕ Registrar Nuevo Cliente y su Moneda")
            with st.form(key="form_nuevo_clientev2"):
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
                            guardar_datos()
                            st.success(f"¡Cliente '{usuario_limpio}' registrado con éxito y guardado permanentemente!")
                            st.rerun()
                    else:
                        st.error("Por favor, ingresa un nombre para el cliente.")

            st.divider()

            st.subheader("👥 Control, Cierre de Ciclo y Eliminación por Cliente")
            for cli in list(st.session_state.clientes_registrados.keys()):
                logos_cli_term = [l for l in st.session_state.logos if l.get('cliente') == cli and l.get('estado', 'Pendiente') == "Terminado"]
                sub_usd = sum(l.get('precio_usd', 5.0) for l in logos_cli_term)
                sub_dop = sum(l.get('precio_dop', 300.0) for l in logos_cli_term)
                
                with st.expander(f"👤 Cliente: {cli} — Acumulado Terminado: ${sub_usd:.2f} USD / RD$ {sub_dop:,.2f}"):
                    c_info, c_btn1, c_btn2 = st.columns([2, 1, 1])
                    with c_info:
                        st.write(f"Trabajos terminados pendientes de cerrar ciclo: **{len(logos_cli_term)}**")
                    with c_btn1:
                        if st.button(f"🔄 Reiniciar Ciclo", key=f"reset_cli_{cli}"):
                            for logo in st.session_state.logos:
                                if logo.get('cliente') == cli and logo.get('estado', 'Pendiente') == "Terminado":
                                    logo['pago'] = "Pagado"
                                    logo['estado'] = "Archivado/Pagado"
                            guardar_datos()
                            st.success(f"¡Ciclo de {cli} reiniciado y guardado!")
                            st.rerun()
                    with c_btn2:
                        if st.button(f"🗑️ Eliminar Usuario", key=f"del_user_{cli}"):
                            del st.session_state.clientes_registrados[cli]
                            if cli in st.session_state.recibos_pago:
                                del st.session_state.recibos_pago[cli]
                            guardar_datos()
                            st.warning(f"¡Usuario '{cli}' eliminado correctamente!")
                            st.rerun()

            st.divider()

            st.subheader("🧾 Recibos de Pago Subidos por Clientes")
            if st.session_state.recibos_pago:
                for cli, recibo_info in st.session_state.recibos_pago.items():
                    with st.expander(f"📥 Ver Recibo de Pago de: {cli} ({recibo_info['nombre_archivo']})"):
                        st.image(recibo_info['bytes'], caption=f"Comprobante de {cli}", width=300)
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

        logos_por_hacer = [l for l in logos_activos_admin if l.get('estado', 'Pendiente') != "Terminado"]
        logos_terminados = [l for l in logos_activos_admin if l.get('estado', 'Pendiente'] == "Terminado"] if False else [l for l in logos_activos_admin if l.get('estado', 'Pendiente') == "Terminado"]
        logos_ordenados_admin = logos_por_hacer + logos_terminados

        st.subheader("📋 Gestión de Trabajos")

        @st.fragment
        def renderizar_lista_admin(logos_lista):
            for logo in logos_lista:
                i = next((idx for idx, item in enumerate(st.session_state.logos) if item["id"] == logo["id"]), None)
                if i is None:
                    continue
                
                with st.container():
                    col_img, col_info = st.columns([1, 3])
                    
                    with col_img:
                        if logo.get('imagen_obj') is not None:
                            st.image(logo['imagen_obj'], caption="Diseño Original", width=100)
                            with st.popover("🔍 Ver Grande"):
                                st.image(logo['imagen_obj'], caption=f"Diseño: {logo.get('nombre')}", use_container_width=True)
                        else:
                            st.info("Sin miniatura")

                    with col_info:
                        st.markdown(f"### 🧵 {logo.get('nombre', 'Sin nombre')} *({logo.get('cliente', 'Cliente')})*")
                        st.write(f"**Tipo:** {logo.get('tipo', 'Tela')} | **Posición:** {logo.get('posicion_logo', 'No especificada')} | **Estado Actual:** `{logo.get('estado', 'Pendiente')}`")
                        st.write(f"**Comentario:** {logo.get('comentario', 'Ninguno')}")
                        st.write(f"**Archivo cliente:** `📁 {logo.get('archivo', 'Sin archivo')}`")
                        st.write(f"**Precio:** ${logo.get('precio_usd', 5.0):.2f} USD / RD${logo.get('precio_dop', 300.0):.2f}")
                    
                    estado_actual = logo.get('estado', 'Pendiente')
                    
                    c1, c2, c3 = st.columns(3)
                    
                    if estado_actual == "Pendiente":
                        if c1.button("▶ Iniciar (Luz Verde)", key=f"iniciar_{logo['id']}"):
                            st.session_state.logos[i]['estado'] = "En Progreso"
                            guardar_datos()
                            st.rerun()
                    elif estado_actual == "En Progreso":
                        c1.warning("🟢 En Progreso")
                        if c2.button("✓ Marcar Terminado", key=f"terminar_{logo['id']}"):
                            st.session_state.logos[i]['estado'] = "Terminado"
                            guardar_datos()
                            st.rerun()
                    else:
                        c1.success("✅ Terminado")
                        pago_actual = logo.get('pago', 'Pendiente')
                        nuevo_pago = c2.selectbox("Estado de Pago", ["Pendiente", "Pagado"], index=0 if pago_actual=="Pendiente" else 1, key=f"pago_{logo['id']}")
                        if nuevo_pago != pago_actual:
                            st.session_state.logos[i]['pago'] = nuevo_pago
                            guardar_datos()
                            st.rerun()

                    with st.form(key=f"form_subida_archivos_{logo['id']}"):
                        archivos_bordado = st.file_uploader(
                            "Sube los archivos listos para bordar (.DST / .EMB / .PDF)", 
                            type=["dst", "emb", "pes", "jef", "pdf"], 
                            accept_multiple_files=True, 
                            key=f"bordado_{logo['id']}"
                        )
                        btn_guardar_archivos = st.form_submit_button("Guardar Archivos en la Orden")
                        if btn_guardar_archivos:
                            if archivos_bordado:
                                st.session_state.logos[i]['archivos_multiples'] = [{"nombre": f.name, "bytes": f.getvalue()} for f in archivos_bordado]
                                guardar_datos()
                                nombres_str = ", ".join([f.name for f in archivos_bordado])
                                st.success(f"¡Archivos guardados correctamente: {nombres_str}!")
                                st.rerun()
                            else:
                                st.warning("Por favor, selecciona al menos un archivo para subir.")

                    st.divider()

        renderizar_lista_admin(logos_ordenados_admin)


# ==========================================
# 2. PORTAL DE CLIENTES
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
            if st.button("🚪 Salir"):
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
            with st.form(key=f"form_recibo_{nombre_cliente}"):
                recibo_subido = st.file_uploader("Sube tu comprobante", type=["png", "jpg", "jpeg", "pdf"], key=f"recibo_file_{nombre_cliente}")
                btn_enviar_recibo = st.form_submit_button("Enviar Comprobante")
                if btn_enviar_recibo:
                    if recibo_subido:
                        st.session_state.recibos_pago[nombre_cliente] = {
                            "nombre_archivo": recibo_subido.name,
                            "bytes": recibo_subido.getvalue()
                        }
                        st.success("¡Recibo enviado al administrador con éxito!")
                        st.rerun()
                    else:
                        st.warning("Selecciona un archivo antes de enviar.")

        st.divider()

        with st.expander("➕ Enviar un Nuevo Logo a Digitalizar", expanded=False):
            if st.session_state.form_enviado:
                st.success("✅ ¡ORDEN AGREGADA CORRECTAMENTE!")
                if st.button("Enviar otro diseño", key=f"otro_{nombre_cliente}"):
                    st.session_state.form_enviado = False
                    st.rerun()
            else:
                with st.form(key=f"form_nuevo_logo_{nombre_cliente}"):
                    nombre_logo = st.text_input("Nombre del Logo / Diseño")
                    
                    archivos_subidos = st.file_uploader(
                        "Sube tus archivos originales (puedes seleccionar varios a la vez)", 
                        type=["png", "jpg", "jpeg", "ai", "pdf"], 
                        accept_multiple_files=True
                    )
                    
                    tipo_aplicacion = st.radio("¿Para qué tipo de soporte es el bordado?", ["Tela (Camisetas, Polos, etc.)", "Gorra"])
                    
                    posicion_logo = st.selectbox(
                        "Posición del logo en la prenda:", 
                        ["Pecho Izquierdo", "Pecho Derecho", "Centro Pecho", "Espalda Alta", "Espalda Centro", "Manga Izquierda", "Manga Derecha", "Gorra Frontal", "Gorra Lateral", "Gorra Trasera", "Otra posición"]
                    )
                    
                    ubicacion_gorra = "N/A"
                    detalle_gorra = "N/A"
                    
                    if tipo_aplicacion == "Gorra":
                        ubicacion_gorra = st.radio("Selecciona la ubicación específica en la gorra:", ["Frontal", "Trasero", "Lateral"])
                        if ubicacion_gorra == "Frontal":
                            detalle_gorra = st.radio("Selecciona el estilo:", ["3D (Puff)", "Plano (Flat)"])
                        else:
                            detalle_gorra = "Plano (Flat)"
                    
                    comentario_cliente = st.text_area("Comentarios o instrucciones especiales")
                    
                    btn_enviar_logo = st.form_submit_button("Enviar Logo a Pixel Thread")
                    if btn_enviar_logo:
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
                                "imagen_obj": img_obj,
                                "archivos_multiples": []
                            }
                            st.session_state.logos.append(nuevo_logo)
                            guardar_datos()
                            st.session_state.form_enviado = True
                            st.rerun()
                        else:
                            st.error("Por favor, ingresa un nombre para el logo.")

        # --- CONTENEDOR DINÁMICO CON FRAGMENTO PARA ACTUALIZACIÓN EN VIVO ---
        @st.fragment
        def renderizar_portal_cliente(nombre_cli, divisa_actual):
            logos_cli = [l for l in st.session_state.logos if l.get('cliente') == nombre_cli and l.get('estado') != "Archivado/Pagado"]
            logos_por_realizar = [l for l in logos_cli if l.get('estado') not in ["Terminado", "Archivado/Pagado"]]
            
            st.subheader("⏳ Trabajos por Realizar y Turno en Cola")
            if not logos_por_realizar:
                st.info("No tienes trabajos pendientes actualmente.")

            cola_global_activa = [l for l in st.session_state.logos if l.get('estado') not in ["Terminado", "Archivado/Pagado"]]

            for logo in logos_por_realizar:
                if logo in cola_global_activa:
                    posicion_en_cola = cola_global_activa.index(logo) + 1
                else:
                    posicion_en_cola = "?"

                col_img, col_info = st.columns([1, 3])
                with col_img:
                    if logo.get('imagen_obj') is not None:
                        st.image(logo['imagen_obj'], caption="Tu Diseño", width=100)
                        with st.popover("🔍 Ver Grande"):
                            st.image(logo['imagen_obj'], caption=f"Tu Diseño: {logo.get('nombre')}", use_container_width=True)
                    else:
                        st.info("Sin miniatura")
                        
                with col_info:
                    st.markdown(f"### 🧵 {logo.get('nombre', 'Logo')}")
                    st.markdown(f"🎟️ Posición en la cola de producción: <span style='color: #10b981; font-weight: bold;'>#{posicion_en_cola}</span>", unsafe_allow_html=True)
                    st.write(f"**Aplicación:** {logo.get('tipo', 'Tela')} | **Posición prenda:** {logo.get('posicion_logo', 'No especificada')}")
                    if logo.get('tipo') == "Gorra":
                        st.write(f"**Detalle Gorra:** {logo.get('ubicacion_gorra', 'N/A')} ({logo.get('detalle_gorra', 'N/A')})")
                    st.write(f"**Tus notas:** {logo.get('comentario', 'Ninguno')}")
                    st.write(f"**Archivos:** `📁 {logo.get('archivo', 'N/A')}`")
                
                estado_logo = logo.get('estado', 'Pendiente')
                if estado_logo == "Pendiente":
                    st.info(f"⏳ Estado: Recibido / Turno #{posicion_en_cola} en espera de inicio")
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
                                    guardar_datos()
                                    st.success("¡Modificado y guardado!")
                                    st.rerun()
                    with col_elim:
                        if st.button("🗑️ Eliminar", key=f"del_{logo['id']}"):
                            st.session_state.logos.remove(logo)
                            guardar_datos()
                            st.warning("Orden eliminada.")
                            st.rerun()
                elif estado_logo == "En Progreso":
                    st.markdown(
                        f"""
                        <div style="background-color: #d1fae5; border-left: 6px solid #10b981; padding: 10px; border-radius: 5px; color: #065f46; font-weight: bold;">
                            🟢 ¡DIGITALIZANDO EN PROGRESO! (Tu turno #{posicion_en_cola} se está trabajando ahora mismo - Bloqueado para cambios)
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                
                precio_mostrar = f"${logo.get('precio_usd', 5.0):.2f} USD" if "Dólares" in divisa_actual else f"RD$ {logo.get('precio_dop', 300.0):.2f} DOP"
                st.write(f"Precio estimado: **{precio_mostrar}**")
                st.divider()

            logos_realizados = [l for l in logos_cli if l.get('estado') == "Terminado"]
            
            st.subheader("✅ Trabajos Realizados y Descargas")
            if not logos_realizados:
                st.info("Aún no tienes trabajos terminados listos para descarga.")
            else:
                for logo in logos_realizados:
                    col_img, col_info = st.columns([1, 3])
                    with col_img:
                        if logo.get('imagen_obj') is not None:
                            st.image(logo['imagen_obj'], caption="Diseño", width=100)
                            with st.popover("🔍 Ver Grande"):
                                st.image(logo['imagen_obj'], caption=f"Diseño Terminado: {logo.get('nombre')}", use_container_width=True)
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
                    
                    precio_mostrar = f"${logo.get('precio_usd', 5.0):.2f} USD" if "Dólares" in divisa_actual else f"RD$ {logo.get('precio_dop', 300.0):.2f} DOP"
                    st.write(f"Precio final: **{precio_mostrar}** | Pago: **{logo.get('pago', 'Pendiente')}**")
                    st.divider()

        renderizar_portal_cliente(nombre_cliente, divisa)
