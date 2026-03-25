import streamlit as st
import streamlit.components.v1 as components
from modules.database import save_to_history, get_history, delete_from_history
from datetime import date

def render():
    st.subheader("📋 Reporte Final e Historial")
    
    # Switch de navegación
    ver_historico = st.checkbox("🔍 Consultar / Gestionar historial de reportes", key="check_hist")

    if not ver_historico:
        # --- MODO 1: GENERAR Y GUARDAR ---
        st.markdown("### 1. Generar Reporte del Día")
        dia_sel = st.selectbox(
            "Selecciona el día de la semana:", 
            ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"],
            key="report_day_sel"
        )

        # Construcción dinámica basada en el orden
        clases_ordenadas = sorted(st.session_state.orden_clases.items(), key=lambda x: x[1])
        reporte_cuerpo = ""
        
        for clase, pos in clases_ordenadas:
            texto_clase = st.session_state.reportes[clase].get(dia_sel, "")
            if texto_clase is None: texto_clase = ""
            
            # --- VALIDACIÓN CRUCIAL ---
            # Si el texto es "nan" (en cualquier combinación de mayúsculas), lo ignoramos
            contenido = str(texto_clase).strip()
            if contenido and contenido.lower() != "nan":
                reporte_cuerpo += f"{contenido}\n\n"

        if not reporte_cuerpo.strip():
            st.warning(f"⚠️ No hay información válida para el {dia_sel} (o todo está marcado como 'nan').")
        else:
            # Cuadro de edición final
            resultado_final = st.text_area(
                "Edita el reporte final (los 'nan' han sido filtrados):", 
                value=reporte_cuerpo.strip(), 
                height=350,
                key="final_report_area"
            )

            # Botón de Copiado
            if st.button("📱 Copiar al Portapapeles", use_container_width=True, type="primary"):
                texto_para_js = resultado_final.replace("\n", "\\n").replace("'", "\\'").replace("`", "\\`")
                components.html(f"""
                    <script>
                    (function() {{
                        const textArea = document.createElement("textarea");
                        textArea.value = `{texto_para_js}`;
                        textArea.style.position = "fixed";
                        textArea.style.left = "-9999px";
                        document.body.appendChild(textArea);
                        textArea.focus();
                        textArea.select();
                        document.execCommand('copy');
                        alert("✅ ¡Copiado al portapapeles!");
                        document.body.removeChild(textArea);
                    }})();
                    </script>
                """, height=0)

            st.divider()

            # --- SECCIÓN DE GUARDADO EN GOOGLE SHEETS ---
            st.markdown("### 2. Archivar en Histórico")
            fecha_reporte = st.date_input("Fecha del reporte:", value=date.today(), key="date_hist")
            
            if st.button("💾 Guardar en Historial (Nube)", use_container_width=True):
                save_to_history(fecha_reporte, resultado_final)
                st.success(f"✅ Reporte del {fecha_reporte} guardado en la pestaña Historial.")

    else:
        # --- MODO 2: CONSULTAR HISTÓRICO ---
        st.markdown("### 🔍 Buscador de Reportes Pasados")
        historico_data = get_history()
        
        if not historico_data:
            st.info("No hay reportes guardados en la nube.")
        else:
            fechas_disponibles = sorted(historico_data.keys(), reverse=True)
            fecha_busqueda = st.selectbox("Selecciona una fecha:", fechas_disponibles)
            texto_antiguo = historico_data[fecha_busqueda]
            
            reporte_viejo_area = st.text_area("Contenido:", value=texto_antiguo, height=250, key="old_report_view")
            
            col_h1, col_h2 = st.columns(2)
            with col_h1:
                if st.button("📋 Copiar antiguo", use_container_width=True):
                    texto_para_js_old = reporte_viejo_area.replace("\n", "\\n").replace("'", "\\'").replace("`", "\\`")
                    components.html(f" <script> ... (mismo JS de copiado) ... </script> ", height=0)
            with col_h2:
                if st.button("🗑️ Eliminar", use_container_width=True):
                    if delete_from_history(fecha_busqueda):
                        st.rerun()

if __name__ == "__main__":
    render()
