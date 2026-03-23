import streamlit as st
from modules.database import init_state
from tabs import content_tab, order_tab, report_tab

# Configuración para iPhone (Layout centrado)
st.set_page_config(page_title="Reportes Preescolar", layout="centered")

# Inicializar datos
init_state()

st.title("🍎 Diario de Clase")

# Crear los Tabs
t1, t2, t3 = st.tabs(["📝 Redacción", "🔢 Orden", "📋 Generar"])

with t1:
    content_tab.render()

with t2:
    order_tab.render()

with t3:
    report_tab.render()
