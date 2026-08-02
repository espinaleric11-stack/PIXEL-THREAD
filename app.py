import streamlit as st

st.set_page_config(page_title="Pixel Thread - Control", layout="centered")

st.title("Pixel Thread")
st.subheader("Gestión de Digitalización y Facturación Semanal")

# Inicializar variables en la sesión
if "acumulado" not in st.session_state:
    st.session_state.acumulado = 0.0
if "terminados" not in st.session_state:
    st.session_state.terminados = 0
if "lista_trabajos" not in st.session_state:
    st.session_state.lista_trabajos = []

st.sidebar.metric("Acumulado Actual", f"${st.session_state.acumulado:.2f} USD")
st.sidebar.metric("Logos Terminados", st.session_state.terminados)

st.write("### Trabajos Activos")

trabajos = [
    {"id": 1, "nombre": "Logo León Dorado (Pecho)", "precio": 15.0},
    {"id": 2, "nombre": "Logo Cafetería (Manga)", "precio": 12.0},
    {"id": 3, "nombre": "Escudo Deportivo (Espalda)", "precio": 20.0}
]

for t in trabajos:
    col1, col2, col3 = st.columns([3, 1, 1])
    col1.write(f"**{t['nombre']}**")
    col2.write(f"${t['precio']:.2f}")
    
    if col3.button("Terminar", key=f"btn_{t['id']}"):
        st.session_state.acumulado += t['precio']
        st.session_state.terminados += 1
        st.session_state.lista_trabajos.append(t)
        st.success(f"¡{t['nombre']} completado!")
        st.rerun()

st.divider()

if st.button("Simular Corte de Lunes 📄"):
    if st.session_state.terminados == 0:
        st.warning("No hay logos terminados esta semana para facturar.")
    else:
        st.success("¡Factura Generada y Enviada!")
        for item in st.session_state.lista_trabajos:
            st.write(f"- {item['nombre']}: ${item['precio']:.2f}")
        st.write(f"**TOTAL A PAGAR: ${st.session_state.acumulado:.2f} USD**")
