import streamlit as st

st.set_page_config(page_title="Capa 2: Staging", page_icon="🗄️", layout="wide")

st.title("🗄️ Capa 2: Staging Area (Zona de Aterrizaje)")

if 'datos_crudos' not in st.session_state:
    st.warning("⚠️ No hay datos en el Staging Area. Por favor, ve a la Capa 1.")
else:
    df = st.session_state['datos_crudos']
    
    if st.button("📊 Analizar Datos Crudos"):
        st.success("✅ Análisis completado.")
        col1, col2, col3 = st.columns(3)
        col1.metric(label="Total de Registros", value=df.shape[0])
        col2.metric(label="Total de Columnas", value=df.shape[1])
        col3.metric(label="Valores Nulos Totales", value=df.isnull().sum().sum())
        
        st.subheader("🔍 Explorador Completo de Datos")
        st.dataframe(df, use_container_width=True)

    # Navegación
    st.write("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Regresar a Capa 1 (Ingesta)", use_container_width=True):
            st.switch_page("pages/1_Capa_1_Ingesta.py")
    with col2:
        if st.button("Siguiente: Ir a Capa 3 (ETL) ➡️", use_container_width=True):
            st.switch_page("pages/3_Capa_3_ETL.py")