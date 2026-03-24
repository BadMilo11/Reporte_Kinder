import streamlit as st
import streamlit.components.v1 as components

def render():
    st.subheader("📋 Reporte Final")
    
    # 1. Selección del día
    dia_sel = st.selectbox(
        "¿De qué día quieres el reporte?", 
        ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"],
        key="report_day_sel"
    )

    # 2. Construcción del texto (Sin el nombre de la clase)
    clases_ordenadas = sorted(st.session_state.orden_clases.items(), key=lambda x: x[1])
    
    reporte_cuerpo = ""
    for clase, pos in clases_ordenadas:
        texto_clase = st.session_state.reportes[clase][dia_sel]
        if texto_clase.strip():  # Solo incluimos si tiene contenido
            # Solo añadimos el texto y saltos de línea
            reporte_cuerpo += f"{texto_clase}\n\n"

    # 3. Área de edición y botón de copiado
    if not reporte_cuerpo.strip():
        st.warning(f"⚠️ No hay información guardada para el {dia_sel}. Ve a la pestaña de Redacción.")
    else:
        resultado_final = st.text_area(
            "Puedes hacer ajustes finales aquí:",
            value=reporte_cuerpo.strip(), # .strip() para quitar espacios extras al final
            height=400,
            key="final_report_area"
        )

        # 4. Botón de Copiado Optimizado para iPhone
        if st.button("📱 Copiar Reporte Completo", use_container_width=True, type="primary"):
            # Limpiamos el texto para que no rompa el script de JS
            texto_para_js = resultado_final.replace("\n", "\\n").replace("'", "\\'").replace("`", "\\`")
            
            # Usamos execCommand('copy') dentro de un elemento temporal, más estable en iOS iFrames
            components.html(f"""
                <script>
                (function() {{
                    const textArea = document.createElement("textarea");
                    textArea.value = `{texto_para_js}`;
                    // Aseguramos que el elemento no sea visible pero esté en el DOM
                    textArea.style.position = "fixed";
                    textArea.style.left = "-9999px";
                    textArea.style.top = "0";
                    document.body.appendChild(textArea);
                    textArea.focus();
                    textArea.select();
                    
                    try {{
                        const successful = document.execCommand('copy');
                        if (successful) {{
                            alert("✅ ¡Reporte copiado!");
                        }} else {{
                            alert("No se pudo copiar automáticamente.");
                        }}
                    }} catch (err) {{
                        alert("Error al copiar. Intenta seleccionar el texto manualmente.");
                    }}
                    
                    document.body.removeChild(textArea);
                }})();
                </script>
            """, height=0)
            
        st.caption("Tip: Una vez copiado, ve a WhatsApp y selecciona 'Pegar'.")

if __name__ == "__main__":
    render()
