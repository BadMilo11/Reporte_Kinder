import streamlit as st
import streamlit.components.v1 as components

def render():
    st.subheader("📋 Reporte Final")
    
    # 1. Selección del día para generar
    dia_sel = st.selectbox("¿De qué día quieres el reporte?", 
                          ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"],
                          key="report_day_sel")

    # 2. Lógica para construir el texto
    # Ordenamos las clases según el número asignado en la Tab 2
    clases_ordenadas = sorted(st.session_state.orden_clases.items(), key=lambda x: x[1])
    
    reporte_completo = ""
    for clase, pos in clases_ordenadas:
        texto_clase = st.session_state.reportes[clase][dia_sel]
        if texto_clase.strip():  # Solo añade si no está vacío
            reporte_completo += f"*{clase}*\n{texto_clase}\n\n"

    # 3. Mostrar el resultado en un área de texto editable
    # Usamos un text_area para que ella pueda dar el último toque
    resultado_final = st.text_area(
        "Edita el reporte final si es necesario:",
        value=reporte_completo,
        height=400,
        key="final_report_area"
    )

    # 4. BOTÓN DE COPIADO (Magia de JavaScript para iPhone)
    if st.button("📱 Copiar Reporte Completo", use_container_width=True, type="primary"):
        # Escapamos los saltos de línea para que JS no rompa
        texto_para_js = resultado_final.replace("\n", "\\n").replace("'", "\\'")
        
        # Componente de JS para copiar
        components.html(f"""
            <script>
            const text = `{texto_para_js}`;
            navigator.clipboard.writeText(text).then(() => {{
                parent.postMessage({{type: 'streamlit:set_component_value', value: true}}, '*');
            }});
            alert("✅ ¡Copiado al portapapeles! Ya puedes pegarlo en WhatsApp.");
            </script>
        """, height=0)

    st.caption("Tip: Una vez copiado, ve a WhatsApp y deja presionado en el cuadro de texto para 'Pegar'.")
