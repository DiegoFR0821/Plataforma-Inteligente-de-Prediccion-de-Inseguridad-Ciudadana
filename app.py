import streamlit as st

# Configuración principal de la página
st.set_page_config(
    page_title="NightWatch BI - Cloud",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Plataforma Integral de Analítica Predictiva - NightWatch BI")
st.markdown("""
Bienvenido a la versión Cloud de la Plataforma de Seguridad Ciudadana. 
Esta plataforma implementa la arquitectura de **7 capas** para el procesamiento de Big Data y Business Intelligence, integrando modelos de Machine Learning.

👈 **Usa el menú lateral para navegar por las capas del proyecto:**
* **1. Capa 1 - Ingesta:** Carga del archivo CSV de fuentes de datos.
* **2. Capa 2 - Staging:** Zona de aterrizaje y previsualización de datos crudos.
* **3. Capa 3 - ETL:** Limpieza, estandarización y transformación.
* **4. Capa 4 - DWH:** Construcción del Data Warehouse (Modelo Copo de Nieve).
* **5. Capa 5 - IA Predictiva:** Motor de inferencia y proyecciones de riesgo.
* **6. Capa 6 - Semántica:** Diccionario de datos y cálculo de los 5 KPIs de Negocio.
* **7. Capa 7 - Dashboard:** Cuadro de mando integral interactivo (Descriptivo y Predictivo).
""")

st.write("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.info("💡 Comienza subiendo tu dataset de pruebas en la Capa 1.")
    if st.button("🚀 Iniciar Plataforma: Ir a Capa 1 (Ingesta)", use_container_width=True):
        st.switch_page("pages/1_Capa_1_Ingesta.py")