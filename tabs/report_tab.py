import streamlit as st
import streamlit.components.v1 as components
from modules.database import save_to_history, get_history, delete_from_history
from datetime import date

def render():
    st.subheader("📋 Reporte Final e Historial")
    
    # Checkbox para alternar entre "Modo Generar/Guardar" y "Modo Consultar"
    ver_historico = st.checkbox("🔍 Consultar / Gestionar historial de reportes")

    if not ver_historico:
        # --- MODO 1: GENERAR Y GUARDAR ---
        st.markdown("### 1. Generar Reporte del Día")
        dia_sel = st.selectbox("Día de la semana:", ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"])

        clases_ordenadas = sorted(st.session_state.orden_clases.items(), key=lambda x: x[1])
        reporte_cuerpo = ""
        for clase, pos in clases_ordenadas:
            texto_clase = st.session_state.reportes[clase][dia_sel]
            if texto_clase.strip():
                reporte_cuerpo += f"{texto_clase}\n\n"

        if not reporte_cuerpo.strip():
            st.warning(f"⚠️ No hay información para el {dia_sel}.")
        else:
            # Cuadro de texto editable
            resultado_final = st.text_area("Edita el reporte final (estos cambios se pueden guardar al histórico):", 
                                          value=reporte_cuerpo.strip(), height=300)

            # Botón de copiar
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

            # BOTÓN DE GUARDADO EN HISTÓRICO (Solo aparece aquí)
            st.markdown("### 2. Archivar este reporte")
            fecha_reporte = st.date_input("Fecha para el archivo:", value=date.today())
            if st.button("💾 Guardar versión actual en Historial", use_container_width=True):
                save_to_history(fecha_reporte, resultado_final)
                st.success(f"✅ Versión guardada para el {fecha_reporte}")

    else:
        # --- MODO 2: CONSULTAR HISTÓRICO ---
        st.markdown("### 🔍 Buscador en Historial")
        historico_data = get_history()
        if not historico_data:
            st.info("No hay registros en la nube.")
        else:
            fechas_disponibles = sorted(historico_data.keys(), reverse=True)
            fecha_busqueda = st.selectbox("Selecciona fecha:", fechas_disponibles)
            texto_antiguo = historico_data[fecha_busqueda]
            
            reporte_viejo_area = st.text_area("Contenido archivado:", value=texto_antiguo, height=250)
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button("📋 Copiar antiguo", use_container_width=True):
                    # (Aquí iría el mismo bloque de JS de copiado...)
                    pass
            with c2:
                if st.button("🗑️ Eliminar registro", use_container_width=True):
                    if delete_from_history(fecha_busqueda):
                        st.toast("Eliminado")
                        st.rerun()
