import streamlit as st

st.set_page_config(page_title="Pixel Thread - Portal de Clientes", layout="centered")

# --- INICIALIZAR DATOS GLOBALES EN LA SESIÓN ---
if "logos" not in st.session_state:
    st.session_state.logos = [
        {"id": 1, "cliente": "Cliente A", "nombre": "Logo León Dorado", "precio": 15.0, "estado": "Pendiente"},
        {"id": 2, "cliente": "Cliente A", "nombre": "Logo Cafetería", "precio": 12.0, "estado": "Pendiente"},
        {"id": 3, "cliente": "Cliente B", "nombre": "Escudo Deportivo", "precio": 20.0, "estado": "Pendiente"},
    ]

# --- MENÚ DE NAVEGACIÓN RÁPIDA (Simulador de vistas) ---
st.sidebar.title("Pixel Thread 🧵")
modo = st.sidebar.radio("Selecciona la Vista:", ["Panel Administrador (Tú)", "Portal Cliente A", "Portal Cliente B"])

st.sidebar.divider()
st.sidebar.info("💡 Sin contraseñas: Los clientes solo entran a su enlace y ven su estado en tiempo real.")

# ==========================================
# 1. VISTA ADMINISTRADOR (Tú controlas todo)
# ==========================================
if modo == "Panel Administrador (Tú)":
    st.title("🎛️ Panel de Control - Pixel Thread")
    st.write("Gestiona el estado de los logos. Al marcar un logo como **En Progreso**, se activará la luz verde automáticamente en el portal de tu cliente.")

    # Calcular acumulados generales de la semana
    total_acumulado = sum(l['precio'] for l in st.session_state.logos if l['estado'] == "Terminado")
    terminados_count = sum(1 for l in st.session_state.logos if l['estado'] == "Terminado")
    
    col1, col2 = st.columns(2)
    col1.metric("Total Facturable Semana", f"${total_acumulado:.2f} USD")
    col2.metric("Logos Terminados", terminados_count)

    st.divider()
    st.subheader("Lista de Todos los Trabajos")

    for i, logo in enumerate(st.session_state.logos):
        with st.container():
            c1, c2, c3, c4 = st.columns([2, 2, 1, 1])
            c1.write(f"**{logo['nombre']}** \n\n *Cliente: {logo['cliente']}*")
            c2.write(f"Precio: ${logo['precio']:.2f}")
            
            # Selector de estado directo
            estado_actual = logo['estado']
            
            # Botones de cambio rápido de estado
            if estado_actual == "Pendiente":
                if c3.button("▶ Iniciar", key=f"iniciar_{i}"):
                    st.session_state.logos[i]['estado'] = "En Progreso"
                    st.rerun()
            elif estado_actual == "En Progreso":
                if c3.warning("🟢 En Progreso", icon="⚠️"):
                    pass
                if c4.button("✓ Terminar", key=f"terminar_{i}"):
                    st.session_state.logos[i]['estado'] = "Terminado"
                    st.rerun()
            else:
                c3.success("Completado")

            st.write("---")

    if st.button("📄 Simular Corte y Factura de Lunes"):
        st.success("¡Corte semanal generado con éxito!")
        st.write(f"**Total a cobrar esta semana:** ${total_acumulado:.2f} USD")


# ==========================================
# 2. VISTA CLIENTE A
# ==========================================
elif modo == "Portal Cliente A":
    st.title("👤 Portal de Cliente: Cliente A")
    st.write("Bienvenido. Aquí puedes ver el estado actual de tus logos en digitalización.")
    
    logos_cliente = [l for l in st.session_state.logos if l['cliente'] == "Cliente A"]
    
    total_cliente = sum(l['precio'] for l in logos_cliente if l['estado'] == "Terminado")
    st.metric("Tu Acumulado Actual (Semana)", f"${total_cliente:.2f} USD")
    st.divider()

    for logo in logos_cliente:
        st.markdown(f"### 🧵 {logo['nombre']}")
        
        # Mostrar indicadores visuales según el estado
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
            st.success("✅ Estado: Logo Terminando / Agregado a la factura")
        
        st.write(f"Precio: **${logo['precio']:.2f} USD**")
        st.divider()


# ==========================================
# 3. VISTA CLIENTE B
# ==========================================
elif modo == "Portal Cliente B":
    st.title("👤 Portal de Cliente: Cliente B")
    st.write("Bienvenido. Aquí puedes ver el estado actual de tus logos en digitalización.")
    
    logos_cliente = [l for l in st.session_state.logos if l['cliente'] == "Cliente B"]
    
    total_cliente = sum(l['precio'] for l in logos_cliente if l['estado'] == "Terminado")
    st.metric("Tu Acumulado Actual (Semana)", f"${total_cliente:.2f} USD")
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
            st.success("✅ Estado: Logo Terminando / Agregado a la factura")
            
        st.write(f"Precio: **${logo['precio']:.2f} USD**")
        st.divider()
