import streamlit as st
from modules.database import save_to_disk

def render():
    st.subheader("🔢 Orden de las Clases")
    st.info("Define el orden en que aparecerán las clases en el reporte final.")

    # Crear una copia para manipular
    clases = list(st.session_state.orden_clases.keys())
    
    # Diccionario temporal para guardar nuevas posiciones
    nuevas_posiciones = {}

    for clase in clases:
        pos_actual = st.session_state.orden_clases[clase]
        nueva_pos = st.number_input(
            f"Posición para {clase}:", 
            min_value=1, 
            max_value=len(clases), 
            value=int(pos_actual),
            key=f"order_{clase}"
        )
        nuevas_posiciones[clase] = nueva_pos

    # Botón para aplicar y subir a Google Sheets
    if st.button("💾 Guardar Orden en la Nube", use_container_width=True, type="primary"):
        st.session_state.orden_clases = nuevas_posiciones
        save_to_disk() # Aquí es donde se envía al Excel
        st.success("✅ Orden actualizado y guardado correctamente.")
        st.rerun()

    # Mostrar vista previa del orden actual
    st.divider()
    st.markdown("**Vista previa del orden:**")
    orden_ordenado = sorted(st.session_state.orden_clases.items(), key=lambda x: x[1])
    for clase, pos in orden_ordenado:
        st.write(f"{pos}. {clase}")

if __name__ == "__main__":
    render()
