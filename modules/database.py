import streamlit as st
import json
import os

# Ruta donde se guardará el archivo en el servidor de Streamlit
DATA_PATH = "data/reportes_guardados.json"

def init_state():
    clases = ["Saludo", "Música", "Lunch", "Arte", "Mini Ciudad", "Neuro", "Terraza", "Cuento", "Personalizado", "Despedida"]
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]

    if 'reportes' not in st.session_state:
        success_load = False
        if os.path.exists(DATA_PATH):
            try:
                with open(DATA_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # Cargamos reportes
                    st.session_state.reportes = data.get("reportes", {clase: {dia: "" for dia in dias} for clase in clases})
                    # Cargamos orden
                    st.session_state.orden_clases = data.get("orden", {clase: i + 1 for i, clase in enumerate(clases)})
                    success_load = True
            except:
                pass
        
        if not success_load:
            st.session_state.reportes = {clase: {dia: "" for dia in dias} for clase in clases}
            st.session_state.orden_clases = {clase: i + 1 for i, clase in enumerate(clases)}

def save_to_disk():
    if not os.path.exists("data"):
        os.makedirs("data")
    
    # Guardamos AMBOS diccionarios en el mismo JSON
    payload = {
        "reportes": st.session_state.reportes,
        "orden": st.session_state.orden_clases
    }
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    # Prueba rápida de inicialización
    init_state()
