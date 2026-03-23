import streamlit as st
import json
import os

# Ruta donde se guardará el archivo en el servidor de Streamlit
DATA_PATH = "data/reportes_guardados.json"

def init_state():
    """Inicializa el estado de la aplicación y carga datos desde el disco si existen."""
    
    # Definición de la estructura base
    clases = [
        "Saludo", "Música", "Lunch", "Arte", "Mini Ciudad", 
        "Neuro", "Terraza", "Cuento", "Personalizado", "Despedida"
    ]
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]

    # 1. Lógica de carga de reportes con manejo de errores (Anti-Crash)
    if 'reportes' not in st.session_state:
        success_load = False
        
        if os.path.exists(DATA_PATH):
            try:
                with open(DATA_PATH, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if content:  # Solo procesar si el archivo no está vacío
                        st.session_state.reportes = json.loads(content)
                        success_load = True
            except (json.JSONDecodeError, ValueError):
                # Si el archivo está corrupto o mal formado, ignoramos y seguimos
                st.warning("Se detectó un archivo de datos dañado. Se iniciará una base de datos nueva.")
                pass

        # Si el archivo no existe o falló la carga, inicializar estructura vacía
        if not success_load:
            st.session_state.reportes = {
                clase: {dia: "" for dia in dias} for clase in clases
            }

    # 2. Inicializar el orden de las clases si no existe
    if 'orden_clases' not in st.session_state:
        st.session_state.orden_clases = {
            clase: i + 1 for i, clase in enumerate(clases)
        }

def save_to_disk():
    """Guarda el estado actual del diccionario de reportes en un archivo JSON."""
    try:
        # Crear la carpeta 'data' si no existe
        if not os.path.exists("data"):
            os.makedirs("data")
        
        # Guardar los datos de forma segura
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(st.session_state.reportes, f, ensure_ascii=False, indent=4)
    except Exception as e:
        st.error(f"Error al guardar en disco: {e}")

if __name__ == "__main__":
    # Prueba rápida de inicialización
    init_state()
