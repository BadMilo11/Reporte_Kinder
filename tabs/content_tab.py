import streamlit as st
from modules.database import save_to_disk

def render():
    st.subheader("📝 Gestión de Contenidos")
    st.info("Selecciona un día y una clase para redactar el reporte correspondiente.")

    # 1. Selectores de filtro
    col1, col2 = st.columns(2)
    with col1:
        # Usamos un índice para que el día persista en el selector al recargar
        dias_opciones = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
        dia_sel = st.selectbox("📅 Selecciona el Día", dias_opciones)
    
    with col2:
        clases_opciones = list(st.session_state.reportes.keys())
        clase_sel = st.selectbox("🏫 Selecciona la Clase", clases_opciones)

    st.divider()

    # 2. Área de Redacción
    # Cargamos el texto que ya existe en el estado global
    texto_actual = st.session_state.reportes[clase_sel][dia_sel]
    
    nuevo_texto = st.text_area(
        f"Editando: {clase_sel} ({dia_sel})",
        value=texto_actual,
        height=250,
        placeholder="Escribe aquí las actividades, logros o avisos del día..."
    )

    # 3. Botones de Acción
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        if st.button("💾 Guardar Cambios", use_container_width=True, type="primary"):
            # Actualizamos la memoria (session_state)
            st.session_state.reportes[clase_sel][dia_sel] = nuevo_texto
            # Guardamos físicamente en el archivo JSON
            save_to_disk()
            st.toast(f"¡{clase_sel} guardado correctamente!", icon="✅")
            st.rerun()

    with col_btn2:
        if st.button("🗑️ Borrar Texto", use_container_width=True):
            # Limpiamos el texto
            st.session_state.reportes[clase_sel][dia_sel] = ""
            save_to_disk()
            st.toast("Contenido eliminado", icon="🗑️")
            st.rerun()

    # 4. Monitor de Progreso (Visualización de Estatus)
    st.divider()
    st.markdown(f"### 📊 Estatus del {dia_sel}")
    
    # Mostramos una lista rápida de qué clases tienen contenido y cuáles no
    cols_status = st.columns(2)
    items = list(st.session_state.reportes.keys())
    mitad = len(items) // 2
    
    with cols_status[0]:
        for c in items[:mitad]:
            tiene_texto = bool(st.session_state.reportes[c][dia_sel].strip())
            icon = "✅" if tiene_texto else "❌"
            st.write(f"{icon} {c}")
            
    with cols_status[1]:
        for c in items[mitad:]:
            tiene_texto = bool(st.session_state.reportes[c][dia_sel].strip())
            icon = "✅" if tiene_texto else "❌"
            st.write(f"{icon} {c}")

if __name__ == "__main__":
    render()
