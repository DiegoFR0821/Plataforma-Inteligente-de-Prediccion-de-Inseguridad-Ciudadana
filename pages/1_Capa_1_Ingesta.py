import streamlit as st
import pandas as pd

st.set_page_config(page_title="Capa 1: Ingesta", page_icon="📥", layout="wide")

st.title("📥 Capa 1: Ingesta de Datos")
st.markdown("Sube el archivo CSV. Como el archivo no tiene encabezados, la plataforma los asignará automáticamente.")

archivo_subido = st.file_uploader("Arrastra tu archivo CSV aquí", type=["csv"])

if archivo_subido is not None:
    # Definimos las columnas base de tu proyecto
    columnas_proyecto = [
        'Fecha_Reporte', 'Hora_Reporte', 'Distrito', 'Tipo_Delito', 
        'Latitud', 'Longitud', 'Tiempo_Respuesta_Min', 'Uso_Arma', 
        'Captura', 'Rango_Horario'
    ]
    
    if st.button("📥 Cargar y Asignar Encabezados"):
        try:
            # header=None le dice a Pandas que el archivo no trae títulos
            # names=columnas_proyecto le asigna nuestros propios títulos
            try:
                df = pd.read_csv(archivo_subido, sep=";", header=None, names=columnas_proyecto)
                if len(df.columns) < 2:
                    archivo_subido.seek(0)
                    df = pd.read_csv(archivo_subido, sep=",", header=None, names=columnas_proyecto)
            except:
                archivo_subido.seek(0)
                df = pd.read_csv(archivo_subido, sep=",", header=None, names=columnas_proyecto)

            st.session_state['datos_crudos'] = df
            st.success("✅ ¡Archivo procesado e ingerido con éxito!")
            
        except Exception as e:
            st.error(f"Ocurrió un error: {e}")

# Si los datos ya están en memoria, mostramos la vista y los botones de navegación
if 'datos_crudos' in st.session_state:
    st.write("**Vista rápida de las primeras 5 filas con sus nuevos encabezados:**")
    st.dataframe(st.session_state['datos_crudos'].head())
    
    st.write("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Reiniciar / Limpiar Datos"):
            del st.session_state['datos_crudos']
            st.rerun()
    with col2:
        if st.button("Siguiente: Ir a Capa 2 (Staging) ➡️", use_container_width=True):
            st.switch_page("pages/2_Capa_2_Staging.py")