import streamlit as st
import streamlit.components.v1 as components
from modules.database import save_to_history, get_history, delete_from_history, init_state
from datetime import date

def render():
    st.subheader("📋 Reporte Final e Historial")
    
    # --- FUNCIÓN PARA FORZAR RECARGA ---
    def al_cambiar_historico():
        # Si el checkbox se activa, limpiamos el estado de reportes para obligar a leer de la nube
        if st.session_state.check_hist:
            # Borramos del session_state para que init_state() vuelva a leer de Google Sheets
            if 'reportes' in st.session_state:
                del st.session_state['reportes']
            if 'orden_clases' in st.session_state:
                del st.session_state['orden_clases']
            init_state() # Recarga todo fresco desde la nube

    # Switch de navegación con el disparador de recarga
    ver_historico = st.checkbox(
        "🔍 Consultar / Gestionar historial de reportes", 
        key="check_hist",
        on_change=al_cambiar_historico
    )

    if not ver_historico:
        # --- MODO 1: GENERAR Y GUARDAR ---
        st.markdown("### 1. Generar Reporte del Día")
        
        dia_sel = st.selectbox(
            "Selecciona el día de la semana:", 
            ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"],
            key="report_day_sel"
        )

        if 'texto_reporte_final' not in st.session_state:
            st.session_state.texto_reporte_final = ""
        if 'report_key_counter' not in st.session_state:
            st.session_state.report_key_counter = 0

        if st.button("🔄 Generar / Actualizar Reporte", use_container_width=True, type="secondary"):
            clases_ordenadas = sorted(st.session_state.orden_clases.items(), key=lambda x: x[1])
            nuevo_cuerpo = ""
            
            for clase, pos in clases_ordenadas:
                texto_clase = st.session_state.reportes[clase].get(dia_sel, "")
                if texto_clase is None: texto_clase = ""
                
                contenido = str(texto_clase).strip()
                if contenido and contenido.lower() != "nan":
                    nuevo_cuerpo += f"{contenido}\n\n"
            
            st.session_state.texto_reporte_final = nuevo_cuerpo.strip()
            st.session_state.report_key_counter += 1
            st.rerun()

        dynamic_key = f"final_report_area_{st.session_state.report_key_counter}"
        
        resultado_final = st.text_area(
            "Edita el reporte final (los 'nan' han sido filtrados):", 
            value=st.session_state.texto_reporte_final, 
            height=350,
            key=dynamic_key
        )
        
        st.session_state.texto_reporte_final = resultado_final

        if resultado_final.strip():
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

            st.markdown("### 2. Archivar en Histórico")
            fecha_reporte = st.date_input("Fecha del reporte:", value=date.today(), key="date_hist")
            
            if st.button("💾 Guardar en Historial (Nube)", use_container_width=True):
                save_to_history(fecha_reporte, resultado_final)
                st.success(f"✅ Reporte del {fecha_reporte} guardado.")

    else:
        # --- MODO 2: CONSULTAR HISTÓRICO ---
        st.markdown("### 🔍 Buscador de Reportes Pasados")
        # Aquí get_history ya tiene ttl=0 en database.py, así que leerá lo último
        historico_data = get_history()
        
        if not historico_data:
            st.info("No hay reportes guardados en la nube.")
        else:
            fechas_disponibles = sorted(historico_data.keys(), reverse=True)
            fecha_busqueda = st.selectbox("Selecciona una fecha:", fechas_disponibles)
            
            texto_archivado = historico_data[fecha_busqueda]
            
            st.text_area("Contenido archivado:", value=texto_archivado, height=250, key="hist_view_area")
            
            if st.button("🗑️ Eliminar registro", use_container_width=True):
                if delete_from_history(fecha_busqueda):
                    st.toast("Eliminado de la nube")
                    st.rerun()
