# Resolvedor de Programación Lineal con IA

Una aplicación con interfaz gráfica que utiliza la API de Google Gemini para resolver problemas de programación lineal mediante el **método gráfico** y el **método Simplex** a partir de imágenes.

## 📋 Características Principales

- **Análisis de imágenes con IA**: Carga imágenes de problemas de programación lineal
- **Google Gemini 2.0 Flash**: Análisis automático inteligente de problemas
- **Método gráfico**: Resuelve problemas de 2 variables paso a paso 
- **Método Simplex completo**: Implementación robusta del algoritmo Simplex
- **Comparación dual**: Compara soluciones entre método gráfico y Simplex
- **Interfaz moderna**: GUI con tkinter organizada en pestañas intuitivas
- **Múltiples formatos**: Acepta PNG, JPG, JPEG, GIF, BMP, WEBP
- **Optimización automática**: Redimensiona imágenes grandes automáticamente
- **Iteraciones detalladas**: Muestra cada paso del algoritmo Simplex
- **Forma estándar**: Conversión automática a forma estándar con explicación

## ✨ Novedades Recientes

### 🆕 Funcionalidades Agregadas:
- ✅ **Método `get_standard_form_explanation`**: Explicación detallada de conversión a forma estándar
- ✅ **Mejor manejo de errores**: Detección y corrección automática de problemas
- ✅ **Soporte ampliado**: Hasta 10 variables y 20 restricciones
- ✅ **Optimización de código**: Mejor rendimiento y estabilidad

## 🚀 Instalación

### Prerrequisitos

- Python 3.11 o superior
- Una API key de Google Gemini (gratuita en [Google AI Studio](https://makersuite.google.com/app/apikey))

### Pasos de instalación

1. **Clonar o descargar el proyecto**
   ```bash
   cd "c:\Users\USUARIO\OneDrive\Documentos\opti\lab IA"
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Obtener API Key de Gemini**
   - Ve a [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Crea una cuenta si no la tienes
   - Genera una nueva API key
   - Copia la API key

## 🎯 Uso

### Ejecutar la aplicación

```bash
python main.py
```

### Pasos para usar

1. **Configurar API Key**
   - Al abrir la aplicación, ingresa tu API key de Gemini en el campo correspondiente
   - Haz clic en "Guardar" (la API key se guarda de forma segura)

2. **Cargar imagen**
   - Haz clic en "Cargar Imagen"
   - Selecciona una imagen que contenga un problema de programación lineal
   - La imagen debe mostrar claramente:
     - Función objetivo
     - Variables de decisión
     - Restricciones
     - Condiciones de no negatividad

3. **Método Gráfico**
   - Ve a la pestaña "Análisis y Solución"
   - Haz clic en "Analizar Problema"
   - Espera mientras la IA procesa la imagen
   - Los resultados aparecerán en el panel de texto
   - Ve a la pestaña "Gráfica del Método" para ver la visualización

4. **Método Simplex**
   - Ve a la pestaña "Método Simplex"
   - Haz clic en "Analizar para Simplex"
   - Espera el análisis específico para Simplex
   - Haz clic en "Resolver con Simplex"
   - Revisa la solución detallada con iteraciones

### Ejemplo de imagen válida

La imagen debe contener un problema como:

```
Maximizar: Z = 3x₁ + 2x₂

Sujeto a:
x₁ + x₂ ≤ 4
2x₁ + x₂ ≤ 6
x₁ ≥ 0, x₂ ≥ 0
```

## 📁 Estructura del proyecto

```
Simplex/
├── main.py                 # 🎯 Interfaz gráfica principal (Tkinter)
├── simplex_solver.py       # 🧮 Implementación completa del método Simplex
├── gemini_api.py          # 🤖 Integración con Google Gemini API
├── image_processor.py     # 🖼️ Procesamiento y optimización de imágenes
├── config.py             # ⚙️ Configuración y manejo de API keys
├── requirements.txt      # 📦 Dependencias del proyecto
├── README.md            # 📋 Documentación principal
├── GUIA_SIMPLEX.md      # 📚 Guía detallada del método Simplex
└── ejemplos/            # 📷 Imágenes de ejemplo para pruebas
    ├── ejemplo.jpg
    └── ejemplo2.jpg
```

### 🔍 Descripción de Archivos Principales

#### `simplex_solver.py` (Núcleo del proyecto)
- **Clase**: `SimplexSolver`
- **Métodos principales**:
  - `solve()`: Algoritmo Simplex completo
  - `parse_problem()`: Análisis de problemas desde texto
  - `get_standard_form_explanation()`: Explicación de forma estándar
  - `get_iteration_summary()`: Resumen de iteraciones
- **Capacidades**: Hasta 10 variables, 20 restricciones, detección de casos especiales

#### `main.py` (Interfaz de usuario)
- **Framework**: Tkinter con diseño por pestañas
- **Pestañas disponibles**:
  1. **Configuración**: API key y carga de imágenes
  2. **Análisis y Solución**: Método gráfico con IA
  3. **Gráfica del Método**: Visualización de soluciones
  4. **Método Simplex**: Algoritmo Simplex paso a paso

## 🧮 Características del Método Simplex

### Funcionalidades implementadas:
- **Forma estándar**: Convierte automáticamente problemas a forma estándar
- **Tableau inicial**: Genera el tableau inicial con variables de holgura
- **Iteraciones**: Ejecuta el algoritmo Simplex paso a paso
- **Regla de Dantzig**: Usa la regla de Dantzig para seleccionar variable entrante
- **Prueba del cociente**: Implementa la prueba del cociente mínimo
- **Detección de casos especiales**: Identifica soluciones no acotadas
- **Formato detallado**: Muestra todas las iteraciones y el tableau final

### Tipos de problemas soportados:
- Maximización y minimización
- Restricciones ≤, ≥, =
- Variables de holgura automáticas
- Variables no negativas
- Hasta 10 variables y 20 restricciones

## 🔧 Configuración avanzada

### Formatos de imagen soportados
- PNG (recomendado para texto claro)
- JPEG/JPG
- GIF
- BMP
- WEBP

### Limitaciones técnicas
- Tamaño máximo de imagen: 5MB
- Dimensiones máximas recomendadas: 1920x1080
- La imagen debe tener texto legible

### Personalización

Puedes modificar la configuración editando `config.py`:

- **Tamaño máximo de imagen**: Modifica `max_file_size` en `ImageProcessor`
- **Prompt de IA**: Edita el prompt en `gemini_api.py` para ajustar el análisis
- **Formatos soportados**: Añade más formatos en `supported_formats`

## 🔄 Estado del Proyecto

### ✅ Últimas Correcciones (Octubre 2025)
- **Problema resuelto**: Error `AttributeError: 'SimplexSolver' object has no attribute 'get_standard_form_explanation'`
- **Método agregado**: `get_standard_form_explanation()` completamente implementado
- **Funcionalidad**: Genera explicaciones detalladas de la conversión a forma estándar
- **Estabilidad**: Código completamente funcional sin errores conocidos

### 🚀 Estado Actual
- ✅ **Funcionando**: Todas las funcionalidades operativas
- ✅ **Probado**: Sin errores en ejecución
- ✅ **Actualizado**: Última versión en repositorio GitHub
- ✅ **Documentado**: README completo y actualizado

## 🐛 Solución de problemas

### Error: "Import could not be resolved"
```bash
# Asegúrate de que estás en el directorio correcto
cd "c:\Users\USUARIO\OneDrive\Documentos\opti\lab IA"
# Verifica que todas las dependencias estén instaladas
pip install -r requirements.txt
```

### Error: "Error HTTP 403"
- Verifica que tu API key de Gemini sea válida
- Asegúrate de que la API key tenga permisos para usar Gemini 2.0 Flash

### Error: "El archivo es demasiado grande"
- Reduce el tamaño de la imagen
- Usa una herramienta de compresión de imágenes
- Convierte a formato PNG o JPEG

### Error: "No se puede analizar la imagen"
- Verifica que la imagen contenga texto claro y legible
- Asegúrate de que el problema esté completo (función objetivo, restricciones)
- Usa imágenes con buena resolución y contraste

## 📚 Ejemplo completo

### 1. Prepara tu imagen
Crea o toma una foto de un problema como:

```
Problema: Una empresa produce dos tipos de productos A y B.

Maximizar: Utilidad = 5A + 3B

Restricciones:
- Tiempo de máquina: 2A + B ≤ 100
- Materia prima: A + 2B ≤ 80
- Demanda A: A ≤ 40
- No negatividad: A ≥ 0, B ≥ 0

Resolver usando método gráfico.
```

### 2. Resultado esperado
La IA debería proporcionar:
- Identificación de variables (A, B)
- Función objetivo: Max Z = 5A + 3B
- Lista de restricciones
- Procedimiento del método gráfico paso a paso
- Vértices de la región factible
- Evaluación de la función objetivo en cada vértice
- Solución óptima con interpretación

## 🎯 Comparación de Métodos

| Característica | Método Gráfico | Método Simplex |
|----------------|----------------|----------------|
| **Variables máximas** | 2 (x₁, x₂) | 10+ variables |
| **Restricciones** | Limitadas | 20+ restricciones |
| **Visualización** | Gráfica 2D intuitiva | Tableau numérico |
| **Precisión** | Aproximada (visual) | Exacta (algorítmica) |
| **Casos especiales** | Limitado | Detecta todos |
| **Iteraciones** | No muestra proceso | Paso a paso detallado |
| **Educativo** | Muy visual | Proceso algorítmico |

## 🔧 Uso Avanzado

### Método Simplex - Características:
- ✅ Maximización y minimización
- ✅ Variables de holgura automáticas  
- ✅ Detección de soluciones no acotadas
- ✅ Tableau completo con iteraciones
- ✅ Manejo de restricciones ≤, ≥, =
- ✅ Hasta 10 variables de decisión
- ✅ Verificación de optimalidad

### Ejemplo de Salida Simplex:
```
SOLUCIÓN POR MÉTODO SIMPLEX
====================================
Tipo de problema: MAXIMIZACIÓN

VARIABLES DE DECISIÓN:
  x1 = 2.000000
  x2 = 4.000000

VALOR ÓPTIMO:
  Z = 14.000000

NÚMERO DE ITERACIONES: 2
```

## 📊 Archivos del Proyecto

```
Optimization-Solver-with-Graphic-Method-And-AI/
├── main.py              # Interfaz gráfica principal (4 pestañas)
├── gemini_api.py        # API de Gemini (2 métodos de análisis)
├── image_processor.py   # Procesamiento de imágenes
├── simplex_solver.py    # ⭐ NUEVO: Implementación Simplex completa
├── config.py           # Configuración y API key
├── test_simplex.py     # ⭐ NUEVO: Pruebas del Simplex
├── requirements.txt    # Dependencias
├── GUIA_SIMPLEX.md     # ⭐ NUEVO: Guía detallada del Simplex
└── README.md          # Documentación principal
```

## 🚀 Novedades de Esta Versión

### ✨ Nuevas Características:
1. **Pestaña Método Simplex**: Interfaz dedicada al Simplex
2. **Solver Simplex Completo**: Algoritmo estándar implementado
3. **Análisis Dual**: Compara método gráfico vs Simplex
4. **Iteraciones Detalladas**: Ve cada paso del algoritmo
5. **Manejo Avanzado**: Restricciones ≥, variables de exceso
6. **Detección de Casos**: Soluciones no acotadas, sin solución factible

### 🎓 Valor Educativo:
- **Para Estudiantes**: Entiende ambos métodos visualmente
- **Para Profesores**: Herramienta completa de enseñanza  
- **Para Profesionales**: Solver robusto para problemas reales

## 🤝 Contribuir

Si encuentras errores o quieres mejorar la aplicación:

1. Reporta issues describiendo el problema
2. Propón mejoras en la funcionalidad
3. Comparte ejemplos de problemas que no se resuelven correctamente

## 📄 Licencia

Este proyecto es de uso educativo y personal. La API de Gemini tiene sus propios términos de uso.

## ⚡ Comandos rápidos

```bash
# Instalar y ejecutar
pip install -r requirements.txt
python main.py

# Verificar instalación
python -c "import requests, PIL; print('Dependencias OK')"

# Limpiar archivos temporales (opcional)
python -c "import os, glob; [os.remove(f) for f in glob.glob('*_optimized.jpg')]"
```

---

**Nota**: Asegúrate de tener una conexión a internet estable para usar la API de Gemini. La primera ejecución puede tomar más tiempo mientras se cargan las librerías.