# Guía de Uso del Método Simplex

## Resumen

Tu aplicación ahora incluye una implementación completa del **método Simplex** además del método gráfico original. Esto te permite resolver problemas de programación lineal de forma algorítmica y comparar resultados entre ambos métodos.

## Nuevas Características Agregadas

### 1. **Nueva Pestaña "Método Simplex"**
- Análisis específico para Simplex
- Solución paso a paso con iteraciones
- Tableau detallado
- Comparación con método gráfico

### 2. **Solver Simplex Completo** (`simplex_solver.py`)
- Implementación del algoritmo Simplex estándar
- Manejo de variables de holgura automático
- Detección de soluciones óptimas y no acotadas
- Soporte para maximización y minimización
- Iteraciones detalladas con tableau

### 3. **API Gemini Extendida**
- Nuevo método `analyze_for_simplex_method()`
- Prompts especializados para extraer datos estructurados
- Formato específico para datos del Simplex

## Cómo Usar la Nueva Funcionalidad

### Paso 1: Cargar una Imagen
1. Haz clic en **"Cargar Imagen"**
2. Selecciona una imagen que contenga un problema de programación lineal
3. La imagen debe mostrar claramente la función objetivo y las restricciones

### Paso 2: Análisis con Método Gráfico (Original)
1. Ve a la pestaña **"Análisis y Solución"**
2. Haz clic en **"Analizar Problema"**
3. Espera el análisis de Gemini
4. Ve a la pestaña **"Gráfica del Método"** para ver la visualización

### Paso 3: Análisis con Método Simplex (Nuevo)
1. Ve a la pestaña **"Método Simplex"**
2. Haz clic en **"Analizar para Simplex"**
3. Espera el análisis específico para Simplex
4. Haz clic en **"Resolver con Simplex"**
5. Revisa la solución detallada con iteraciones

## Tipos de Problemas Soportados

### ✅ Formato Recomendado de Imagen:
```
Maximizar (o Minimizar): Z = 3x₁ + 2x₂

Sujeto a:
  x₁ + x₂ ≤ 6
  2x₁ + x₂ ≤ 8  
  x₁ ≤ 4
  x₁, x₂ ≥ 0
```

### ✅ Características del Solver Simplex:
- **Variables**: Hasta 10 variables de decisión
- **Restricciones**: Hasta 20 restricciones
- **Tipos de restricción**: ≤, ≥, = 
- **Optimización**: Maximización y minimización
- **Variables de holgura**: Automáticas para restricciones ≤
- **Detección**: Soluciones no acotadas y sin solución factible

## Interpretación de Resultados

### Información Mostrada:
1. **Variables de Decisión**: Valores óptimos de x₁, x₂, etc.
2. **Valor Óptimo**: Valor máximo o mínimo de la función objetivo
3. **Variables Básicas**: Variables que están en la base final
4. **Número de Iteraciones**: Cuántas iteraciones tomó encontrar la solución
5. **Tableau Final**: Matriz final del método Simplex

### Ejemplo de Salida:
```
SOLUCIÓN POR MÉTODO SIMPLEX
====================================

Tipo de problema: MAXIMIZACIÓN

VARIABLES DE DECISIÓN:
  x1 = 2.000000
  x2 = 4.000000

VALOR ÓPTIMO:
  Z = 14.000000

VARIABLES BÁSICAS FINALES:
  x2 = 4.000000
  x1 = 2.000000
  s3 = 2.000000

NÚMERO DE ITERACIONES: 2
```

## Comparación entre Métodos

| Aspecto | Método Gráfico | Método Simplex |
|---------|----------------|----------------|
| **Variables** | Máximo 2 (x₁, x₂) | Hasta 10+ |
| **Visualización** | Gráfica 2D | Tableau numérico |
| **Precisión** | Aproximada | Exacta |
| **Iteraciones** | No aplica | Detalladas |
| **Casos especiales** | Limitado | Detecta todos |
| **Educativo** | Visual intuitivo | Algorítmico |

## Archivos Agregados/Modificados

### Nuevos Archivos:
- `simplex_solver.py` - Implementación completa del Simplex
- `test_simplex.py` - Archivo de prueba y validación

### Archivos Modificados:
- `main.py` - Nueva pestaña y funcionalidad Simplex
- `gemini_api.py` - Método adicional para análisis Simplex
- `README.md` - Documentación actualizada

## Solución de Problemas Comunes

### Error: "No se encontraron datos estructurados"
- **Causa**: La imagen no contiene un formato claro de problema
- **Solución**: Asegúrate de que la imagen tenga función objetivo y restricciones claramente definidas

### Error: "Valores negativos en el lado derecho"
- **Causa**: Restricciones mal formuladas para el Simplex estándar
- **Solución**: Verifica que todas las restricciones ≤ tengan valores positivos del lado derecho

### Solución incorrecta
- **Causa**: Datos mal extraídos de la imagen
- **Solución**: Verifica el análisis en la pestaña "Método Simplex" antes de resolver

## Prueba de Funcionalidad

Para probar que todo funciona correctamente, ejecuta:
```bash
python test_simplex.py
```

Este archivo incluye varios casos de prueba que validan:
- Problemas de maximización
- Problemas de minimización  
- Parseo de restricciones
- Extracción de datos desde texto

## Ventajas de la Implementación

1. **Educativo**: Permite comparar ambos métodos
2. **Completo**: Maneja casos que el método gráfico no puede
3. **Preciso**: Resultados exactos con algoritmo estándar
4. **Detallado**: Muestra el proceso paso a paso
5. **Robusto**: Maneja errores y casos especiales
6. **Extensible**: Fácil agregar más características

¡Tu aplicación ahora es una herramienta completa para enseñar y resolver problemas de programación lineal!