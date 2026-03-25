import streamlit as st
import streamlit.components.v1 as components
from modules.database import save_to_history, get_history, delete_from_history
from datetime import date

def render():
    st.subheader("📋 Reporte Final e Historial")
    
    # --- SECCIÓN 1: GENERACIÓN DEL REPORTE ACTUAL ---
    st.markdown("### 1. Generar Reporte del Día")
    dia_sel = st.selectbox(
        "Selecciona el día de la semana:", 
        ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"],
        key="report_day_sel"
    )

    clases_ordenadas = sorted(st.session_state.orden_clases.items(), key=lambda x: x[1])
    
    reporte_cuerpo = ""
    for clase, pos in clases_ordenadas:
        texto_clase = st.session_state.reportes[clase][dia_sel]
        if texto_clase.strip():
            reporte_cuerpo += f"{texto_clase}\n\n"

    if not reporte_cuerpo.strip():
        st.warning(f"⚠️ No hay información guardada para el {dia_sel}.")
    else:
        resultado_final = st.text_area(
            "Edita el reporte final si es necesario:",
            value=reporte_cuerpo.strip(),
            height=300,
            key="final_report_area"
        )

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

        # --- SECCIÓN 2: ARCHIVAR EN HISTÓRICO ---
        st.markdown("### 2. Archivar en Histórico")
        fecha_reporte = st.date_input("¿Para qué fecha es este reporte?", value=date.today())
        
        if st.button("🗄️ Guardar en Historial", use_container_width=True):
            save_to_history(fecha_reporte, resultado_final)
            st.success(f"✅ Reporte del {fecha_reporte} archivado.")

    # --- SECCIÓN 3: CONSULTAR Y GESTIONAR HISTÓRICO ---
    st.divider()
    ver_historico = st.checkbox("🔍 Consultar / Gestionar historial")
    
    if ver_historico:
        historico_data = get_history()
        if not historico_data:
            st.info("Aún no hay reportes en el historial.")
        else:
            fechas_disponibles = sorted(historico_data.keys(), reverse=True)
            fecha_busqueda = st.selectbox("Selecciona una fecha:", fechas_disponibles)
            
            texto_antiguo = historico_data[fecha_busqueda]
            st.markdown(f"**Contenido del {fecha_busqueda}:**")
            
            # Área de texto para el reporte histórico
            reporte_viejo_area = st.text_area("Reporte archivado:", value=texto_antiguo, height=250, key="view_old")
            
            # Botones de Acción para el Historial
            col_h1, col_h2 = st.columns(2)
            
            with col_h1:
                if st.button("📋 Copiar este reporte", use_container_width=True):
                    texto_para_js_old = reporte_viejo_area.replace("\n", "\\n").replace("'", "\\'").replace("`", "\\`")
                    components.html(f"""
                        <script>
                        (function() {{
                            const textArea = document.createElement("textarea");
                            textArea.value = `{texto_para_js_old}`;
                            textArea.style.position = "fixed";
                            textArea.style.left = "-9999px";
                            document.body.appendChild(textArea);
                            textArea.select();
                            document.execCommand('copy');
                            alert("✅ Reporte antiguo copiado!");
                            document.body.removeChild(textArea);
                        }})();
                        </script>
                    """, height=0)

            with col_h2:
                # Botón de eliminar con confirmación simple
                if st.button("🗑️ Eliminar Fecha", use_container_width=True):
                    if delete_from_history(fecha_busqueda):
                        st.toast(f"Reporte del {fecha_busqueda} eliminado")
                        st.rerun()

if __name__ == "__main__":
    render()
