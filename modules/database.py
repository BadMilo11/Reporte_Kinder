import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

def init_state():
    # Conexión con Google Sheets (ttl=0 evita que use datos viejos en cache)
    conn = st.connection("gsheets", type=GSheetsConnection, ttl=0)
    
    clases_default = ["Saludo", "Música", "Lunch", "Arte", "Mini Ciudad", "Neuro", "Terraza", "Cuento", "Personalizado", "Despedida"]
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]

    # --- CARGAR REPORTES SEMANALES ---
    if 'reportes' not in st.session_state:
        try:
            df_rep = conn.read(worksheet="Reportes")
            if not df_rep.empty:
                # Convertimos el DataFrame de la nube al diccionario del programa
                st.session_state.reportes = df_rep.set_index('Clase').to_dict('index')
            else:
                raise Exception("Hoja vacía")
        except:
            st.session_state.reportes = {clase: {dia: "" for dia in dias} for clase in clases_default}

    # --- CARGAR ORDEN ---
    if 'orden_clases' not in st.session_state:
        try:
            df_ord = conn.read(worksheet="Orden")
            if not df_ord.empty:
                st.session_state.orden_clases = df_ord.set_index('Clase')['Posicion'].to_dict()
            else:
                raise Exception("Hoja vacía")
        except:
            st.session_state.orden_clases = {clase: i + 1 for i, clase in enumerate(clases_default)}

def save_to_disk():
    """Guarda los reportes semanales y el orden de las clases en la nube."""
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # Guardar Reportes
    df_reportes = pd.DataFrame.from_dict(st.session_state.reportes, orient='index').reset_index()
    df_reportes.rename(columns={'index': 'Clase'}, inplace=True)
    conn.update(worksheet="Reportes", data=df_reportes)
    
    # Guardar Orden
    df_orden = pd.DataFrame(list(st.session_state.orden_clases.items()), columns=['Clase', 'Posicion'])
    conn.update(worksheet="Orden", data=df_orden)

def save_to_history(fecha, texto):
    """Guarda una versión final en la pestaña de Histórico."""
    conn = st.connection("gsheets", type=GSheetsConnection)
    try:
        df_hist = conn.read(worksheet="Historico")
    except:
        df_hist = pd.DataFrame(columns=['Fecha', 'Reporte'])
    
    nuevo_registro = pd.DataFrame([{'Fecha': str(fecha), 'Reporte': texto}])
    df_hist = pd.concat([df_hist, nuevo_registro], ignore_index=True)
    df_hist = df_hist.drop_duplicates(subset=['Fecha'], keep='last')
    
    conn.update(worksheet="Historico", data=df_hist)

def get_history():
    """Trae todos los reportes archivados."""
    conn = st.connection("gsheets", type=GSheetsConnection, ttl=0)
    try:
        df_hist = conn.read(worksheet="Historico")
        return df_hist.set_index('Fecha')['Reporte'].to_dict()
    except:
        return {}

def delete_from_history(fecha):
    """Borra una fila del histórico en la nube."""
    conn = st.connection("gsheets", type=GSheetsConnection)
    try:
        df_hist = conn.read(worksheet="Historico")
        df_hist = df_hist[df_hist['Fecha'] != str(fecha)]
        conn.update(worksheet="Historico", data=df_hist)
        return True
    except:
        return False
