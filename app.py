import streamlit as st

st.set_page_config(page_title="Pixel Thread - Portal de Clientes", layout="centered")

# --- INICIALIZAR DATOS GLOBALES EN LA SESIÓN ---
if "logos" not in st.session_state or "archivo" not in st.session_state.logos[0]:
    st.session_state.logos = [
        {"id": 1, "cliente": "Cliente A", "nombre": "Logo León Dorado", "precio_usd": 5.0, "precio_dop": 300.0, "estado": "Pendiente", "tipo": "Tela", "detalle_gorra": "N/A", "comentario": "Urgente para entrega", "archivo": "leon.png"},
        {"id": 2, "cliente": "Cliente A", "nombre": "Logo Cafetería", "precio_usd": 5.0, "precio_dop": 300.0, "estado": "Pendiente", "tipo": "Gorra", "detalle_gorra": "3D (Puff)", "comentario": "Centrado en frente", "archivo": "cafe.png"},
        {"id": 3, "cliente": "Cliente B", "nombre": "Escudo Deportivo", "precio_usd": 5.0, "precio_dop": 300.0, "estado": "Pendiente", "tipo": "Tela", "detalle_gorra": "N/A", "comentario": "Ninguno", "archivo": "escudo.png"},
    ]

# --- MENÚ DE NAVEGACIÓN RÁPIDA (Simulador de vistas) ---
st.sidebar.title("Pixel Thread 🧵")
modo = st.sidebar.radio("Selecciona la Vista:", ["Panel Administrador (Tú)", "Portal Cliente A", "Portal Cliente B"])

st.sidebar.divider()
st.sidebar.info("💡 Tarifa oficial: $5.00 USD / $300.00 DOP por logo digitalizado.")

# ==========================================
# 1. VISTA ADMINISTRADOR (Tú controlas todo)
# ==========================================
if modo == "Panel Administrador (Tú)":
    st.title("🎛️ Panel de Control - Pixel Thread")
    st.write("Gestiona el estado de los logos. Al marcar un logo como **En Progreso**, se encenderá la luz verde en el portal de tu cliente.")

    # Calcular acumulados de la semana de forma segura
    total_usd = sum(l.get('precio_usd', 5.0) for l in st.session_state.logos if l['estado'] == "Terminado")
    total_dop = sum(l.get('precio_dop', 300.0) for l in st.session_state.logos if l['estado'] == "Terminado")
    
    col1, col2 = st.columns(2)
    col1.metric("Total Facturable (USD)", f"${total_usd:.2f} USD")
    col2.metric("Total Facturable (DOP)", f"RD$ {total_dop:,.2f}")

    st.divider()
    st.subheader("Lista de Todos los Trabajos")

    for i, logo in enumerate(st.session_state.logos):
        with st.container():
            st.markdown(f"### 🧵 {logo['nombre']} *({logo['cliente']})*")
            st.write(f"**Tipo:** {logo.get('tipo', 'Tela')} | **Detalle Gorra:** {logo.get('detalle_gorra', 'N/A')}")
            st.write(f"**Comentario del cliente:** {logo.get('comentario', 'Ninguno')}")
            st.write(f"**Archivo:** `📁 {logo.get('archivo', 'Sin archivo')}`")
            st.write(f"**Precio:** ${logo.get('precio_usd', 5.0):.2f} USD / RD${logo.get('precio_dop', 300.0):.2f}")
            
            estado_actual = logo['estado']
            
            c1, c2 = st.columns(2)
            if estado_actual == "Pendiente":
                if c1.button("▶ Iniciar (Luz Verde)", key=f"iniciar_{i}"):
                    st.session_state.logos[i]['estado'] = "En Progreso"
                    st.rerun()
            elif estado_actual == "En Progreso":
                c1.warning("🟢 En Progreso (Luz Verde Activa)")
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

    # --- SECCIÓN PARA NUEVO PEDIDO / SUBIR ARCHIVO ---
    with st.expander("➕ Enviar un Nuevo Logo a Digitalizar"):
        with st.form(key=f"form_{nombre_cliente}"):
            nombre_logo = st.text_input("Nombre del Logo / Diseño")
            archivo_subido = st.file_uploader("Sube tu archivo (Imagen o formato de diseño)", type=["png", "jpg", "jpeg", "dst", "emb", "pdf"])
            
            tipo_aplicacion = st.radio("¿Para qué tipo de soporte es el bordado?", ["Tela (Camisetas, Polos, etc.)", "Gorra"])
            
            detalle_gorra = "N/A"
            if tipo_aplicacion == "Gorra":
                detalle_gorra = st.radio("Estilo para Gorra:", ["Plano", "3D (Puff)"])
            
            comentario_cliente = st.text_area("Comentarios o instrucciones adicionales (opcional)")
            
            submitted = st.form_submit_button("Enviar Logo a Pixel Thread")
            if submitted:
                if nombre_logo:
                    nombre_archivo = archivo_subido.name if archivo_subido else "Sin archivo adjunto"
                    nuevo_logo = {
                        "id": len(st.session_state.logos) + 1,
                        "cliente": nombre_cliente,
                        "nombre": nombre_logo,
                        "precio_usd": 5.0,
                        "precio_dop": 300.0,
                        "estado": "Pendiente",
                        "tipo": tipo_aplicacion,
                        "detalle_gorra": detalle_gorra,
                        "comentario": comentario_cliente if comentario_cliente else "Ninguno",
                        "archivo": nombre_archivo
                    }
                    st.session_state.logos.append(nuevo_logo)
                    st.success("¡Logo enviado exitosamente a la cola de trabajo!")
                    st.rerun()
                else:
                    st.error("Por favor, ingresa un nombre para el logo.")

    st.subheader("📋 Tus Trabajos Activos e Historial")

    if not logos_cliente:
        st.info("No tienes logos registrados actualmente.")

    for logo in logos_cliente:
        st.markdown(f"### 🧵 {logo['nombre']}")
        st.write(f"**Aplicación:** {logo.get('tipo', 'Tela')} | **Estilo:** {logo.get('detalle_gorra', 'N/A')}")
        st.write(f"**Tus notas:** {logo.get('comentario', 'Ninguno')}")
        st.write(f"**Archivo adjunto:** `📁 {logo.get('archivo', 'N/A')}`")
        
        if logo['estado'] == "Pendiente":
            st.info("⏳ Estado: En espera de turno")
        elif logo['estado'] == "En Progreso":
            # LA LUZ VERDE SOLICITADA
            st.markdown(
                """
                <div style="background-color: #d1fae5; border-left: 6px solid #10b981; padding: 10px; border-radius: 5px; color: #065f46; font-weight: bold;">
                    🟢 ¡TRABAJANDO EN ESTE LOGO! (En Progreso)
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
# 2. VISTA CLIENTE A
# ==========================================
if modo == "Portal Cliente A":
    render_portal_cliente("Cliente A")

# ==========================================
# 3. VISTA CLIENTE B
# ==========================================
elif modo == "Portal Cliente B":
    render_portal_cliente("Cliente B")
