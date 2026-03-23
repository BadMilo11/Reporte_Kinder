import streamlit as st

def render():
    st.subheader("🔢 Orden del Reporte")
    st.info("Cambia el número de una clase y las demás se ajustarán automáticamente.")

    # Obtenemos el diccionario de orden actual
    orden_actual = st.session_state.orden_clases
    clases = list(orden_actual.keys())

    # Creamos una copia para comparar cambios
    nuevo_orden = orden_actual.copy()

    # Generamos los selectores para cada clase
    for clase in clases:
        # El selector muestra el valor actual
        valor_seleccionado = st.selectbox(
            f"Posición para: {clase}",
            options=range(1, len(clases) + 1),
            index=orden_actual[clase] - 1,
            key=f"sel_{clase}"
        )

        # LÓGICA DE INTERCAMBIO (SWAP)
        if valor_seleccionado != orden_actual[clase]:
            # 1. Identificar qué clase tenía el número que acabamos de elegir
            clase_a_desplazar = ""
            for c, v in orden_actual.items():
                if v == valor_seleccionado and c != clase:
                    clase_a_desplazar = c
                    break
            
            # 2. Hacer el intercambio: 
            # La clase desplazada toma la posición vieja de la clase actual
            if clase_a_desplazar:
                nuevo_orden[clase_a_desplazar] = orden_actual[clase]
            
            # 3. La clase actual toma su nuevo valor
            nuevo_orden[clase] = valor_seleccionado
            
            # 4. Actualizar el estado global y refrescar
            st.session_state.orden_clases = nuevo_orden
            st.rerun()

    # Visualización del orden final
    st.divider()
    st.write("**Vista previa del orden:**")
    # Ordenamos la lista para mostrarla bonita
    clases_ordenadas = sorted(st.session_state.orden_clases.items(), key=lambda x: x[1])
    for clase, pos in clases_ordenadas:
        st.write(f"{pos}. {clase}")
