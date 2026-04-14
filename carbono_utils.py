# carbono_utils.py
# Módulo para cálculos de Huella de Carbono
# Basado en metodologías de Greenpeace y GHG Protocol

import pandas as pd
import numpy as np

# Factores de emisión (kg CO2e)
FACTORES_EMISION = {
    'ultraprocesada': 0.8,      # kg CO2e por unidad
    'mixta': 0.4,               # kg CO2e por unidad
    'natural': 0.1              # kg CO2e por unidad
}

# Factor de logística
FACTOR_LOGISTICA = 0.2  # kg CO2e por km por frecuencia

def calcular_huella_tienda(fila, factor_desperdicio=1.0):
    """
    Calcula la huella de carbono mensual de una tienda.
    
    Parámetros:
    -----------
    fila : dict o Series
        Datos de la tienda con columnas:
        - cantidad_ultraprocesada
        - cantidad_mixta
        - cantidad_natural
        - distancia_proveedor_km
        - frecuencia_entregas
    
    factor_desperdicio : float
        Multiplicador para simular desperdicio (default 1.0)
    
    Retorna:
    --------
    float : Huella de carbono en kg CO2e
    """
    
    # Emisiones por tipo de alimento
    emision_ultraprocesada = fila['cantidad_ultraprocesada'] * FACTORES_EMISION['ultraprocesada']
    emision_mixta = fila['cantidad_mixta'] * FACTORES_EMISION['mixta']
    emision_natural = fila['cantidad_natural'] * FACTORES_EMISION['natural']
    
    # Emisiones por logística
    emision_logistica = (fila['distancia_proveedor_km'] * FACTOR_LOGISTICA * 
                         fila['frecuencia_entregas'])
    
    # Total con factor de desperdicio
    total_emision = ((emision_ultraprocesada + emision_mixta + emision_natural + 
                      emision_logistica) * factor_desperdicio)
    
    return round(total_emision, 2)


def calcular_huellas_dataframe(df, factor_desperdicio=1.0):
    """
    Calcula la huella de carbono para todas las tiendas.
    
    Parámetros:
    -----------
    df : DataFrame
        Dataframe con datos de tiendas
    factor_desperdicio : float
        Multiplicador para desperdicio
    
    Retorna:
    --------
    DataFrame : Dataframe original con columna 'huella_carbono_kg_co2e'
    """
    
    df_copia = df.copy()
    df_copia['huella_carbono_kg_co2e'] = df_copia.apply(
        lambda fila: calcular_huella_tienda(fila, factor_desperdicio),
        axis=1
    )
    
    return df_copia


def calcular_metricas_principales(df, total_personas=2148):
    """
    Calcula las 3 métricas principales del dashboard.
    
    Parámetros:
    -----------
    df : DataFrame
        Dataframe con columna 'huella_carbono_kg_co2e'
    total_personas : int
        Total de personas en el colegio (default 2148)
    
    Retorna:
    --------
    dict : Diccionario con las métricas
    """
    
    emision_total = df['huella_carbono_kg_co2e'].sum()
    tienda_mayor_impacto = df.loc[df['huella_carbono_kg_co2e'].idxmax()]
    promedio_por_persona = emision_total / total_personas
    
    return {
        'total_emisiones': round(emision_total, 2),
        'tienda_mayor_impacto': tienda_mayor_impacto['nombre_tienda'],
        'emision_mayor_tienda': round(tienda_mayor_impacto['huella_carbono_kg_co2e'], 2),
        'promedio_por_persona': round(promedio_por_persona, 4),
        'total_personas': total_personas
    }


def generar_recomendaciones(df, umbral_emision=200):
    """
    Genera recomendaciones basadas en los datos de huella de carbono.
    
    Parámetros:
    -----------
    df : DataFrame
        Dataframe con datos y huella de carbono
    umbral_emision : float
        Umbral de kg CO2e para generar recomendaciones
    
    Retorna:
    --------
    list : Lista de recomendaciones
    """
    
    recomendaciones = []
    emision_total = df['huella_carbono_kg_co2e'].sum()
    
    # Recomendación 1: Si la huella total es alta
    if emision_total > umbral_emision * 5:
        recomendaciones.append({
            'titulo': '🌱 Reactivar la Huerta Escolar',
            'descripcion': 'Implementar un programa de cultivo de vegetales en el campus para reducir dependencia de alimentos ultraprocesados y gestionar residuos orgánicos.',
            'impacto': 'Reducción del 15-20% en emisiones'
        })
    
    # Recomendación 2: Proporción de ultraprocesados
    ultraprocesados_total = df['cantidad_ultraprocesada'].sum()
    naturales_total = df['cantidad_natural'].sum()
    total_productos = ultraprocesados_total + naturales_total
    
    if total_productos > 0:
        proporcion_ultraprocesada = ultraprocesados_total / total_productos
        if proporcion_ultraprocesada > 0.6:
            recomendaciones.append({
                'titulo': '🥗 Incrementar Opciones Naturales',
                'descripcion': 'Aumentar disponibilidad de frutas, verduras y alimentos sin procesar en las tiendas escolares.',
                'impacto': 'Reducción del 10-15% en emisiones'
            })
    
    # Recomendación 3: Logística
    tiendas_lejanas = df[df['distancia_proveedor_km'] > 20]
    if len(tiendas_lejanas) > 0:
        recomendaciones.append({
            'titulo': '🚚 Optimizar Logística y Proveedores Locales',
            'descripcion': 'Considera trabajar con proveedores más cercanos para reducir emisiones de transporte.',
            'impacto': 'Reducción del 8-12% en emisiones'
        })
    
    # Recomendación 4: Reducir plásticos
    recomendaciones.append({
        'titulo': '♻️ Reducir Plásticos de Un Solo Uso',
        'descripcion': 'Implementar empaques reutilizables y biodegradables en todas las tiendas escolares.',
        'impacto': 'Reducción del 5-8% en emisiones'
    })
    
    # Recomendación 5: Factor Medellín
    recomendaciones.append({
        'titulo': '🌳 Árboles del Campus como Sumideros de Carbono',
        'descripcion': 'El INEM posee una excelente cobertura arbórea que actúa como sumidero natural. Se estima que los árboles del campus compensan aproximadamente 50-100 kg CO2e/mes.',
        'impacto': 'Compensación natural del 10-15%'
    })
    
    return recomendaciones


def calcular_estadisticas_productos(df):
    """
    Calcula estadísticas sobre tipos de productos.
    
    Parámetros:
    -----------
    df : DataFrame
        Dataframe con datos de tiendas
    
    Retorna:
    --------
    dict : Diccionario con estadísticas
    """
    
    ultraprocesados = df['cantidad_ultraprocesada'].sum()
    mixtos = df['cantidad_mixta'].sum()
    naturales = df['cantidad_natural'].sum()
    total = ultraprocesados + mixtos + naturales
    
    estadisticas = {
        'ultraprocesados': round((ultraprocesados / total) * 100, 1) if total > 0 else 0,
        'mixtos': round((mixtos / total) * 100, 1) if total > 0 else 0,
        'naturales': round((naturales / total) * 100, 1) if total > 0 else 0,
        'total_productos': total
    }
    
    return estadisticas
