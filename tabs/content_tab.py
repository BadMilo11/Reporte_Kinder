import streamlit as st
from modules.database import save_to_disk

def render():
    st.subheader("📝 Contenido de los Reportes")
    
    dia_sel = st.selectbox("Seleccionar día para editar:", 
                          ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"],
                          key="content_day_sel")

    # --- INDICADORES DE ESTADO (STATUS) ---
    st.write("**Estado de avance:**")
    cols_status = st.columns(5)
    clases_lista = list(st.session_state.reportes.keys())
    
    for i, c in enumerate(clases_lista):
        with cols_status[i % 5]:
            # Validación segura contra valores None/NaN de Google Sheets
            texto_raw = st.session_state.reportes[c].get(dia_sel, "")
            if texto_raw is None: texto_raw = ""
            
            if len(str(texto_raw).strip()) > 0:
                st.caption(f"✅ {c}")
            else:
                st.caption(f"⚪ {c}")

    st.divider()

    # --- ÁREA DE EDICIÓN ---
    for clase in clases_lista:
        with st.expander(f"Editar: {clase}", expanded=False):
            # Obtener valor actual de forma segura
            valor_actual = st.session_state.reportes[clase].get(dia_sel, "")
            if valor_actual is None: valor_actual = ""

            nuevo_texto = st.text_area(
                f"Escribe el reporte de {clase}:",
                value=str(valor_actual),
                key=f"input_{clase}_{dia_sel}",
                height=150
            )
            # Actualizamos el estado en memoria
            st.session_state.reportes[clase][dia_sel] = nuevo_texto

    st.divider()
    
    # --- BOTÓN DE GUARDADO ---
    if st.button("💾 Guardar Cambios en la Nube", use_container_width=True, type="primary"):
        save_to_disk()
        st.success(f"✅ Reportes del {dia_sel} guardados en Google Sheets.")
        st.rerun()

if __name__ == "__main__":
    render()
