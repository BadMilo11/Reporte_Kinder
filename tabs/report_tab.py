import streamlit as st
import streamlit.components.v1 as components

def render():
    st.subheader("📋 Reporte Final")
    
    # 1. Selección del día
    dia_sel = st.selectbox("¿De qué día quieres el reporte?", 
                          ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"],
                          key="report_day_sel")

    # 2. Lógica para construir el texto
    clases_ordenadas = sorted(st.session_state.orden_clases.items(), key=lambda x: x[1])
    
    reporte_completo = ""
    for clase, pos in clases_ordenadas:
        texto_clase = st.session_state.reportes[clase][dia_sel]
        if texto_clase.strip():
            reporte_completo += f"*{clase}*\n{texto_clase}\n\n"

    # 3. Validación y Visualización
    if not reporte_completo.strip():
        st.warning(f"⚠️ No hay información guardada para el {dia_sel}. Redacta algo en la primera pestaña.")
    else:
        resultado_final = st.text_area(
            "Edita el reporte final si es necesario:",
            value=reporte_completo,
            height=400,
            key="final_report_area"
        )

        # 4. BOTÓN DE COPIADO
        if st.button("📱 Copiar Reporte Completo", use_container_width=True, type="primary"):
            # Escapamos los caracteres para JS
            texto_para_js = resultado_final.replace("\n", "\\n").replace("'", "\\'").replace("`", "\\`")
            
            # El truco aquí es usar una variable de control o asegurar que el JS se ejecute solo al click
            components.html(f"""
                <script>
                (function() {{
                    const text = `{texto_para_js}`;
                    navigator.clipboard.writeText(text).then(() => {{
                        alert("✅ ¡Copiado al portapapeles! Ya puedes pegarlo en WhatsApp.");
                    }}).catch(err => {{
                        alert("Hubo un error al copiar. Intenta seleccionar el texto manualmente.");
                    }});
                }})();
                </script>
            """, height=0)

    st.caption("Tip: El formato con *asteriscos* se verá como **negrita** al pegarlo en WhatsApp.")
