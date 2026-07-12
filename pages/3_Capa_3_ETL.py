import streamlit as st
import pandas as pd

st.set_page_config(page_title="Capa 3: ETL", page_icon="⚙️", layout="wide")

st.title("⚙️ Capa 3: Proceso ETL (Transformación)")

if 'datos_crudos' not in st.session_state:
    st.warning("⚠️ Faltan datos. Regresa a la Capa 1.")
else:
    df_crudo = st.session_state['datos_crudos'].copy()
    st.info(f"Registros pendientes de limpieza: {df_crudo.shape[0]}")
    
    # Botón de acción explícito para ejecutar el ETL
    if st.button("⚙️ Ejecutar Proceso de Limpieza (ETL)"):
        with st.spinner('Procesando...'):
            df_limpio = df_crudo.drop_duplicates()
            
            columnas_para_nulos = [col for col in ['Distrito', 'Tipo_Delito'] if col in df_limpio.columns]
            if columnas_para_nulos:
                df_limpio = df_limpio.dropna(subset=columnas_para_nulos) 
            
            for col in ['Distrito', 'Tipo_Delito']:
                if col in df_limpio.columns:
                    df_limpio[col] = df_limpio[col].astype(str).str.upper().str.strip()
                
            if 'Tiempo_Respuesta_Min' in df_limpio.columns:
                df_limpio['Tiempo_Respuesta_Min'] = pd.to_numeric(df_limpio['Tiempo_Respuesta_Min'], errors='coerce').fillna(0).astype(int)

        st.session_state['datos_limpios'] = df_limpio
        st.success("✅ ETL finalizado. Datos estandarizados.")
        st.dataframe(df_limpio.head(10), use_container_width=True)

    # Navegación
    st.write("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Regresar a Capa 2", use_container_width=True):
            st.switch_page("pages/2_Capa_2_Staging.py")
    with col2:
        if st.button("Siguiente: Ir a Capa 4 (DWH) ➡️", use_container_width=True):
            st.switch_page("pages/4_Capa_4_DWH.py")