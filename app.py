import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import sys

# Importar funciones de actualización
sys.path.insert(0, '/workspaces/Dashboard_KoboToolbox')
from logica_etl import actualizar_base_datos, obtener_datos_historicos

# ==================== CONFIGURACIÓN ====================
st.set_page_config(
    page_title="Dashboard UMSA - Tienda Universitaria",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== DICCIONARIOS DE TRADUCCIÓN ====================
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
    'medicina_veterinaria_y_zootecnia': 'Medicina Veterinaria y Zootecnia',
}

# ==================== FUNCIONES DE PROCESAMIENTO ====================

@st.cache_data
def cargar_esquema():
    """Carga el esquema base del diccionario."""
    return {
        'facultades': TRADUCCION_FACULTADES,
        'carreras': TRADUCCION_CARRERAS
    }

def procesar_datos(df):
    """
    Procesa y limpia los datos.
    
    IMPORTANTE: Mantiene TODOS los registros, incluso aquellos sin carrera especificada.
    Los registros sin carrera se marcan como "Sin carrera especificada".
    """
    if df.empty:
        return df
    
    df = df.copy()
    
    # Consolidar carreras desde múltiples columnas
    cols_carrera = [c for c in df.columns if 'group_bo0sv10/_2_2_Carrera' in c and c != 'group_bo0sv10/_2_2_Carrera']
    if cols_carrera:
        df['carrera_consolidada'] = df['group_bo0sv10/_2_2_Carrera'].fillna(pd.NA)
        for col in sorted(cols_carrera):
            df['carrera_consolidada'] = df['carrera_consolidada'].fillna(df[col])
    else:
        df['carrera_consolidada'] = df['group_bo0sv10/_2_2_Carrera']
    
    # Traducir facultades
    if 'group_bo0sv10/Facultad' in df.columns:
        df['facultad_traducida'] = df['group_bo0sv10/Facultad'].map(
            lambda x: TRADUCCION_FACULTADES.get(x, x) if pd.notna(x) else 'Facultad desconocida'
        )
    else:
        df['facultad_traducida'] = 'Facultad desconocida'
    
    # Limpiar y traducir carreras
    df['carrera_consolidada'] = df['carrera_consolidada'].str.strip() if df['carrera_consolidada'].dtype == 'object' else df['carrera_consolidada']
    df['carrera_consolidada'] = df['carrera_consolidada'].map(
        lambda x: TRADUCCION_CARRERAS.get(x, x) if pd.notna(x) else None
    )
    df['facultad_traducida'] = df['facultad_traducida'].str.strip() if df['facultad_traducida'].dtype == 'object' else df['facultad_traducida']
    
    # Reemplazar carreras nulas con "Sin carrera especificada"
    df['carrera_consolidada'] = df['carrera_consolidada'].fillna('⚠️ Sin carrera especificada')
    
    # Obtener tipo de participante (estudiante vs egresado)
    if 'group_bo0sv10/Su_carrera_es_anual_o_semestra' in df.columns:
        df['tipo_participante'] = df['group_bo0sv10/Su_carrera_es_anual_o_semestra'].map({
            'egresado': 'Egresado',
            'anula': 'Estudiante',
            'semestral': 'Estudiante'
        })
    else:
        df['tipo_participante'] = 'Estudiante'
    
    # Llenar valores nulos en tipo_participante
    df['tipo_participante'] = df['tipo_participante'].fillna('Estudiante')
    
    # IMPORTANTE: NO eliminamos registros incompletos
    # Todos los registros se mantienen para análisis completo
    
    return df

def detectar_duplicados(df):
    """Detecta registros duplicados por número de registro universitario."""
    duplicados_df = df[df.duplicated(subset=['group_bo0sv10/_1_Nro_de_Registro_Universitario'], keep=False)].copy()
    duplicados_df = duplicados_df.sort_values('group_bo0sv10/_1_Nro_de_Registro_Universitario')
    return duplicados_df

# ==================== INTERFAZ PRINCIPAL ====================

# Título y controles
col_titulo, col_actualizar = st.columns([4, 1])

with col_titulo:
    st.title("📊 Dashboard UMSA - Tienda Universitaria")

with col_actualizar:
    st.write("")
    if st.button("🔄 Actualizar Datos", use_container_width=True):
        with st.spinner("Sincronizando con KoboToolbox..."):
            resultado = actualizar_base_datos()
            
            if resultado['exito']:
                st.success(resultado['mensaje'])
                st.cache_data.clear()
                st.rerun()
            else:
                st.error(resultado['mensaje'])

# Mostrar timestamp de última actualización
if os.path.exists("datos_historicos.csv"):
    timestamp = os.path.getmtime("datos_historicos.csv")
    fecha_mod = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
    st.caption(f"⏱️ Última actualización: {fecha_mod}")

st.markdown("---")

# Cargar datos
df_bruto = obtener_datos_historicos()
df = procesar_datos(df_bruto)

if df.empty:
    st.error("❌ No se encontraron registros en la base de datos.")
else:
    # ==================== PESTAÑA 1: RESUMEN GENERAL ====================
    
    tab1, tab2, tab3 = st.tabs(["📊 Resumen General", "🏫 Análisis por Facultad", "⚠️ Duplicados"])
    
    # ========== TAB 1: RESUMEN GENERAL ==========
    with tab1:
        # Métricas principales
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("📋 Total de Respuestas", f"{len(df):,}")
        col2.metric("🏫 Facultades", df['facultad_traducida'].nunique())
        col3.metric("🎓 Carreras", df['carrera_consolidada'].nunique())
        
        # Diferenciar por tipo de participante
        est_count = (df['tipo_participante'] == 'Estudiante').sum()
        egr_count = (df['tipo_participante'] == 'Egresado').sum()
        col4.metric("👥 Estudiantes/Egresados", f"{est_count}/{egr_count}")
        
        st.markdown("---")
        
        # Distribución por facultad
        st.subheader("Respuestas por Facultad")
        df_fac = df['facultad_traducida'].value_counts().reset_index()
        df_fac.columns = ['Facultad', 'Cantidad']
        df_fac = df_fac.sort_values('Cantidad', ascending=True)
        
        col_t, col_g = st.columns([1, 1.5])
        with col_t:
            st.dataframe(df_fac, use_container_width=True, hide_index=True)
        with col_g:
            fig = px.bar(df_fac, y='Facultad', x='Cantidad', orientation='h',
                        color='Cantidad', color_continuous_scale='Blues')
            fig.update_layout(showlegend=False, height=400, margin=dict(l=250))
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Distribución por carrera
        st.subheader("Respuestas por Carrera")
        df_car = df['carrera_consolidada'].value_counts().reset_index()
        df_car.columns = ['Carrera', 'Cantidad']
        df_car = df_car.sort_values('Cantidad', ascending=True)
        
        col_t2, col_g2 = st.columns([1, 1.5])
        with col_t2:
            st.dataframe(df_car.head(20), use_container_width=True, hide_index=True)
        with col_g2:
            fig2 = px.bar(df_car, y='Carrera', x='Cantidad', orientation='h',
                         color='Cantidad', color_continuous_scale='Teal')
            fig2.update_layout(showlegend=False, height=600, margin=dict(l=300))
            st.plotly_chart(fig2, use_container_width=True)
        
        st.markdown("---")
        
        # Diferenciación por tipo de participante
        st.subheader("Análisis: Estudiantes vs Egresados")
        col_e1, col_e2, col_e3 = st.columns(3)
        col_e1.metric("👨‍🎓 Estudiantes de Pregrado", est_count)
        col_e2.metric("🎖️ Egresados", egr_count)
        col_e3.metric("📊 Porcentaje Egresados", f"{(egr_count/len(df)*100):.1f}%")
        
        # Gráfico de distribución
        df_tipo = df['tipo_participante'].value_counts().reset_index()
        df_tipo.columns = ['Tipo', 'Cantidad']
        fig_tipo = px.pie(df_tipo, names='Tipo', values='Cantidad', hole=0.4,
                         title="Distribución de Participantes")
        st.plotly_chart(fig_tipo, use_container_width=True)
    
    # ========== TAB 2: ANÁLISIS POR FACULTAD ==========
    with tab2:
        st.subheader("📚 Selecciona una Facultad para ver detalles")
        
        facultades_disponibles = sorted(df['facultad_traducida'].unique())
        facultad_seleccionada = st.selectbox("Facultad:", facultades_disponibles, key="fac_select")
        
        if facultad_seleccionada:
            df_fac_filtrada = df[df['facultad_traducida'] == facultad_seleccionada]
            
            # Métricas de la facultad
            col_f1, col_f2, col_f3 = st.columns(3)
            col_f1.metric("📋 Total de Respuestas", len(df_fac_filtrada))
            col_f2.metric("🎓 Carreras", df_fac_filtrada['carrera_consolidada'].nunique())
            
            est_fac = (df_fac_filtrada['tipo_participante'] == 'Estudiante').sum()
            egr_fac = (df_fac_filtrada['tipo_participante'] == 'Egresado').sum()
            col_f3.metric("👥 Estudiantes/Egresados", f"{est_fac}/{egr_fac}")
            
            st.markdown("---")
            
            # Carreras en la facultad
            st.markdown("#### Carreras de la Facultad:")
            df_carreras = df_fac_filtrada['carrera_consolidada'].value_counts().reset_index()
            df_carreras.columns = ['Carrera', 'Respuestas']
            df_carreras = df_carreras.sort_values('Respuestas', ascending=False)
            
            col_c1, col_c2 = st.columns([1, 1.5])
            with col_c1:
                st.dataframe(df_carreras, use_container_width=True, hide_index=True)
            
            with col_c2:
                fig_c = px.bar(df_carreras, y='Carrera', x='Respuestas', orientation='h',
                              color='Respuestas', color_continuous_scale='Viridis')
                fig_c.update_layout(showlegend=False, height=400, margin=dict(l=250))
                st.plotly_chart(fig_c, use_container_width=True)
            
            st.markdown("---")
            
            # Análisis por tipo de participante
            st.markdown("#### Distribución: Estudiantes vs Egresados")
            df_tipo_fac = df_fac_filtrada['tipo_participante'].value_counts().reset_index()
            df_tipo_fac.columns = ['Tipo', 'Cantidad']
            
            fig_tipo_fac = px.bar(df_tipo_fac, x='Tipo', y='Cantidad',
                                 color='Tipo', color_discrete_map={'Estudiante': '#636EFA', 'Egresado': '#EF553B'})
            st.plotly_chart(fig_tipo_fac, use_container_width=True)
            
            st.markdown("---")
            
            # Datos de la facultad
            st.markdown("#### Datos detallados:")
            st.dataframe(df_fac_filtrada[['group_bo0sv10/_1_Nro_de_Registro_Universitario', 
                                          'facultad_traducida', 
                                          'carrera_consolidada', 
                                          'tipo_participante']].head(20), 
                        use_container_width=True, hide_index=True)
    
    # ========== TAB 3: DUPLICADOS ==========
    with tab3:
        st.subheader("⚠️ Análisis de Registros Duplicados")
        
        duplicados = detectar_duplicados(df)
        total_registros = len(df)
        registros_unicos = df['group_bo0sv10/_1_Nro_de_Registro_Universitario'].nunique()
        registros_duplicados = total_registros - registros_unicos
        
        col_d1, col_d2, col_d3, col_d4 = st.columns(4)
        col_d1.metric("📋 Total de Registros", total_registros)
        col_d2.metric("✅ Registros Únicos", registros_unicos)
        col_d3.metric("⚠️ Registros Duplicados", registros_duplicados)
        col_d4.metric("📊 % Duplicados", f"{(registros_duplicados/total_registros*100):.2f}%")
        
        st.markdown("---")
        
        if not duplicados.empty:
            st.markdown("#### Registros Duplicados por Facultad:")
            
            dup_por_fac = duplicados.groupby('facultad_traducida').size().reset_index(name='Cantidad')
            dup_por_fac = dup_por_fac.sort_values('Cantidad', ascending=False)
            
            col_d_t, col_d_g = st.columns([1, 1.5])
            with col_d_t:
                st.dataframe(dup_por_fac, use_container_width=True, hide_index=True)
            
            with col_d_g:
                fig_dup = px.bar(dup_por_fac, y='facultad_traducida', x='Cantidad', orientation='h',
                               color='Cantidad', color_continuous_scale='Reds')
                fig_dup.update_layout(showlegend=False, height=400, margin=dict(l=250))
                st.plotly_chart(fig_dup, use_container_width=True)
            
            st.markdown("---")
            
            st.markdown("#### Registros Duplicados por Carrera:")
            
            dup_por_car = duplicados.groupby('carrera_consolidada').size().reset_index(name='Cantidad')
            dup_por_car = dup_por_car.sort_values('Cantidad', ascending=False)
            
            col_d_t2, col_d_g2 = st.columns([1, 1.5])
            with col_d_t2:
                st.dataframe(dup_por_car, use_container_width=True, hide_index=True)
            
            with col_d_g2:
                fig_dup2 = px.bar(dup_por_car, y='carrera_consolidada', x='Cantidad', orientation='h',
                                color='Cantidad', color_continuous_scale='Reds')
                fig_dup2.update_layout(showlegend=False, height=500, margin=dict(l=300))
                st.plotly_chart(fig_dup2, use_container_width=True)
            
            st.markdown("---")
            
            st.markdown("#### Detalles de Duplicados:")
            st.dataframe(duplicados[['group_bo0sv10/_1_Nro_de_Registro_Universitario',
                                     'facultad_traducida',
                                     'carrera_consolidada',
                                     'tipo_participante',
                                     '_submission_time']].sort_values('group_bo0sv10/_1_Nro_de_Registro_Universitario'),
                        use_container_width=True, hide_index=True)
        else:
            st.success("✅ No se detectaron registros duplicados.")
