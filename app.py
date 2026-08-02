import streamlit as st

st.set_page_config(page_title="Pixel Thread - Portal de Clientes", layout="centered")

# --- INICIALIZAR DATOS GLOBALES EN LA SESIÓN (CON REINICIO AUTOMÁTICO SI CAMBIA LA ESTRUCTURA) ---
if "logos" not in st.session_state or "precio_usd" not in st.session_state.logos[0]:
    st.session_state.logos = [
        {"id": 1, "cliente": "Cliente A", "nombre": "Logo León Dorado", "precio_usd": 5.0, "precio_dop": 300.0, "estado": "Pendiente"},
        {"id": 2, "cliente": "Cliente A", "nombre": "Logo Cafetería", "precio_usd": 5.0, "precio_dop": 300.0, "estado": "Pendiente"},
        {"id": 3, "cliente": "Cliente B", "nombre": "Escudo Deportivo", "precio_usd": 5.0, "precio_dop": 300.0, "estado": "Pendiente"},
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

    # Calcular acumulados generales de la semana de forma segura
    total_usd = sum(l.get('precio_usd', 5.0) for l in st.session_state.logos if l['estado'] == "Terminado")
    total_dop = sum(l.get('precio_dop', 300.0) for l in st.session_state.logos if l['estado'] == "Terminado")
    
    col1, col2 = st.columns(2)
    col1.metric("Total Facturable (USD)", f"${total_usd:.2f} USD")
    col2.metric("Total Facturable (DOP)", f"RD$ {total_dop:,.2f}")

    st.divider()
    st.subheader("Lista de Todos los Trabajos")

    for i, logo in enumerate(st.session_state.logos):
        with st.container():
            c1, c2, c3, c4 = st.columns([2, 2, 1, 1])
            c1.write(f"**{logo['nombre']}** \n\n *Cliente: {logo['cliente']}*")
            c2.write(f"Precio: ${logo.get('precio_usd', 5.0):.2f} USD / RD${logo.get('precio_dop', 300.0):.2f}")
            
            estado_actual = logo['estado']
            
            if estado_actual == "Pendiente":
                if c3.button("▶ Iniciar", key=f"iniciar_{i}"):
                    st.session_state.logos[i]['estado'] = "En Progreso"
                    st.rerun()
            elif estado_actual == "En Progreso":
                c3.warning("En Progreso")
                if c4.button("✓ Terminar", key=f"terminar_{i}"):
                    st.session_state.logos[i]['estado'] = "Terminado"
                    st.rerun()
            else:
                c3.success("Completado")

            st.write("---")

    if st.button("📄 Simular Corte y Factura de Lunes"):
        st.success("¡Corte semanal generado con éxito!")
        st.write(f"**Total a cobrar esta semana:** ${total_usd:.2f} USD (RD$ {total_dop:,.2f} DOP)")


# ==========================================
# 2. VISTA CLIENTE A
# ==========================================
elif modo == "Portal Cliente A":
    st.title("👤 Portal de Cliente: Cliente A")
    st.write("Bienvenido a Pixel Thread. Consulta el estado de tus digitalizaciones en tiempo real.")
    
    divisa = st.radio("Selecciona tu moneda de preferencia:", ["Dólares (USD - $)", "Pesos Dominicanos (DOP - RD$)"], horizontal=True)
    
    logos_cliente = [l for l in st.session_state.logos if l['cliente'] == "Cliente A"]
    
    if "Dólares" in divisa:
        total_cliente = sum(l.get('precio_usd', 5.0) for l in logos_cliente if l['estado'] == "Terminado")
        st.metric("Tu Acumulado Actual (Semana)", f"${total_cliente:.2f} USD")
    else:
        total_cliente = sum(l.get('precio_dop', 300.0) for l in logos_cliente if l['estado'] == "Terminado")
        st.metric("Tu Acumulado Actual (Semana)", f"RD$ {total_cliente:,.2f}")

    st.divider()

    for logo in logos_cliente:
        st.markdown(f"### 🧵 {logo['nombre']}")
        
        if logo['estado'] == "Pendiente":
            st.info("⏳ Estado: En espera de turno")
        elif logo['estado'] == "En Progreso":
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
# 3. VISTA CLIENTE B
# ==========================================
elif modo == "Portal Cliente B":
    st.title("👤 Portal de Cliente: Cliente B")
    st.write("Bienvenido a Pixel Thread. Consulta el estado de tus digitalizaciones en tiempo real.")
    
    divisa = st.radio("Selecciona tu moneda de preferencia:", ["Dólares (USD - $)", "Pesos Dominicanos (DOP - RD$)"], horizontal=True, key="divisa_b")
    
    logos_cliente = [l for l in st.session_state.logos if l['cliente'] == "Cliente B"]
    
    if "Dólares" in divisa:
        total_cliente = sum(l.get('precio_usd', 5.0) for l in logos_cliente if l['estado'] == "Terminado")
        st.metric("Tu Acumulado Actual (Semana)", f"${total_cliente:.2f} USD")
    else:
        total_cliente = sum(l.get('precio_dop', 300.0) for l in logos_cliente if l['estado'] == "Terminado")
        st.metric("Tu Acumulado Actual (Semana)", f"RD$ {total_cliente:,.2f}")

    st.divider()

    for logo in logos_cliente:
        st.markdown(f"### 🧵 {logo['nombre']}")
        
        if logo['estado'] == "Pendiente":
            st.info("⏳ Estado: En espera de turno")
        elif logo['estado'] == "En Progreso":
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
