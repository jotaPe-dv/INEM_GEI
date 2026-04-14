# 🌍 HuellaCarb: Análisis de Impacto Ambiental

Aplicación de Streamlit para evaluación de la huella de carbono de las tiendas escolares del **Colegio INEM José Félix de Restrepo** en Medellín.

## 📋 Descripción

Esta aplicación proporciona un análisis exploratorio de datos (EDA) y cálculo de huella de carbono mensual en kg CO₂e (equivalentes de dióxido de carbono) basado en metodologías de **Greenpeace** y **GHG Protocol**.

### Usuarios Finales
- **Directivos:** Para tomar decisiones estratégicas de sostenibilidad
- **Profesores:** Para educación ambiental y concientización estudiantil
- **Estudiantes:** Para aprender sobre impacto ambiental

### Datos Base
- **Población Total:** 2,148 personas (2,000 estudiantes + 148 profesores)
- **Tiendas Escolares:** 7 puntos de venta
- **Período:** Análisis mensual

---

## 🔧 Requerimientos Técnicos

### Instalación

1. **Clonar el repositorio** (si aplica)
   ```bash
   git clone <repo-url>
   cd INEM_GEI
   ```

2. **Crear un ambiente virtual** (recomendado)
   ```bash
   python -m venv venv
   
   # En Windows
   venv\Scripts\activate
   
   # En macOS/Linux
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar la aplicación**
   ```bash
   streamlit run app.py
   ```

La aplicación se abrirá automáticamente en `http://localhost:8501`

---

## 📊 Lógica de Cálculo (Backend)

### Factores de Emisión

| Categoría | Factor | Unidad |
|-----------|--------|--------|
| Alimento Ultraprocesado | 0.8 | kg CO₂e/unidad |
| Alimento Mixto/Preparado | 0.4 | kg CO₂e/unidad |
| Alimento Natural | 0.1 | kg CO₂e/unidad |
| Logística | 0.2 × distancia × frecuencia | kg CO₂e/km/entrega |

### Fórmula de Cálculo

```
Huella Mensual = (
    [Ultraprocesada × 0.8] +
    [Mixta × 0.4] +
    [Natural × 0.1] +
    [Distancia_km × 0.2 × Frecuencia_entregas]
) × Factor_Desperdicio
```

### Ejemplo de Cálculo

Para la **Tienda Norte** (del dataset):
- 250 unidades ultraprocesadas: 250 × 0.8 = **200 kg CO₂e**
- 180 unidades mixtas: 180 × 0.4 = **72 kg CO₂e**
- 120 unidades naturales: 120 × 0.1 = **12 kg CO₂e**
- Logística: 15 km × 0.2 × 12 entregas = **36 kg CO₂e**
- **Total:** 200 + 72 + 12 + 36 = **320 kg CO₂e** (sin desperdicio)

---

## 🎨 Interfaz de Streamlit

### Sidebar - Controles

1. **Filtro de Tiendas:** Selecciona qué tipos de tienda visualizar
2. **Factor de Desperdicio:** Slider (0.5x a 2.5x)
   - 0.5x: Eficiencia estratosférica
   - 1.0x: Operación normal
   - 2.0x+: Desperdicio masivo

### Dashboard Principal

3 métricas clave en la parte superior:
- **📈 Emisiones Total (kg CO₂e):** Suma de todas las tiendas
- **🏢 Tienda Mayor Impacto:** Tienda con más huella
- **👤 Promedio por Estudiante:** Distribución per cápita

---

## 📉 Visualizaciones

### 1. Gráfico de Barras - Emisiones por Tienda
- Visualización comparativa interactiva
- Hover para ver valores exactos
- Escala de colores indica intensidad de emisiones

### 2. Gráfico Circular - Composición de Productos
- Proporción de alimentos Naturales vs Ultraprocesados
- Porcentaje de cada categoría
- Útil para identificar oportunidades de mejora

### 3. Gráfico de Dispersión - Ventas vs Huella
- Eje X: Ventas mensuales ($)
- Eje Y: Emisiones (kg CO₂e)
- Tamaño de burbuja: Frecuencia de entregas
- Identifica relaciones entre volumen y impacto

---

## 💡 Recomendaciones Estratégicas

La aplicación genera automáticamente recomendaciones basadas en los datos:

### 🌱 Reactivar Huerta Escolar
- **Implementar:** Cultivo de vegetales en campus
- **Objetivo:** Reducir alimentos ultraprocesados
- **Impacto:** -15-20% en emisiones

### 🥗 Incrementar Opciones Naturales
- **Implementar:** Mayor disponibilidad de frutas/verduras
- **Objetivo:** Cambiar hábitos de consumo
- **Impacto:** -10-15% en emisiones

### 🚚 Optimizar Logística
- **Implementar:** Proveedores más cercanos
- **Objetivo:** Reducir distancia de transporte
- **Impacto:** -8-12% en emisiones

### ♻️ Reducir Plásticos de Un Solo Uso
- **Implementar:** Empaques reutilizables
- **Target:** 100% de tiendas
- **Impacto:** -5-8% en emisiones

### 🌳 Factor Medellín: Árboles como Sumideros
- **Recurso:** Cobertura arbórea del campus
- **Compensación:** 50-100 kg CO₂e/mes (10-15%)
- **Teoría:** Un árbol adulto absorbe ~20 kg CO₂/año

---

## 📁 Estructura de Archivos

```
INEM_GEI/
│
├── app.py                      # Aplicación principal de Streamlit
├── carbono_utils.py            # Módulo de cálculos de huella
├── datos_tiendas_inem.csv      # Dataset de ejemplo
├── requirements.txt            # Dependencias Python
└── README.md                   # Esta documentación
```

---

## 🗂️ Descripción de Archivos

### `app.py`
Aplicación principal con:
- Interfaz de usuario interactiva
- Sidebar con filtros y configuración
- Dashboard con 3 métricas KPI
- 3 gráficos interactivos (Plotly)
- Sección de recomendaciones
- Información sobre factor Medellín

### `carbono_utils.py`
Módulo de lógica de negocio con funciones:
- `calcular_huella_tienda()`: Calcula huella individual
- `calcular_huellas_dataframe()`: Aplica a todas las tiendas
- `calcular_metricas_principales()`: KPIs del dashboard
- `generar_recomendaciones()`: Recomendaciones automáticas
- `calcular_estadisticas_productos()`: Estadísticas de composición

### `datos_tiendas_inem.csv`
Dataset de ejemplo con 7 tiendas e incluye:
- ID y nombre de tienda
- Tipo de tienda (Cafetería, Comedor, etc.)
- Cantidad de productos por categoría
- Distancia a proveedores y frecuencia de entregas
- Ventas mensuales

---

## 🚀 Despliegue en Streamlit Cloud

Para publicar la aplicación en la nube:

1. **Sube el repo a GitHub**
2. **Ve a [streamlit.io/cloud](https://streamlit.io/cloud)**
3. **Conecta tu GitHub**
4. **Selecciona el repo y archivo `app.py`**
5. **¡Listo! Tu app estará en línea**

**Nota:** Asegúrate de que `requirements.txt` esté en el root del repo.

---

## 📌 Notas Importantes

### Para Directivos
- Las visualizaciones prioritarias son gráficas, no tablas de números
- Todas las métricas están en **kg CO₂e** (kilogramos de CO₂ equivalentes)
- El "Factor de Desperdicio" simula escenarios de mejora

### Para Profesores
- Explica que 1 kg CO₂e ≈ equivalente a 1 km en automóvil
- Usa las recomendaciones para proyectos educativos
- Los árboles del campus son activos ambientales reales

### Factor Medellín
- Medellín es conocida como "Ciudad de la Primavera"
- El campus del INEM tiene cobertura arbórea significativa
- **Cada árbol compensa ~20 kg CO₂/año** (2-3 kg/mes)
- Estimación conservadora: 25-50 árboles en campus = 50-100 kg CO₂e/mes

---

## 🔄 Cómo Actualizar los Datos

1. **Edita `datos_tiendas_inem.csv`** con datos reales
2. **Recarga la aplicación** (Ctrl+R o botón de reload)
3. Los cálculos se actualizan automáticamente

---

## 🐛 Solución de Problemas

### Error: "No se encontró datos_tiendas_inem.csv"
- Verifica que el archivo esté en la misma carpeta que `app.py`
- Revisa la ruta: `C:\Users\Juan Rua\Desktop\INEM_GEI\`

### La aplicación se ejecuta muy lentamente
- Cierra otras pestañas/aplicaciones
- Reduce el "Factor de Desperdicio" si tiene muchos decimales

### Los gráficos no se muestran
- Actualiza Plotly: `pip install --upgrade plotly`

---

## 📞 Contacto y Soporte

Para preguntas sobre:
- **Cálculos:** Ver `carbono_utils.py` y comentarios
- **Interfaz:** Ver secciones en `app.py`
- **Datos:** Editar `datos_tiendas_inem.csv`

---

## 📜 Metodologías Utilizadas

- **Greenpeace:** Protocolo de transporte bajo carbono
- **GHG Protocol:** Estándares internacionales de emisiones
- **EPA:** Factores de emisión de alimentos procesados

---

## ✅ Checklist de Validación

Antes de presentar a directivos:

- [ ] Dataset `datos_tiendas_inem.csv` con datos reales
- [ ] Todos los gráficos se cargan sin errores
- [ ] Sidebar de filtros funciona correctamente
- [ ] Recomendaciones son contextuales
- [ ] Documento sobre "Factor Medellín" está visible
- [ ] Aplicación responde rápidamente

---

## 📚 Referencias

- [Streamlit Documentation](https://docs.streamlit.io)
- [Plotly Documentation](https://plotly.com/python/)
- [GHG Protocol Corporate Accounting](https://ghgprotocol.org/)
- [Greenpeace Carbon Footprint](https://www.greenpeace.org/)

---

**Última actualización:** Abril 2026
**Versión:** 1.0
**Desarrollador:** Equipo de Sostenibilidad INEM
