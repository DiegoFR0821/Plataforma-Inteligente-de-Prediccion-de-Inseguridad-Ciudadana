import streamlit as st

st.set_page_config(page_title="Capa 6: Capa Semántica", page_icon="📖", layout="wide")

st.title("📖 Capa 6: Capa Semántica y Reglas de Negocio")
st.markdown("Definición de los 5 Indicadores Clave de Rendimiento (KPIs) y el diccionario de datos.")

if 'datos_limpios' not in st.session_state:
    st.warning("⚠️ Por favor, procesa los datos en las capas iniciales primero.")
else:
    df = st.session_state['datos_limpios']
    
    st.subheader("1️⃣ Los 5 KPIs del Negocio (Métricas Oficiales)")
    
    # Cálculo de los 5 KPIs
    tot = len(df)
    t_resp = df['Tiempo_Respuesta_Min'].mean() if 'Tiempo_Respuesta_Min' in df.columns else 0
    cap_ok = (len(df[df['Captura'].astype(str).str.upper() == 'TRUE']) / tot) * 100 if 'Captura' in df.columns and tot > 0 else 0
    arm_ok = (len(df[df['Uso_Arma'].astype(str).str.upper() == 'TRUE']) / tot) * 100 if 'Uso_Arma' in df.columns and tot > 0 else 0
    # Nuevo KPI 5: Delitos de Alto Impacto (Robos, Extorsiones, Homicidios)
    delitos_criticos = df['Tipo_Delito'].str.contains('ROBO|EXTORSION|HOMICIDIO', case=False, na=False).sum()
    tasa_criticos = (delitos_criticos / tot) * 100 if tot > 0 else 0
    
    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("1. Volumen de Incidentes", f"{tot}")
    k2.metric("2. Tiempo Promedio Resp.", f"{t_resp:.1f} min")
    k3.metric("3. Tasa de Capturas", f"{cap_ok:.1f} %")
    k4.metric("4. Tasa Uso de Armas", f"{arm_ok:.1f} %")
    k5.metric("5. Delitos Críticos", f"{tasa_criticos:.1f} %")

    st.write("---")
    st.subheader("2️⃣ Reglas de Negocio Aplicadas")
    st.info("📌 **Regla KPI 3 (Capturas):** Se considera éxito operativo si la tasa global supera el 45%.")
    st.info("📌 **Regla KPI 5 (Críticos):** Agrupa modalidades de alto impacto (Robo, Extorsión, Homicidio) para medir la severidad de la zona.")

    st.write("---")
    st.subheader("3️⃣ Catálogo Semántico")
    tabla_diccionario = """
    | Campo en Base de Datos | Tipo | Definición para el Usuario |
    |------------------------|------|----------------------------|
    | `Distrito` | Dimensión | Zona geográfica jurisdiccional del incidente. |
    | `Tipo_Delito` | Dimensión | Categoría penal del suceso reportado. |
    | `Rango_Horario` | Dimensión | Agrupación del día (Mañana, Tarde, Noche, Madrugada). |
    | `Tiempo_Respuesta_Min` | Hecho | Minutos desde la llamada hasta la llegada de la unidad. |
    | `Captura` / `Uso_Arma` | Hecho | Banderas booleanas (Sí/No) de efectividad y peligrosidad. |
    """
    st.markdown(tabla_diccionario)

# Navegación inferior
st.write("---")
col1, col2 = st.columns(2)
with col1:
    if st.button("⬅️ Regresar a Capa 5 (IA)", use_container_width=True): st.switch_page("pages/5_Capa_5_IA_Predictiva.py")
with col2:
    if st.button("Siguiente: Ir a Capa 7 (Dashboard) ➡️", use_container_width=True): st.switch_page("pages/7_Capa_7_Dashboard.py")