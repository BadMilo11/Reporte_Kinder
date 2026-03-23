import streamlit as st

def render():
    st.subheader("📝 Gestión de Contenidos")

    # Selectores para filtrar qué queremos editar
    col1, col2 = st.columns(2)
    with col1:
        dia_sel = st.selectbox("Selecciona el Día", ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"])
    with col2:
        clase_sel = st.selectbox("Selecciona la Clase", list(st.session_state.reportes.keys()))

    # Área de texto que carga lo que ya existe en el diccionario
    texto_actual = st.session_state.reportes[clase_sel][dia_sel]
    
    nuevo_texto = st.text_area(
        f"Reporte de {clase_sel} - {dia_sel}:",
        value=texto_actual,
        height=200,
        placeholder="Escribe aquí las actividades realizadas..."
    )

    # Botones de acción
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        if st.button("💾 Guardar Texto", use_container_width=True):
            st.session_state.reportes[clase_sel][dia_sel] = nuevo_texto
            st.success(f"¡{clase_sel} de {dia_sel} guardado!")
            st.rerun() # Refresca para mostrar cambios

    with col_btn2:
        if st.button("🗑️ Eliminar Texto", use_container_width=True, type="secondary"):
            st.session_state.reportes[clase_sel][dia_sel] = ""
            st.warning("Texto eliminado.")
            st.rerun()

    # Visualización rápida de lo que ya está listo para ese día
    st.divider()
    st.write(f"**Estatus del {dia_sel}:**")
    for c in st.session_state.reportes.keys():
        status = "✅" if st.session_state.reportes[c][dia_sel].strip() else "❌"
        st.write(f"{status} {c}")
