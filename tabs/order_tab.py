import streamlit as st
from modules.database import save_to_disk

def render():
    st.subheader("🔢 Orden del Reporte")
    st.info("Cambia el número de una clase y las demás se ajustarán automáticamente. El orden se guarda al instante.")

    # Obtenemos el orden actual del estado
    orden_actual = st.session_state.orden_clases
    clases = list(orden_actual.keys())

    # Creamos una copia para trabajar los cambios
    nuevo_orden = orden_actual.copy()
    cambio_detectado = False

    # Generamos los selectores para cada clase
    for clase in clases:
        # El selector muestra el valor que tiene actualmente en memoria
        valor_seleccionado = st.selectbox(
            f"Posición para: {clase}",
            options=list(range(1, len(clases) + 1)),
            index=orden_actual[clase] - 1,
            key=f"sel_{clase}"
        )

        # LÓGICA DE INTERCAMBIO (SWAP)
        if valor_seleccionado != orden_actual[clase]:
            clase_a_desplazar = ""
            # Buscamos quién ocupaba el lugar al que queremos movernos
            for c, v in orden_actual.items():
                if v == valor_seleccionado and c != clase:
                    clase_a_desplazar = c
                    break
            
            # Intercambiamos posiciones
            if clase_a_desplazar:
                nuevo_orden[clase_a_desplazar] = orden_actual[clase]
            
            nuevo_orden[clase] = valor_seleccionado
            cambio_detectado = True

    # Si hubo un cambio, actualizamos sesión, guardamos en disco y refrescamos
    if cambio_detectado:
        st.session_state.orden_clases = nuevo_orden
        save_to_disk()
        st.rerun()

    # Visualización limpia del orden resultante
    st.divider()
    st.write("**Vista previa del orden final:**")
    clases_ordenadas = sorted(st.session_state.orden_clases.items(), key=lambda x: x[1])
    for clase, pos in clases_ordenadas:
        st.write(f"{pos}. {clase}")

if __name__ == "__main__":
    render()
