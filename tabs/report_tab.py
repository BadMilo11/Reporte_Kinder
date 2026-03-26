import streamlit as st
import streamlit.components.v1 as components
from modules.database import save_to_history, get_history, delete_from_history
from datetime import date

def render():
    st.subheader("📋 Reporte Final e Historial")
    
    ver_historico = st.checkbox("🔍 Consultar / Gestionar historial de reportes", key="check_hist")

    if not ver_historico:
        st.markdown("### 1. Generar Reporte del Día")
        
        # Selector de día
        dia_sel = st.selectbox(
            "Selecciona el día de la semana:", 
            ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"],
            key="report_day_sel"
        )

        # Inicializamos variables en el estado de la sesión si no existen
        if 'texto_reporte_final' not in st.session_state:
            st.session_state.texto_reporte_final = ""
        if 'report_key_counter' not in st.session_state:
            st.session_state.report_key_counter = 0

        # --- BOTÓN DE GENERACIÓN FORZADA ---
        if st.button("🔄 Generar / Actualizar Reporte", use_container_width=True, type="secondary"):
            clases_ordenadas = sorted(st.session_state.orden_clases.items(), key=lambda x: x[1])
            nuevo_cuerpo = ""
            
            for clase, pos in clases_ordenadas:
                texto_clase = st.session_state.reportes[clase].get(dia_sel, "")
                if texto_clase is None: texto_clase = ""
                
                contenido = str(texto_clase).strip()
                if contenido and contenido.lower() != "nan":
                    nuevo_cuerpo += f"{contenido}\n\n"
            
            # 1. Actualizamos el contenido
            st.session_state.texto_reporte_final = nuevo_cuerpo.strip()
            # 2. Incrementamos el contador para cambiar la KEY del text_area y forzar el refresco visual
            st.session_state.report_key_counter += 1
            st.rerun()

        # Cuadro de edición final
        # Usamos una key dinámica: "final_area_0", "final_area_1", etc.
        dynamic_key = f"final_report_area_{st.session_state.report_key_counter}"
        
        resultado_final = st.text_area(
            "Edita el reporte final (los 'nan' han sido filtrados):", 
            value=st.session_state.texto_reporte_final, 
            height=350,
            key=dynamic_key
        )
        
        # Sincronizamos lo que la maestra escriba manualmente con el session_state
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

            # --- SECCIÓN DE GUARDADO EN HISTÓRICO ---
            st.markdown("### 2. Archivar en Histórico")
            fecha_reporte = st.date_input("Fecha del reporte:", value=date.today(), key="date_hist")
            
            if st.button("💾 Guardar en Historial (Nube)", use_container_width=True):
                save_to_history(fecha_reporte, resultado_final)
                st.success(f"✅ Reporte del {fecha_reporte} guardado en la pestaña Historial.")
        else:
            st.info("Presiona el botón 'Generar' para cargar la información del día.")

    else:
        # --- MODO CONSULTAR (Se mantiene igual) ---
        st.markdown("### 🔍 Buscador de Reportes Pasados")
        historico_data = get_history()
        if not historico_data:
            st.info("No hay reportes guardados en la nube.")
        else:
            fechas_disponibles = sorted(historico_data.keys(), reverse=True)
            fecha_busqueda = st.selectbox("Selecciona una fecha:", fechas_disponibles)
            st.text_area("Contenido archivado:", value=historico_data[fecha_busqueda], height=250)
            if st.button("🗑️ Eliminar registro", use_container_width=True):
                if delete_from_history(fecha_busqueda):
                    st.rerun()
