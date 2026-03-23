import streamlit as st
import json
import os

# Ruta donde se guardará el archivo en el servidor de Streamlit
DATA_PATH = "data/reportes_guardados.json"

def init_state():
    clases = ["Saludo", "Música", "Lunch", "Arte", "Mini Ciudad", "Neuro", "Terraza", "Cuento", "Personalizado", "Despedida"]
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]

    # 1. Intentar cargar datos desde el archivo JSON
    if 'reportes' not in st.session_state:
        if os.path.exists(DATA_PATH):
            with open(DATA_PATH, "r", encoding="utf-8") as f:
                st.session_state.reportes = json.load(f)
        else:
            # Si el archivo no existe, inicializar vacío
            st.session_state.reportes = {clase: {dia: "" for dia in dias} for clase in clases}

    # 2. Inicializar el orden de las clases
    if 'orden_clases' not in st.session_state:
        st.session_state.orden_clases = {clase: i + 1 for i, clase in enumerate(clases)}

def save_to_disk():
    """Guarda el estado actual del diccionario en el archivo JSON"""
    # Crear carpeta data si no existe
    if not os.path.exists("data"):
        os.makedirs("data")
    
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(st.session_state.reportes, f, ensure_ascii=False, indent=4)
