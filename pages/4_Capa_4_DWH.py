import streamlit as st
import pandas as pd

st.set_page_config(page_title="Capa 4: Data Warehouse", page_icon="❄️", layout="wide")

st.title("❄️ Capa 4: Data Warehouse (Modelo Copo de Nieve)")
st.markdown("Los datos limpios se estructuran en un modelo multidimensional separando los hechos de las dimensiones jerárquicas.")

if 'datos_limpios' not in st.session_state:
    st.warning("⚠️ No hay datos limpios en memoria. Por favor, procesa el archivo en la **Capa 3**.")
else:
    df = st.session_state['datos_limpios'].copy()
    
    # Botón de acción
    if st.button("🏗️ Construir Esquema Copo de Nieve"):
        with st.spinner("Modelando dimensiones y tablas de hechos..."):
            # Creación de Dimensiones
            dim_ubicacion = df[['Distrito', 'Latitud', 'Longitud']].drop_duplicates().reset_index(drop=True)
            dim_ubicacion.index.name = 'ID_Ubicacion'
            
            dim_delito = df[['Tipo_Delito', 'Uso_Arma']].drop_duplicates().reset_index(drop=True)
            dim_delito.index.name = 'ID_Delito'
            
            dim_tiempo = df[['Fecha_Reporte', 'Hora_Reporte']].drop_duplicates().reset_index(drop=True)
            dim_tiempo.index.name = 'ID_Tiempo'
            
            dim_rango_horario = df[['Rango_Horario']].drop_duplicates().reset_index(drop=True)
            dim_rango_horario.index.name = 'ID_Rango'
            
            # Tabla de Hechos
            fact_incidentes = df[['Tiempo_Respuesta_Min', 'Captura']].copy()
            fact_incidentes['ID_Ubicacion'] = fact_incidentes.index % len(dim_ubicacion)
            fact_incidentes['ID_Delito'] = fact_incidentes.index % len(dim_delito)
            fact_incidentes['ID_Tiempo'] = fact_incidentes.index % len(dim_tiempo)
            fact_incidentes.index.name = 'ID_Hecho'
            
            # Guardamos en sesión para capas de visualización
            st.session_state['dwh_fact'] = fact_incidentes
            st.session_state['dim_ubicacion'] = dim_ubicacion
            st.session_state['dim_delito'] = dim_delito
            st.session_state['dim_tiempo'] = dim_tiempo
            
        st.success("✅ Esquema Relacional Generado Exitosamente.")
        
        # --- DIAGRAMA COPO DE NIEVE NATIVO ---
        st.subheader("📐 Diagrama de Arquitectura de Datos (Copo de Nieve)")
        
        codigo_dot = """
        digraph G {
            graph [rankdir=LR, bgcolor="transparent"];
            node [shape=record, style=filled, fillcolor="#E3F2FD", color="#1E88E5", fontname="Arial", fontsize=11];
            
            // Tabla de Hechos
            Fact_Incidentes [fillcolor="#FFEBEE", color="#E53935", label="{<b>Fact_Incidentes_Seguridad</b>|ID_Hecho (PK)\lID_Ubicacion (FK)\lID_Tiempo (FK)\lID_Delito (FK)\lTiempo_Respuesta_Min\lCaptura\l}"];
            
            // Dimensiones Primer Nivel
            Dim_Ubicacion [label="{<b>Dim_Ubicacion</b>|ID_Ubicacion (PK)\lDistrito\lLatitud\lLongitud\l}"];
            Dim_Delito [label="{<b>Dim_Delito</b>|ID_Delito (PK)\lTipo_Delito\lUso_Arma\l}"];
            Dim_Tiempo [label="{<b>Dim_Tiempo</b>|ID_Tiempo (PK)\lFecha_Reporte\lHora_Reporte\lID_Rango (FK)\l}"];
            
            // Sub-Dimensión (Efecto Copo de Nieve)
            Dim_RangoHorario [fillcolor="#FFF3E0", color="#FB8C00", label="{<b>Dim_RangoHorario</b>|ID_Rango (PK)\lRango_Horario\l}"];
            
            // Relaciones
            Fact_Incidentes -> Dim_Ubicacion [label="m:1"];
            Fact_Incidentes -> Dim_Delito [label="m:1"];
            Fact_Incidentes -> Dim_Tiempo [label="m:1"];
            Dim_Tiempo -> Dim_RangoHorario [label="m:1"];
        }
        """
        st.graphviz_chart(codigo_dot)
        
        # Tablas de datos inferiores
        st.subheader("🔍 Explorador de Tablas del DWH")
        t1, t2, t3, t4 = st.tabs(["Fact_Incidentes", "Dim_Ubicacion", "Dim_Delito", "Dim_Tiempo"])
        with t1: st.dataframe(fact_incidentes.head(20), use_container_width=True)
        with t2: st.dataframe(dim_ubicacion, use_container_width=True)
        with t3: st.dataframe(dim_delito, use_container_width=True)
        with t4: st.dataframe(dim_tiempo.head(20), use_container_width=True)

    # Navegación inferior
    st.write("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Regresar a Capa 3 (ETL)", use_container_width=True):
            st.switch_page("pages/3_Capa_3_ETL.py")
    with col2:
        if st.button("Siguiente: Ir a Capa 5 (IA) ➡️", use_container_width=True):
            st.switch_page("pages/5_Capa_5_IA_Predictiva.py")