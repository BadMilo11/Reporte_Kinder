import streamlit as st
import streamlit.components.v1 as components
from modules.database import save_to_history, get_history, delete_from_history
from datetime import date

def render():
    st.subheader("📋 Reporte Final e Historial")
    
    # 1. Switch de navegación: Ocultamos el generador si estamos consultando el historial
    ver_historico = st.checkbox("🔍 Consultar / Gestionar historial de reportes", key="check_hist")

    if not ver_historico:
        # --- MODO 1: GENERAR Y GUARDAR ---
        st.markdown("### 1. Generar Reporte del Día")
        dia_sel = st.selectbox(
            "Selecciona el día de la semana:", 
            ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"],
            key="report_day_sel"
        )

        # Construcción dinámica basada en el orden de la Tab 2
        clases_ordenadas = sorted(st.session_state.orden_clases.items(), key=lambda x: x[1])
        reporte_cuerpo = ""
        for clase, pos in clases_ordenadas:
            texto_clase = st.session_state.reportes[clase][dia_sel]
            if texto_clase.strip():
                reporte_cuerpo += f"{texto_clase}\n\n"

        if not reporte_cuerpo.strip():
            st.warning(f"⚠️ No hay información guardada para el {dia_sel}.")
        else:
            # Cuadro de edición final (Aquí es donde la maestra hace ajustes de último minuto)
            resultado_final = st.text_area(
                "Edita el reporte final (estos cambios se guardarán si usas el historial):", 
                value=reporte_cuerpo.strip(), 
                height=350,
                key="final_report_area"
            )

            # Botón de Copiado Principal
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

            # --- SECCIÓN DE GUARDADO EN GOOGLE SHEETS (HISTÓRICO) ---
            st.markdown("### 2. Archivar en Histórico")
            st.caption("Selecciona la fecha exacta y guarda la versión final que aparece arriba.")
            
            fecha_reporte = st.date_input("Fecha del reporte:", value=date.today(), key="date_hist")
            
            if st.button("💾 Guardar en Historial (Nube)", use_container_width=True):
                # Importante: Guardamos 'resultado_final' para capturar sus ediciones manuales
                save_to_history(fecha_reporte, resultado_final)
                st.success(f"✅ Reporte del {fecha_reporte} guardado en Google Sheets.")

    else:
        # --- MODO 2: CONSULTAR HISTÓRICO ---
        st.markdown("### 🔍 Buscador de Reportes Pasados")
        historico_data = get_history()
        
        if not historico_data:
            st.info("Aún no hay reportes guardados en la nube.")
        else:
            # Ordenamos para que lo más reciente aparezca arriba
            fechas_disponibles = sorted(historico_data.keys(), reverse=True)
            fecha_busqueda = st.selectbox("Selecciona una fecha guardada:", fechas_disponibles)
            
            texto_antiguo = historico_data[fecha_busqueda]
            
            st.markdown(f"**Reporte archivado del {fecha_busqueda}:**")
            reporte_viejo_area = st.text_area("Contenido:", value=texto_antiguo, height=250, key="old_report_view")
            
            col_h1, col_h2 = st.columns(2)
            
            with col_h1:
                # Botón de copiado para reportes antiguos
                if st.button("📋 Copiar este", use_container_width=True):
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
                # Botón de eliminar con actualización inmediata
                if st.button("🗑️ Eliminar", use_container_width=True):
                    if delete_from_history(fecha_busqueda):
                        st.toast(f"Reporte del {fecha_busqueda} eliminado de la nube")
                        st.rerun()

if __name__ == "__main__":
    render()
