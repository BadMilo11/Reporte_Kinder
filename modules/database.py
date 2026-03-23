import streamlit as st

def init_state():
    # 1. Definir las clases y los días
    clases = [
        "Saludo", "Música", "Lunch", "Arte", "Mini Ciudad", 
        "Neuro", "Terraza", "Cuento", "Personalizado", "Despedida"
    ]
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]

    # 2. Inicializar el diccionario de reportes si no existe
    if 'reportes' not in st.session_state:
        # Creamos un diccionario: {Clase: {Lunes: "", Martes: "", ...}}
        st.session_state.reportes = {
            clase: {dia: "" for dia in dias} for clase in clases
        }

    # 3. Inicializar el orden de las clases (1 a 10)
    if 'orden_clases' not in st.session_state:
        st.session_state.orden_clases = {
            clase: i + 1 for i, clase in enumerate(clases)
        }
