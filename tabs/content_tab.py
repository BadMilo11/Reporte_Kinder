import streamlit as st
from modules.database import save_to_disk

def render():
    st.subheader("📝 Contenido de los Reportes")
    
    dia_sel = st.selectbox("Seleccionar día para editar:", 
                          ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"],
                          key="content_day_sel")

    # --- INDICADORES DE ESTADO (STATUS) ---
    st.write("**Estado de avance:**")
    st.caption("✅ = Lleno | ❌ = No aplica (nan) | ⚪ = Vacío")
    
    cols_status = st.columns(5)
    clases_lista = list(st.session_state.reportes.keys())
    
    for i, c in enumerate(clases_lista):
        with cols_status[i % 5]:
            # Obtención segura del texto
            texto_raw = st.session_state.reportes[c].get(dia_sel, "")
            if texto_raw is None: texto_raw = ""
            texto_str = str(texto_raw).strip().lower() # Convertimos a minúsculas para comparar
            
            # Lógica de validación visual
            if texto_str == "nan":
                st.caption(f"❌ {c}")
            elif len(texto_str) > 0:
                st.caption(f"✅ {c}")
            else:
                st.caption(f"⚪ {c}")

    st.divider()

    # --- ÁREA DE EDICIÓN ---
    for clase in clases_lista:
        with st.expander(f"Editar: {clase}", expanded=False):
            valor_actual = st.session_state.reportes[clase].get(dia_sel, "")
            if valor_actual is None: valor_actual = ""

            nuevo_texto = st.text_area(
                f"Escribe el reporte de {clase} (Escribe 'nan' si no aplica):",
                value=str(valor_actual),
                key=f"input_{clase}_{dia_sel}",
                height=150
            )
            # Guardamos en memoria exactamente lo que el usuario escribe
            st.session_state.reportes[clase][dia_sel] = nuevo_texto

    st.divider()
    
    if st.button("💾 Guardar Cambios en la Nube", use_container_width=True, type="primary"):
        save_to_disk()
        st.success(f"✅ Reportes del {dia_sel} guardados.")
        st.rerun()
