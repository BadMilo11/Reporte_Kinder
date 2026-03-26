import streamlit as st
import streamlit.components.v1 as components
from modules.database import save_to_history, get_history, delete_from_history, init_state
from datetime import date

def render():
    st.subheader("📋 Reporte Final e Historial")
    
    # --- FUNCIÓN PARA FORZAR RECARGA SEGURA ---
    def al_cambiar_historico():
        if 'check_hist' in st.session_state and st.session_state.check_hist:
            with st.spinner("🔄 Sincronizando con Google Sheets..."):
                # Forzamos la limpieza de la memoria temporal
                st.cache_data.clear()
                if 'reportes' in st.session_state:
                    del st.session_state['reportes']
                if 'orden_clases' in st.session_state:
                    del st.session_state['orden_clases']
                init_state()

    ver_historico = st.checkbox(
        "🔍 Consultar / Gestionar historial de reportes", 
        key="check_hist",
        on_change=al_cambiar_historico
    )

    if not ver_historico:
        # --- MODO 1: GENERAR Y GUARDAR ---
        st.markdown("### 1. Generar Reporte del Día")
        dia_sel = st.selectbox("Selecciona día:", ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"], key="report_day_sel")

        if 'texto_reporte_final' not in st.session_state:
            st.session_state.texto_reporte_final = ""
        if 'report_key_counter' not in st.session_state:
            st.session_state.report_key_counter = 0

        if st.button("🔄 Generar / Actualizar Reporte", use_container_width=True, type="secondary"):
            clases_ordenadas = sorted(st.session_state.orden_clases.items(), key=lambda x: x[1])
            nuevo_cuerpo = ""
            for clase, pos in clases_ordenadas:
                texto_clase = st.session_state.reportes[clase].get(dia_sel, "")
                contenido = str(texto_clase).strip() if texto_clase else ""
                if contenido and contenido.lower() != "nan":
                    nuevo_cuerpo += f"{contenido}\n\n"
            
            st.session_state.texto_reporte_final = nuevo_cuerpo.strip()
            st.session_state.report_key_counter += 1
            st.rerun()

        dynamic_key = f"final_report_area_{st.session_state.report_key_counter}"
        resultado_final = st.text_area("Reporte final:", value=st.session_state.texto_reporte_final, height=350, key=dynamic_key)
        st.session_state.texto_reporte_final = resultado_final

        if resultado_final.strip():
            # Botón de Copiado con API Moderna
            if st.button("📱 Copiar al Portapapeles", use_container_width=True, type="primary"):
                # Preparamos el texto escapando saltos de línea y comillas
                texto_js = resultado_final.replace("\\", "\\\\").replace("\n", "\\n").replace("'", "\\'").replace("`", "\\`")
                components.html(f"""
                    <script>
                    const copiarTexto = async () => {{
                        try {{
                            // Intentar usar la API moderna de portapapeles
                            await navigator.clipboard.writeText(`{texto_js}`);
                            alert("✅ ¡Reporte copiado con éxito!");
                        }} catch (err) {{
                            // Si falla (por permisos), intentar el método antiguo como respaldo
                            const textArea = document.createElement("textarea");
                            textArea.value = `{texto_js}`;
                            document.body.appendChild(textArea);
                            textArea.select();
                            try {{
                                document.execCommand('copy');
                                alert("✅ ¡Copiado!");
                            }} catch (err2) {{
                                alert("❌ Error al copiar. Intenta seleccionar y copiar manualmente.");
                            }}
                            document.body.removeChild(textArea);
                        }}
                    }};
                    copiarTexto();
                    </script>
                """, height=0)

            st.divider()
            st.markdown("### 2. Archivar")
            fecha_reporte = st.date_input("Fecha:", value=date.today(), key="date_hist")
            if st.button("💾 Guardar en Historial", use_container_width=True):
                save_to_history(fecha_reporte, resultado_final)
                st.success("✅ Guardado en la nube.")

    else:
        # --- MODO 2: CONSULTAR HISTÓRICO ---
        st.markdown("### 🔍 Buscador de Reportes Pasados")
        historico_data = get_history()
        
        if not historico_data:
            st.info("No hay reportes en la nube.")
        else:
            fechas_disponibles = sorted(historico_data.keys(), reverse=True)
            fecha_busqueda = st.selectbox("Selecciona fecha:", fechas_disponibles)
            st.text_area("Contenido:", value=historico_data[fecha_busqueda], height=250, key="hist_view")
            
            if st.button("🗑️ Eliminar registro permanentemente", use_container_width=True):
                with st.spinner("Eliminando..."):
                    if delete_from_history(fecha_busqueda):
                        st.cache_data.clear() # Limpieza extra
                        st.rerun()

if __name__ == "__main__":
    render()
