import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from carbono_utils import (
    calcular_huellas_dataframe,
    calcular_metricas_principales,
    generar_recomendaciones,
    calcular_estadisticas_productos
)

# ============================================================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================================================

st.set_page_config(
    page_title="Huella de Carbono - INEM GEI",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para mejorar la estética
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 8px;
        text-align: center;
    }
    .metric-value {
        font-size: 28px;
        font-weight: bold;
        color: #1f77b4;
    }
    .metric-label {
        font-size: 14px;
        color: #666;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# TÍTULO Y ENCABEZADO
# ============================================================================

st.title("🌍 HuellaCarb: Análisis de Impacto Ambiental")
st.markdown("### Colegio INEM José Félix de Restrepo - Medellín")
st.markdown(
    "Evaluación del impacto ambiental de las tiendas escolares "
    "basado en metodologías de **Greenpeace** y **GHG Protocol**"
)

# ============================================================================
# CARGA DE DATOS
# ============================================================================

try:
    df = pd.read_csv('datos_tiendas_inem.csv')
except FileNotFoundError:
    st.error("❌ Error: No se encontró el archivo 'datos_tiendas_inem.csv'")
    st.stop()

# ============================================================================
# SIDEBAR: FILTROS Y CONFIGURACIÓN
# ============================================================================

st.sidebar.markdown("## ⚙️ Configuración")
st.sidebar.markdown("---")

# Filtro por tipo de tienda
tipos_tienda = df['tipo_tienda'].unique()
tiendas_seleccionadas = st.sidebar.multiselect(
    "Selecciona tipos de tienda:",
    tipos_tienda,
    default=tipos_tienda,
    help="Utiliza Ctrl+Click para seleccionar múltiples opciones"
)

# Slider para Factor de Desperdicio
factor_desperdicio = st.sidebar.slider(
    "🗑️ Factor de Desperdicio",
    min_value=0.5,
    max_value=2.5,
    value=1.0,
    step=0.1,
    help="Ajusta este factor para simular diferentes escenarios de desperdicio"
)

st.sidebar.info(
    f"📊 **Factor Actual:** {factor_desperdicio}x\n\n"
    "- 0.5x: Desperdicio muy bajo (eficiente)\n"
    "- 1.0x: Condiciones normales\n"
    "- 2.0x+: Alto desperdicio"
)

# ============================================================================
# FILTRAR DATOS
# ============================================================================

df_filtrado = df[df['tipo_tienda'].isin(tiendas_seleccionadas)].copy()

# Validar que hay datos seleccionados
if len(df_filtrado) == 0:
    st.warning("⚠️ Por favor, selecciona al menos un tipo de tienda en el sidebar para ver los análisis.")
    st.stop()

# Calcular huella de carbono
df_filtrado = calcular_huellas_dataframe(df_filtrado, factor_desperdicio)

# ============================================================================
# MÉTRICAS PRINCIPALES (KPIs)
# ============================================================================

st.markdown("## 📊 Métricas Principales")

metricas = calcular_metricas_principales(df_filtrado)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="📈 Emisiones Total (kg CO2e)",
        value=f"{metricas['total_emisiones']:,.0f}",
        delta="Mes Actual",
        help="Huella de carbono total de todas las tiendas seleccionadas"
    )

with col2:
    st.metric(
        label="🏢 Tienda Mayor Impacto",
        value=metricas['tienda_mayor_impacto'],
        delta=f"{metricas['emision_mayor_tienda']} kg CO2e",
        help="Tienda con la mayor huella de carbono"
    )

with col3:
    st.metric(
        label="👤 Promedio por Estudiante (kg CO2e)",
        value=f"{metricas['promedio_por_persona']:.4f}",
        delta=f"De {metricas['total_personas']} personas",
        help="Huella de carbono por persona en el colegio"
    )

st.markdown("---")

# ============================================================================
# SECCIÓN DE VISUALIZACIONES
# ============================================================================

st.markdown("## 📈 Análisis Visual")

# Fila 1: Gráfico de barras y gráfico circular
col_grafico1, col_grafico2 = st.columns(2)

with col_grafico1:
    st.markdown("### Emisiones por Tienda")
    
    # Gráfico de barras - Emisiones por tienda
    fig_barras = px.bar(
        df_filtrado,
        x='nombre_tienda',
        y='huella_carbono_kg_co2e',
        color='huella_carbono_kg_co2e',
        color_continuous_scale='Reds',
        labels={
            'nombre_tienda': 'Tienda',
            'huella_carbono_kg_co2e': 'Emisiones (kg CO2e)',
            'tipo_tienda': 'Tipo de Tienda'
        },
        hover_name='nombre_tienda',
        hover_data={
            'tipo_tienda': True,
            'huella_carbono_kg_co2e': ':.2f',
            'nombre_tienda': False
        }
    )
    
    fig_barras.update_layout(
        height=400,
        showlegend=False,
        hovermode='x unified',
        font=dict(size=11)
    )
    
    st.plotly_chart(fig_barras, use_container_width=True)

with col_grafico2:
    st.markdown("### Composición de Productos (Colegio)")
    
    # Gráfico circular - Proporción de productos
    estadisticas = calcular_estadisticas_productos(df_filtrado)
    
    fig_pie = go.Figure(data=[go.Pie(
        labels=['Ultraprocesados', 'Mixtos/Preparados', 'Naturales'],
        values=[
            estadisticas['ultraprocesados'],
            estadisticas['mixtos'],
            estadisticas['naturales']
        ],
        marker=dict(colors=['#ff6b6b', '#ffd93d', '#6bcf7f']),
        textposition='inside',
        textinfo='label+percent',
        hovertemplate='<b>%{label}</b><br>%{percent}<extra></extra>'
    )])
    
    fig_pie.update_layout(
        height=400,
        font=dict(size=12),
        showlegend=True
    )
    
    st.plotly_chart(fig_pie, use_container_width=True)

# Fila 2: Gráfico de dispersión
col_grafico3 = st.columns(1)[0]

with col_grafico3:
    st.markdown("### Relación: Ventas vs Huella de Carbono")
    
    fig_scatter = px.scatter(
        df_filtrado,
        x='ventas_mensuales',
        y='huella_carbono_kg_co2e',
        size='frecuencia_entregas',
        color='tipo_tienda',
        hover_name='nombre_tienda',
        hover_data={
            'ventas_mensuales': '$,.0f',
            'huella_carbono_kg_co2e': ':.2f',
            'tipo_tienda': True,
            'frecuencia_entregas': True
        },
        labels={
            'ventas_mensuales': 'Ventas Mensuales ($)',
            'huella_carbono_kg_co2e': 'Emisiones (kg CO2e)',
            'tipo_tienda': 'Tipo Tienda',
            'frecuencia_entregas': 'Freq. Entregas'
        },
        title="Tamaño de la burbuja = Frecuencia de entregas"
    )
    
    fig_scatter.update_layout(
        height=400,
        hovermode='closest',
        font=dict(size=11)
    )
    
    st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("---")

# ============================================================================
# TABLA DE DETALLES (CON OPCIÓN DE OCULTAR)
# ============================================================================

with st.expander("📋 Ver Detalles de Tiendas", expanded=False):
    # Preparar datos para la tabla
    df_tabla = df_filtrado[[
        'nombre_tienda', 'tipo_tienda', 'cantidad_ultraprocesada',
        'cantidad_mixta', 'cantidad_natural', 'huella_carbono_kg_co2e'
    ]].copy()
    
    df_tabla.columns = [
        'Tienda', 'Tipo', 'Ultraprocesados', 'Mixtos', 'Naturales', 'Emisiones (kg CO2e)'
    ]
    
    # Mostrar tabla con formato personalizado
    st.dataframe(
        df_tabla,
        use_container_width=True,
        hide_index=True
    )

# ============================================================================
# SECCIÓN DE RECOMENDACIONES
# ============================================================================

st.markdown("## 💡 Recomendaciones Estratégicas")

recomendaciones = generar_recomendaciones(df_filtrado)

for i, rec in enumerate(recomendaciones, 1):
    with st.container():
        col_num, col_content = st.columns([0.5, 9.5])
        
        with col_num:
            st.markdown(f"**#{i}**")
        
        with col_content:
            st.markdown(f"### {rec['titulo']}")
            st.markdown(f"{rec['descripcion']}")
            st.info(f"💚 **Impacto Potencial:** {rec['impacto']}")

# ============================================================================
# INFORMACIÓN SOBRE MEDELLÍN Y FACTOR AMBIENTAL
# ============================================================================

st.markdown("---")
st.markdown("## 🌳 Factor Medellín: Biodiversidad del Campus")

info_col1, info_col2 = st.columns(2)

with info_col1:
    st.markdown("""
    ### Teoría de Sumidero de Carbono
    
    El Colegio INEM cuenta con una **excelente cobertura arbórea** que actúa 
    como sumidero natural de carbono. La biodiversidad del campus contribuye a:
    
    - **Absorción de CO2:** Un árbol adulto absorbe ~20-25 kg CO2/año
    - **Compensación:** Los árboles del INEM compensan aproximadamente 
      **50-100 kg CO2e/mes**
    - **Impacto Total:** Esto representa una compensación del **10-15%** 
      de la huella calculada
    """)

with info_col2:
    st.success("""
    ### Datos del Campus INEM
    
    ✅ **Ubicación:** Medellín (Ciudad de la Primavera)
    
    ✅ **Biodiversidad:** Clima tropical-subtropical
    
    ✅ **Cobertura Verde:** Árboles nativos y ornamentales
    
    ✅ **Beneficio Ambiental:** Mejora de calidad del aire
    
    💚 **Compensación Estimada:** +50-100 kg CO2e/mes
    """)

# ============================================================================
# PIE DE PÁGINA
# ============================================================================

st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; font-size: 12px; margin-top: 20px;'>
    <p>
        Aplicación de Análisis de Huella de Carbono | INEM José Félix de Restrepo
        <br/>
        Basado en metodologías de <b>Greenpeace</b> y <b>GHG Protocol</b>
        <br/>
        © 2024 - Análisis Ambiental Escolar
    </p>
    </div>
""", unsafe_allow_html=True)
