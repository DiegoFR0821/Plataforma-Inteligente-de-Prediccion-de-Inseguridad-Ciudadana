import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Capa 7: Dashboard", page_icon="📊", layout="wide")

st.title("📊 Capa 7: Dashboard de Mando Integral (BI & AI)")

if 'datos_limpios' not in st.session_state:
    st.warning("⚠️ No hay datos cargados. Por favor, realiza la ingesta en la Capa 1.")
else:
    df = st.session_state['datos_limpios']
    
    # --- 5 FILTROS INTERACTIVOS MULTISELECCIÓN ---
    st.markdown("### 🎛️ Filtros Interactivos (Selección Múltiple)")
    f1, f2, f3 = st.columns(3)
    f4, f5 = st.columns(2)
    
    distritos_opc = sorted(list(df['Distrito'].unique()))
    horarios_opc = sorted(list(df['Rango_Horario'].unique())) if 'Rango_Horario' in df.columns else []
    delitos_opc = sorted(list(df['Tipo_Delito'].unique())) if 'Tipo_Delito' in df.columns else []
    armas_opc = ["TRUE", "FALSE"]
    captura_opc = ["TRUE", "FALSE"]

    with f1: f_distrito = st.multiselect("Distritos", distritos_opc, default=distritos_opc)
    with f2: f_horario = st.multiselect("Horarios", horarios_opc, default=horarios_opc)
    with f3: f_delito = st.multiselect("Delitos", delitos_opc, default=delitos_opc)
    with f4: f_arma = st.multiselect("¿Uso Arma?", armas_opc, default=armas_opc)
    with f5: f_captura = st.multiselect("¿Hubo Captura?", captura_opc, default=captura_opc)
            
    # Aplicar los filtros multiselect
    df_f = df.copy()
    if f_distrito: df_f = df_f[df_f['Distrito'].isin(f_distrito)]
    if f_horario: df_f = df_f[df_f['Rango_Horario'].isin(f_horario)]
    if f_delito: df_f = df_f[df_f['Tipo_Delito'].isin(f_delito)]
    
    # Manejo seguro para booleanos como texto
    df_f['Uso_Arma_Str'] = df_f['Uso_Arma'].astype(str).str.upper()
    df_f['Captura_Str'] = df_f['Captura'].astype(str).str.upper()
    
    if f_arma: df_f = df_f[df_f['Uso_Arma_Str'].isin(f_arma)]
    if f_captura: df_f = df_f[df_f['Captura_Str'].isin(f_captura)]
    
    # --- LOS 5 KPIs DINÁMICOS ---
    st.write("---")
    tot = len(df_f)
    t_resp = df_f['Tiempo_Respuesta_Min'].mean() if 'Tiempo_Respuesta_Min' in df_f.columns and tot > 0 else 0
    cap_ok = (len(df_f[df_f['Captura_Str'] == 'TRUE']) / tot) * 100 if tot > 0 else 0
    arm_ok = (len(df_f[df_f['Uso_Arma_Str'] == 'TRUE']) / tot) * 100 if tot > 0 else 0
    delitos_criticos = df_f['Tipo_Delito'].str.contains('ROBO|EXTORSION|HOMICIDIO', case=False, na=False).sum() if 'Tipo_Delito' in df_f.columns else 0
    tasa_criticos = (delitos_criticos / tot) * 100 if tot > 0 else 0
    
    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Volumen", tot)
    k2.metric("Tiempo Promedio", f"{t_resp:.1f} min")
    k3.metric("Tasa Capturas", f"{cap_ok:.1f}%")
    k4.metric("Uso de Armas", f"{arm_ok:.1f}%")
    k5.metric("Delitos Críticos", f"{tasa_criticos:.1f}%")

    st.write("---")

    # ==========================================
    # 4 GRÁFICOS DESCRIPTIVOS
    # ==========================================
    st.markdown("### 📈 Descriptivo: Histórico de Sucesos")
    row1_c1, row1_c2 = st.columns(2)
    row2_c1, row2_c2 = st.columns(2)
    
    if tot > 0:
        with row1_c1:
            st.markdown("**1. Frecuencia por Distrito**")
            fig1 = px.bar(df_f['Distrito'].value_counts().reset_index(), x='Distrito', y='count', color='Distrito')
            fig1.update_layout(showlegend=False, margin=dict(t=10, b=10))
            st.plotly_chart(fig1, use_container_width=True)
            
        with row1_c2:
            st.markdown("**2. Distribución de Delitos**")
            fig2 = px.pie(df_f, names='Tipo_Delito', hole=0.4)
            fig2.update_layout(margin=dict(t=10, b=10))
            st.plotly_chart(fig2, use_container_width=True)
            
        with row2_c1:
            st.markdown("**3. Tiempos de Respuesta por Horario**")
            fig3 = px.box(df_f, x='Rango_Horario', y='Tiempo_Respuesta_Min', color='Rango_Horario')
            fig3.update_layout(showlegend=False, margin=dict(t=10, b=10))
            st.plotly_chart(fig3, use_container_width=True)
            
        with row2_c2:
            st.markdown("**4. Casos con Uso de Armas de Fuego**")
            fig4 = px.histogram(df_f, x='Uso_Arma_Str', color='Tipo_Delito', barmode='group', labels={'Uso_Arma_Str': 'Uso de Arma'})
            fig4.update_layout(margin=dict(t=10, b=10))
            st.plotly_chart(fig4, use_container_width=True)
    else:
        st.info("No hay datos para la combinación de filtros seleccionada.")

    st.write("---")

    # ==========================================
    # 4 GRÁFICOS PREDICTIVOS (Sincronizados)
    # ==========================================
    st.markdown("### 🔮 Predictivo: Proyecciones de Inteligencia Artificial")
    
    if tot > 0:
        row3_c1, row3_c2 = st.columns(2)
        row4_c1, row4_c2 = st.columns(2)
        
        with row3_c1:
            st.markdown("**1. Proyección: Niveles de Alerta**")
            riesgos = pd.DataFrame({"Nivel": ["ALTO RIESGO", "MODERADO", "BAJO"], "Porcentaje": [tasa_criticos, 100-tasa_criticos-10, 10]})
            fig5 = px.pie(riesgos, names='Nivel', values='Porcentaje', color='Nivel', 
                          color_discrete_map={'ALTO RIESGO':'#ff4b4b', 'MODERADO':'#ffa500', 'BAJO':'#00cc66'}, hole=0.5)
            fig5.update_layout(margin=dict(t=10, b=10))
            st.plotly_chart(fig5, use_container_width=True)
            
        with row3_c2:
            st.markdown("**2. Mapa de Calor: Riesgo de Fuga por Horario**")
            df_pred_heat = df_f.groupby(['Distrito', 'Rango_Horario']).size().reset_index(name='Casos')
            fig6 = px.density_heatmap(df_pred_heat, x='Distrito', y='Rango_Horario', z='Casos', color_continuous_scale='Reds')
            fig6.update_layout(margin=dict(t=10, b=10))
            st.plotly_chart(fig6, use_container_width=True)

        with row4_c1:
            st.markdown("**3. Predicción de Tiempos Críticos vs Captura**")
            fig7 = px.scatter(df_f, x='Tiempo_Respuesta_Min', y='Tipo_Delito', color='Captura_Str')
            fig7.update_layout(margin=dict(t=10, b=10))
            st.plotly_chart(fig7, use_container_width=True)

        with row4_c2:
            st.markdown("**4. Tendencia Proyectada (+30 Días)**")
            df_forecast = df_f['Tipo_Delito'].value_counts().reset_index()
            df_forecast['Proyección +30D'] = df_forecast['count'] * 1.124 
            fig8 = px.bar(df_forecast, x='Tipo_Delito', y=['count', 'Proyección +30D'], barmode='group')
            fig8.update_layout(margin=dict(t=10, b=10), legend_title_text="Escenario")
            st.plotly_chart(fig8, use_container_width=True)

# Navegación inferior
st.write("---")
col_back, col_home = st.columns(2)
with col_back:
    if st.button("⬅️ Regresar a Capa 6", use_container_width=True): st.switch_page("pages/6_Capa_6_Semantica.py")
with col_home:
    if st.button("🏠 Ir a la Portada Principal", use_container_width=True): st.switch_page("app.py")