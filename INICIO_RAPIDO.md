# 🚀 Guía de Inicio Rápido

## Instalación (Primero ejecutar)

### Opción 1: Windows (Recomendado)

1. **Abre PowerShell o CMD**
   ```
   cd Desktop\INEM_GEI
   ```

2. **Crea un ambiente virtual**
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Instala las dependencias**
   ```
   pip install -r requirements.txt
   ```

4. **Ejecuta la aplicación**
   ```
   streamlit run app.py
   ```

--- 

## ⚡ Uso Individual de la Aplicación

Una vez que ejecutes `streamlit run app.py`:

1. ✅ Se abrirá automáticamente en http://localhost:8501
2. ✅ Ve al **Sidebar izquierdo**
3. ✅ **Selecciona tipos de tienda** (puedes elegir múltiples)
4. ✅ **Ajusta el slider de desperdicio** (0.5x a 2.5x)
5. ✅ Los gráficos se actualizan automáticamente

---

## 📊 Interpretación Rápida para Directivos

### Métrica 1: Emisiones Total (kg CO2e)
- **¿Qué significa?** La "huella de carbono" combinada de todas las tiendas en el mes
- **Comparación:** 1 kg CO₂ equivale a 1 km en auto

### Métrica 2: Tienda Mayor Impacto
- **¿Qué significa?** Cuál tienda genera más contaminación
- **Acción:** Enfoca mejoras ahí primero

### Métrica 3: Promedio por Estudiante
- **¿Qué significa?** Si dividimos toda la huella entre 2,148 personas
- **Comparación:** ¿Es justo o alto?

---

## 🎨 Los 3 Gráficos Explicados

### Gráfico 1: Barras (Emisiones por Tienda)
- **Cada barra** = Una tienda
- **Altura** = Más alto = Más contaminación
- **Cómo mejorar:** Reduce el tipo de producto que causa más daño

### Gráfico 2: Circular (Composición)
- **Rojo** = Ultraprocesados (muy malo)
- **Amarillo** = Mixtos (regular)
- **Verde** = Naturales (bueno)
- **Objetivo:** Hacer el gráfico más verde

### Gráfico 3: Dispersión (Ventas vs Huella)
- **Eje horizontal (X)** = Cuánto venden en dinero
- **Eje vertical (Y)** = Cuánto contaminan
- **Análisis:** ¿Vender más siempre = más contaminación?

---

## 💡 Recomendaciones Clave

La app sugiere 5+ acciones. Las principales:

| # | Recomendación | Impacto | Dificultad |
|---|---|---|---|
| 1 | Huerta escolar | Alto | Media |
| 2 | Más alimentos naturales | Medio | Baja |
| 3 | Proveedores locales | Medio | Media |
| 4 | Menos plásticos | Bajo | Baja |
| 5 | Aprovechar árboles del campus | Alto | Nula |

---

## 📋 Estructura de Archivos

```
INEM_GEI/
├── app.py                    ← AQUÍ: Ejecuta esto
├── carbono_utils.py          ← Cálculos automáticos
├── datos_tiendas_inem.csv    ← Datos (editable)
├── requirements.txt          ← Dependencias
├── README.md                 ← Guía completa
├── FACTOR_MEDELLIN.md        ← Documento teórico
└── INICIO_RAPIDO.md          ← Esta guía
```

---

## 🔧 Troubleshooting

### "Error: ModuleNotFoundError: No module named 'streamlit'"
→ Faltó instalar: `pip install -r requirements.txt`

### "Error: datos_tiendas_inem.csv no se encontró"
→ Verifica que el archivo esté en la misma carpeta que `app.py`

### "La app va lenta"
→ Cierra otras aplicaciones o reduce el Factor de Desperdicio

### "No me abre el navegador"
→ Abre manualmente: http://localhost:8501

---

## 📞 Contacto

Para soporte técnico, revisa:
- README.md (documentación completa)
- FACTOR_MEDELLIN.md (ciencia detrás de árboles)
- Comentarios en app.py y carbono_utils.py

