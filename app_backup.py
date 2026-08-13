import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import os

# 1. CONFIGURACIÓN DE LA PÁGINA (Diseño limpio, directo y de una sola página)
st.set_page_config(page_title="Dashboard UMSA - Tienda Universitaria", layout="wide", initial_sidebar_state="collapsed")

# 2. DICCIONARIOS DE TRADUCCIÓN (Slugs -> Nombres legibles)
TRADUCCION_FACULTADES = {
    'facultad_de_ciencias_econ_mica': 'Facultad de Ciencias Económicas',
    'facultad_de_ciencias_puras_y_n': 'Facultad de Ciencias Puras y Naturales',
    'facultad_de_ingenier_a': 'Facultad de Ingeniería',
    'facultad_de_medicina__enfermer': 'Facultad de Medicina y Enfermería',
    'facultad_de_derecho_y_ciencias': 'Facultad de Derecho y Ciencias Políticas',
    'facultad_de_arquitectura__arte': 'Facultad de Arquitectura, Artes y Diseño',
    'facultad_de_humanidades_y_cien': 'Facultad de Humanidades y Ciencias de la Educación',
    'facultad_de_tecnolog_a': 'Facultad de Tecnología',
    'facultad_de_ciencias_sociales': 'Facultad de Ciencias Sociales',
    'facultad_de_agronom_a': 'Facultad de Agronomía',
    'facultad_de_odontolog_a': 'Facultad de Odontología',
    'facultad_de_ciencias_farmac_ut': 'Facultad de Ciencias Farmacéuticas y Bioquímicas',
    'facultad_de_ciencias_geol_gica': 'Facultad de Ciencias Geológicas',
}

TRADUCCION_CARRERAS = {
    'contadur_a_p_blica': 'Contaduría Pública',
    'inform_tica': 'Informática',
    'administraci_n_de_empresas': 'Administración de Empresas',
    'derecho': 'Derecho',
    'arquitectura': 'Arquitectura',
    'medicina': 'Medicina',
    'econom_a': 'Economía',
    'ciencias_de_la_comunicaci_n_social': 'Ciencias de la Comunicación Social',
    'ingenier_a_civil': 'Ingeniería Civil',
    'ling_stica_e_idiomas': 'Lingüística e Idiomas',
    'ingenier_a_industrial': 'Ingeniería Industrial',
    'odontolog_a': 'Odontología',
    'ingenier_a_electr_nica': 'Ingeniería Electrónica',
    'tecnolog_a_m_dica': 'Tecnología Médica',
    'ingenier_a_qu_mica': 'Ingeniería Química',
    'ciencias_de_la_educaci_n': 'Ciencias de la Educación',
    'electr_nica_y_telecomunicaciones': 'Electrónica y Telecomunicaciones',
    'ingenier_a_el_ctrica': 'Ingeniería Eléctrica',
    'trabajo_social': 'Trabajo Social',
    'psicolog_a': 'Psicología',
    'ciencias_pol_ticas_y_gesti_n_p_blica': 'Ciencias Políticas y Gestión Pública',
    'qu_mica_industrial': 'Química Industrial',
    'turismo': 'Turismo',
    'dise_o_gr_fico': 'Diseño Gráfico',
    'ingenier_a_agron_mica': 'Ingeniería Agronómica',
    'f_sica': 'Física',
    'electromec_nica': 'Electromecánica',
    'matem_tica': 'Matemática',
    'aeron_utica': 'Aeronáutica',
    'qu_mica_farmac_utica': 'Química Farmacéutica',
    'biolog_a': 'Biología',
    'geodesia__topograf_a_y_geom_tica': 'Geodesia, Topografía y Geomática',
    'ingenier_a_mec_nica': 'Ingeniería Mecánica',
    'enfermer_a': 'Enfermería',
    'ingenier_a_ambiental': 'Ingeniería Ambiental',
    'ingenier_a_geol_gica': 'Ingeniería Geológica',
    'mec_nica_automotriz': 'Mecánica Automotriz',
    'nutrici_n_y_diet_tica': 'Nutrición y Dietética',
    'bioqu_mica': 'Bioquímica',
    'construcciones_civiles': 'Construcciones Civiles',
    'mecatr_nica': 'Mecatrónica',
    'ciencias_de_la_informaci_n': 'Ciencias de la Información',
    'artes_pl_sticas': 'Artes Plásticas',
    'electricidad_industrial': 'Electricidad Industrial',
    'sociolog_a': 'Sociología',
    'filosof_a': 'Filosofía',
    'antropolog_a_y_arqueolog_a': 'Antropología y Arqueología',
    'ciencias_qu_micas': 'Ciencias Químicas',
    'ingenier_a_metal_rgica': 'Ingeniería Metalúrgica',
    'estad_stica': 'Estadística',
    'ingenier_a_geogr_fica': 'Ingeniería Geográfica',
    'ingenier_a_de_seguridad_industrial': 'Ingeniería de Seguridad Industrial',
    'ingenier_a_de_producci_n_industrial': 'Ingeniería de Producción Industrial',
    'ingenier_a_petrolera': 'Ingeniería Petrolera',
    'ingenier_a_de_producci_n_y_com': 'Ingeniería de Producción y Comercialización',
    'mec_nica_industrial': 'Mecánica Industrial',
    'literatura': 'Literatura',
    'historia': 'Historia',
}

# 3. CARGAR LOS DATOS
def obtener_datos():
    """Carga los datos del CSV."""
    if os.path.exists("datos_historicos.csv"):
        return pd.read_csv("datos_historicos.csv")
    return pd.DataFrame()

def procesar_datos(df):
    """Procesa y limpia los datos."""
    if df.empty:
        return df
    
    # Copiar para no afectar el original
    df = df.copy()
    
    # Consolidar carreras: usar la columna principal o cualquiera que tenga valor
    cols_carrera = [c for c in df.columns if 'group_bo0sv10/_2_2_Carrera' in c and c != 'group_bo0sv10/_2_2_Carrera']
    cols_carrera_orden = sorted(cols_carrera, key=lambda x: int(x.split('_')[-1]) if x.split('_')[-1].isdigit() else 999)
    
    # Si hay múltiples columnas de carrera, consolidarlas
    if cols_carrera_orden:
        df['carrera_consolidada'] = df['group_bo0sv10/_2_2_Carrera'].fillna(pd.NA)
        for col in cols_carrera_orden:
            df['carrera_consolidada'] = df['carrera_consolidada'].fillna(df[col])
    else:
        df['carrera_consolidada'] = df['group_bo0sv10/_2_2_Carrera']
    
    # Traducir facultades de slug a nombre legible
    if 'group_bo0sv10/Facultad' in df.columns:
        df['facultad_traducida'] = df['group_bo0sv10/Facultad'].map(
            lambda x: TRADUCCION_FACULTADES.get(x, x) if pd.notna(x) else None
        )
    
    # Eliminar espacios en blanco y traducir carreras
    df['carrera_consolidada'] = df['carrera_consolidada'].str.strip() if df['carrera_consolidada'].dtype == 'object' else df['carrera_consolidada']
    df['carrera_consolidada'] = df['carrera_consolidada'].map(
        lambda x: TRADUCCION_CARRERAS.get(x, x) if pd.notna(x) else None
    )
    df['facultad_traducida'] = df['facultad_traducida'].str.strip() if df['facultad_traducida'].dtype == 'object' else df['facultad_traducida']
    
    # Eliminar filas donde falten facultad o carrera
    df = df.dropna(subset=['facultad_traducida', 'carrera_consolidada'])
    
    return df

# Cargar y procesar datos
df_bruto = obtener_datos()
df = procesar_datos(df_bruto)

COL_FACULTAD = 'facultad_traducida'
COL_CARRERA = 'carrera_consolidada'

# 4. ENCABEZADO Y CONTROL DE ACTUALIZACIÓN
col_h1, col_h2 = st.columns([3, 1])

with col_h1:
    st.title("📊 Demanda - Tienda Universitaria UMSA")

with col_h2:
    st.write("")
    if st.button("🔄 Actualizar Datos", use_container_width=True):
        st.rerun()

st.markdown("---")

if df.empty:
    st.error("❌ No se encontraron registros en la base de datos.")
else:
    # 5. INDICADORES PRINCIPALES (Métricas claras y directas)
    total_encuestados = len(df)
    total_facultades = df[COL_FACULTAD].nunique()
    total_carreras = df[COL_CARRERA].nunique()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("📋 Total de Respuestas", f"{total_encuestados:,}")
    col2.metric("🏫 Facultades", total_facultades)
    col3.metric("🎓 Carreras", total_carreras)

    st.markdown("---")

    # 6. RESPUESTAS POR FACULTAD
    st.subheader("Cantidad de Respuestas por Facultad")
    
    df_fac = df[COL_FACULTAD].value_counts().reset_index()
    df_fac.columns = ['Facultad', 'Cantidad']
    df_fac = df_fac.sort_values('Cantidad', ascending=True)
    
    # Mostrar tabla y gráfico
    col_table, col_chart = st.columns([1, 1.5])
    
    with col_table:
        st.dataframe(df_fac, use_container_width=True, hide_index=True)
    
    with col_chart:
        fig_fac = px.bar(df_fac, y='Facultad', x='Cantidad',
                          title="Distribución por Facultad",
                          color='Cantidad',
                          color_continuous_scale='Blues',
                          orientation='h')
        fig_fac.update_traces(textposition='auto')
        fig_fac.update_layout(showlegend=False, height=400, margin=dict(l=250))
        st.plotly_chart(fig_fac, use_container_width=True)

    st.markdown("---")

    # 7. RESPUESTAS POR CARRERA
    st.subheader("Cantidad de Respuestas por Carrera")
    
    df_car = df[COL_CARRERA].value_counts().reset_index()
    df_car.columns = ['Carrera', 'Cantidad']
    df_car = df_car.sort_values('Cantidad', ascending=True)
    
    # Mostrar tabla y gráfico
    col_table2, col_chart2 = st.columns([1, 1.5])
    
    with col_table2:
        st.dataframe(df_car, use_container_width=True, hide_index=True)
    
    with col_chart2:
        fig_car = px.bar(df_car, y='Carrera', x='Cantidad',
                          title="Distribución por Carrera",
                          color='Cantidad',
                          color_continuous_scale='Teal',
                          orientation='h')
        fig_car.update_traces(textposition='auto')
        fig_car.update_layout(showlegend=False, height=600, margin=dict(l=300))
        st.plotly_chart(fig_car, use_container_width=True)

