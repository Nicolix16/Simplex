import requests
import json
import base64
from typing import Dict, Any

class GeminiAPI:
    def __init__(self, api_key: str):
        """
        Inicializar la clase GeminiAPI
        
        Args:
            api_key (str): Clave de API de Google Gemini
        """
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        self.headers = {
            'Content-Type': 'application/json',
            'X-goog-api-key': self.api_key
        }
    
    def analyze_linear_programming_problem(self, image_data: Dict[str, Any]) -> str:
        """
        Analizar un problema de programación lineal desde una imagen
        
        Args:
            image_data (Dict): Diccionario con los datos de la imagen en base64
            
        Returns:
            str: Respuesta de Gemini con el análisis y solución
        """
        
        # Prompt especializado para problemas de programación lineal
        prompt = """
        Analiza la imagen que contiene un problema de programación lineal que debe resolverse usando el método gráfico.

        INSTRUCCIONES CRÍTICAS PARA EL ANÁLISIS:
        1. Identifica TODAS las restricciones del problema, incluyendo límites inferiores (x ≥ valor)
        2. Encuentra los puntos de intersección de TODAS las restricciones
        3. Verifica la factibilidad de cada punto candidato
        4. Evalúa la función objetivo SOLO en los vértices factibles
        5. Asegúrate de que los cálculos sean matemáticamente exactos

        FORMATO DE VERIFICACIÓN:
        Para cada punto candidato (x1, x2), verifica que cumpla TODAS las restricciones:
        - Si x1 + 3x2 ≤ 200, entonces calcular x1 + 3x2 y verificar ≤ 200
        - Si x1 + x2 ≤ 100, entonces calcular x1 + x2 y verificar ≤ 100
        - Si x1 ≥ 20, entonces verificar x1 ≥ 20
        - Si x2 ≥ 10, entonces verificar x2 ≥ 10
        - Siempre verificar x1 ≥ 0 y x2 ≥ 0

        IMPORTANTE: Al final de tu respuesta, incluye una sección llamada "DATOS PARA GRÁFICA" con el siguiente formato EXACTO:

        === DATOS PARA GRÁFICA ===
        FUNCION_OBJETIVO: [Maximizar o Minimizar] Z = [coeficientes]x1 + [coeficientes]x2
        RESTRICCIONES:
        - [coef]x1 + [coef]x2 <= [valor]
        - [coef]x1 + [coef]x2 <= [valor]
        - [coef]x1 + [coef]x2 >= [valor]
        - x1 >= 0
        - x2 >= 0
        VERTICES:
        - (x1, x2) = (0, 0)
        - (x1, x2) = (valor, valor)
        - (x1, x2) = (valor, valor)
        SOLUCION_OPTIMA: (x1, x2) = (valor, valor)
        VALOR_OPTIMO: Z = valor
        === FIN DATOS ===

        Ejemplo de formato con verificación:
        === DATOS PARA GRÁFICA ===
        FUNCION_OBJETIVO: Maximizar Z = 30x1 + 50x2
        RESTRICCIONES:
        - 1x1 + 3x2 <= 200
        - 1x1 + 1x2 <= 100
        - x1 >= 20
        - x2 >= 10
        - x1 >= 0
        - x2 >= 0
        VERTICES:
        - (x1, x2) = (50, 50)
        - (x1, x2) = (20, 60)
        - (x1, x2) = (90, 10)
        - (x1, x2) = (20, 10)
        SOLUCION_OPTIMA: (x1, x2) = (50, 50)
        VALOR_OPTIMO: Z = 4000
        === FIN DATOS ===

        PASOS OBLIGATORIOS:
        1. Lee cuidadosamente TODAS las restricciones del problema
        2. Encuentra TODOS los puntos de intersección posibles
        3. Para CADA punto, verifica TODAS las restricciones matemáticamente
        4. Incluye SOLO los puntos que satisfacen TODAS las restricciones
        5. Evalúa la función objetivo en cada vértice factible
        6. Selecciona el punto con mayor (maximización) o menor (minimización) valor
        7. Revisa tus cálculos antes de dar la respuesta final

        Usa SIEMPRE el formato exacto mostrado arriba para que el programa pueda leerlo correctamente.

        Ahora resuelve el problema paso a paso con verificación matemática rigurosa.
        """
        
        # Preparar el payload para la API
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        },
                        {
                            "inline_data": {
                                "mime_type": image_data["mime_type"],
                                "data": image_data["base64_data"]
                            }
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.1,  # Baja temperatura para respuestas más precisas
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 8192
            },
            "safetySettings": [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH", 
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                }
            ]
        }
        
        try:
            # Realizar la petición a la API
            response = requests.post(
                self.base_url,
                headers=self.headers,
                data=json.dumps(payload),
                timeout=60
            )
            
            # Verificar el código de estado
            if response.status_code != 200:
                error_detail = response.text
                raise Exception(f"Error HTTP {response.status_code}: {error_detail}")
            
            # Procesar la respuesta
            response_data = response.json()
            
            if 'candidates' not in response_data or not response_data['candidates']:
                raise Exception("No se recibió respuesta válida de Gemini API")
            
            # Extraer el texto de la respuesta
            candidate = response_data['candidates'][0]
            
            if 'content' not in candidate or 'parts' not in candidate['content']:
                raise Exception("Formato de respuesta inválido")
            
            parts = candidate['content']['parts']
            if not parts or 'text' not in parts[0]:
                raise Exception("No se encontró texto en la respuesta")
            
            return parts[0]['text']
            
        except requests.exceptions.Timeout:
            raise Exception("Timeout al conectar con Gemini API")
        except requests.exceptions.ConnectionError:
            raise Exception("Error de conexión con Gemini API")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error de petición: {str(e)}")
        except json.JSONDecodeError:
            raise Exception("Error al procesar la respuesta JSON")
        except KeyError as e:
            raise Exception(f"Campo faltante en la respuesta: {str(e)}")
        except Exception as e:
            raise Exception(f"Error inesperado: {str(e)}")
    
    def test_connection(self) -> bool:
        """
        Probar la conexión con la API de Gemini
        
        Returns:
            bool: True si la conexión es exitosa, False en caso contrario
        """
        try:
            # Crear un payload simple para probar
            test_payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": "Hello, this is a test."
                            }
                        ]
                    }
                ]
            }
            
            response = requests.post(
                self.base_url,
                headers=self.headers,
                data=json.dumps(test_payload),
                timeout=30
            )
            
            return response.status_code == 200
            
        except Exception:
            return False
    
    def analyze_for_simplex_method(self, image_data: Dict[str, Any]) -> str:
        """
        Analizar un problema de programación lineal específicamente para el método Simplex
        
        Args:
            image_data (Dict): Diccionario con los datos de la imagen en base64
            
        Returns:
            str: Respuesta de Gemini con el análisis para Simplex
        """
        
        # Prompt específico para método Simplex
        prompt = """
        Analiza la imagen que contiene un problema de programación lineal que debe resolverse usando el MÉTODO SIMPLEX.

        IMPORTANTE: Tu respuesta debe incluir obligatoriamente una sección llamada "DATOS PARA SIMPLEX" con el siguiente formato EXACTO:

        === DATOS PARA SIMPLEX ===
        TIPO: [Maximizar o Minimizar]
        FUNCION_OBJETIVO: Z = [coef1]x1 + [coef2]x2
        RESTRICCIONES:
        - [coef1]x1 + [coef2]x2 <= [valor]
        - [coef1]x1 + [coef2]x2 <= [valor]
        - [coef1]x1 + [coef2]x2 >= [valor]
        - x1 >= 0
        - x2 >= 0
        VARIABLES: x1, x2
        === FIN DATOS SIMPLEX ===

        Ejemplo de formato correcto:
        === DATOS PARA SIMPLEX ===
        TIPO: Maximizar
        FUNCION_OBJETIVO: Z = 3x1 + 2x2
        RESTRICCIONES:
        - 1x1 + 1x2 <= 6
        - 2x1 + 1x2 <= 8
        - 1x1 <= 4
        - x1 >= 0
        - x2 >= 0
        VARIABLES: x1, x2
        === FIN DATOS SIMPLEX ===

        INSTRUCCIONES ESPECÍFICAS:
        1. Identifica si es un problema de MAXIMIZACIÓN o MINIMIZACIÓN
        2. Extrae la función objetivo con sus coeficientes exactos
        3. Lista TODAS las restricciones, incluyendo:
           - Restricciones principales (con ambas variables)
           - Restricciones de límite superior (x1 ≤ valor, x2 ≤ valor)
           - Restricciones de no negatividad (x1 ≥ 0, x2 ≥ 0)
           - Cualquier restricción adicional
        4. Asegúrate de que las restricciones estén en formato estándar (≤ para maximización)
        5. Usa coeficientes numéricos exactos (no uses palabras como "dos", usa "2")

        FORMATO DE RESTRICCIONES:
        - Para restricciones con ambas variables: "coefx1 + coefx2 <= valor"
        - Para restricciones con una variable: "coefx1 <= valor" o "coefx2 <= valor"
        - Para no negatividad: "x1 >= 0" y "x2 >= 0"
        - Si una restricción es ≥, déjala como está: "coefx1 + coefx2 >= valor"

        Proporciona también:
        - Análisis paso a paso del problema
        - Explicación de por qué es adecuado para el método Simplex
        - Identificación de variables de decisión
        - Preparación para la forma estándar del Simplex

        Recuerda: La sección "DATOS PARA SIMPLEX" debe aparecer AL FINAL de tu respuesta con el formato EXACTO mostrado arriba.
        """
        
        # Preparar el payload para la API
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        },
                        {
                            "inline_data": {
                                "mime_type": image_data["mime_type"],
                                "data": image_data["base64_data"]
                            }
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.1,  # Baja temperatura para respuestas más precisas
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 8192
            },
            "safetySettings": [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH", 
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                }
            ]
        }
        
        try:
            # Realizar la petición a la API
            response = requests.post(
                self.base_url,
                headers=self.headers,
                data=json.dumps(payload),
                timeout=60
            )
            
            # Verificar el código de estado
            if response.status_code != 200:
                error_detail = response.text
                raise Exception(f"Error HTTP {response.status_code}: {error_detail}")
            
            # Procesar la respuesta
            response_data = response.json()
            
            if 'candidates' not in response_data or not response_data['candidates']:
                raise Exception("No se recibió respuesta válida de Gemini API")
            
            # Extraer el texto de la respuesta
            candidate = response_data['candidates'][0]
            
            if 'content' not in candidate or 'parts' not in candidate['content']:
                raise Exception("Formato de respuesta inválido")
            
            parts = candidate['content']['parts']
            if not parts or 'text' not in parts[0]:
                raise Exception("No se encontró texto en la respuesta")
            
            return parts[0]['text']
            
        except requests.exceptions.Timeout:
            raise Exception("Timeout al conectar con Gemini API")
        except requests.exceptions.ConnectionError:
            raise Exception("Error de conexión con Gemini API")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error de petición: {str(e)}")
        except json.JSONDecodeError:
            raise Exception("Error al procesar la respuesta JSON")
        except KeyError as e:
            raise Exception(f"Campo faltante en la respuesta: {str(e)}")
        except Exception as e:
            raise Exception(f"Error inesperado: {str(e)}")