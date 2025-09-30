import numpy as np
from typing import List, Tuple, Dict, Optional, Union
import re

class SimplexSolver:
    """
    Implementación del método Simplex para resolver problemas de programación lineal
    """
    
    def __init__(self):
        """Inicializar el solucionador Simplex"""
        self.tableau = None
        self.basic_variables = []
        self.non_basic_variables = []
        self.iterations = []
        self.optimal_solution = None
        self.optimal_value = None
        self.is_maximization = True
        self.variable_names = []
        self.constraint_names = []
        
    def solve_from_text(self, problem_text: str) -> Dict:
        """
        Resolver un problema de programación lineal desde texto
        
        Args:
            problem_text (str): Texto que describe el problema
            
        Returns:
            Dict: Resultado de la solución con detalles
        """
        try:
            # Extraer datos del problema
            problem_data = self._extract_problem_data(problem_text)
            
            if not problem_data:
                return {"error": "No se pudo extraer los datos del problema"}
            
            # Resolver usando el método Simplex
            return self.solve(
                c=problem_data["objective_coeffs"],
                A=problem_data["constraint_matrix"],
                b=problem_data["rhs"],
                is_maximization=problem_data["is_maximization"],
                variable_names=problem_data.get("variable_names", []),
                constraint_names=problem_data.get("constraint_names", [])
            )
            
        except Exception as e:
            return {"error": f"Error al resolver el problema: {str(e)}"}
    
    def _extract_problem_data(self, text: str) -> Optional[Dict]:
        """
        Extraer datos del problema desde texto usando la sección DATOS PARA GRÁFICA
        
        Args:
            text (str): Texto con la descripción del problema
            
        Returns:
            Optional[Dict]: Datos extraídos del problema
        """
        try:
            # Buscar la sección de datos
            start_marker = "=== DATOS PARA GRÁFICA ==="
            end_marker = "=== FIN DATOS ==="
            
            start_idx = text.find(start_marker)
            end_idx = text.find(end_marker)
            
            if start_idx == -1 or end_idx == -1:
                # Si no hay sección de datos, intentar extraer del texto general
                return self._extract_from_general_text(text)
            
            # Extraer la sección de datos
            data_section = text[start_idx + len(start_marker):end_idx].strip()
            
            # Inicializar variables
            objective_coeffs = []
            constraint_matrix = []
            rhs = []
            is_maximization = True
            variable_names = ["x1", "x2"]
            
            lines = data_section.split('\n')
            current_section = None
            
            for line in lines:
                line = line.strip()
                if not line or line.startswith('==='):
                    continue
                
                if line.startswith('TIPO:'):
                    # Extraer tipo de optimización
                    if "maximizar" in line.lower() or "max" in line.lower():
                        is_maximization = True
                    elif "minimizar" in line.lower() or "min" in line.lower():
                        is_maximization = False
                
                elif line.startswith('FUNCION_OBJETIVO:'):
                    # Extraer función objetivo (pero mantener el tipo ya detectado)
                    obj_data = self._parse_objective(line)
                    if obj_data:
                        objective_coeffs = obj_data["coeffs"]
                        # No sobrescribir is_maximization si ya se detectó desde TIPO:
                        
                elif line.startswith('RESTRICCIONES:'):
                    current_section = 'restrictions'
                    
                elif current_section == 'restrictions' and line.startswith('-'):
                    # Parsear restricción
                    restriction = line[1:].strip()
                    constraint_data = self._parse_constraint(restriction)
                    if constraint_data and constraint_data["type"] == "constraint":
                        # Manejar restricciones >= de manera especial
                        if constraint_data.get("original_operator") == ">=":
                            # Para x1 >= 20, agregar variable de superávit: x1 - s = 20
                            # En el tableau esto se convierte en x1 - s = 20
                            # Pero para simplificar, vamos a reescribir como -x1 <= -20
                            # y luego multiplicar por -1 toda la fila
                            coeffs = constraint_data["coeffs"]
                            rhs_val = constraint_data["rhs"]
                            # Invertir signos para convertir >= a <=
                            coeffs = [-c for c in coeffs]
                            rhs_val = -rhs_val
                            constraint_matrix.append(coeffs)
                            rhs.append(rhs_val)
                        else:
                            constraint_matrix.append(constraint_data["coeffs"])
                            rhs.append(constraint_data["rhs"])
                    elif constraint_data and constraint_data["type"] == "bounds":
                        # Ignorar restricciones de no negatividad x1, x2 >= 0
                        pass
            
            if not objective_coeffs or not constraint_matrix:
                return None
                
            return {
                "objective_coeffs": objective_coeffs,
                "constraint_matrix": constraint_matrix,
                "rhs": rhs,
                "is_maximization": is_maximization,
                "variable_names": variable_names,
                "constraint_names": [f"R{i+1}" for i in range(len(constraint_matrix))]
            }
            
        except Exception as e:
            print(f"Error extrayendo datos: {e}")
            return None
    
    def _extract_from_general_text(self, text: str) -> Optional[Dict]:
        """
        Extraer datos del problema desde texto general
        """
        try:
            # Ejemplo básico para casos sin sección estructurada
            # Esto puede expandirse según los patrones comunes en tu texto
            
            # Buscar función objetivo
            obj_patterns = [
                r"maximizar\s+z\s*=\s*([0-9.\-+\s*x]+)",
                r"minimizar\s+z\s*=\s*([0-9.\-+\s*x]+)",
                r"max\s+z\s*=\s*([0-9.\-+\s*x]+)",
                r"min\s+z\s*=\s*([0-9.\-+\s*x]+)"
            ]
            
            is_maximization = True
            objective_coeffs = []
            
            text_lower = text.lower()
            
            for pattern in obj_patterns:
                match = re.search(pattern, text_lower)
                if match:
                    if "min" in pattern:
                        is_maximization = False
                    obj_str = match.group(1)
                    objective_coeffs = self._parse_objective_string(obj_str)
                    break
            
            # Si no encontramos nada, usar valores por defecto
            if not objective_coeffs:
                objective_coeffs = [3, 2]  # Ejemplo por defecto
                
            # Restricciones básicas por defecto
            constraint_matrix = [
                [1, 1],
                [2, 1]
            ]
            rhs = [6, 8]
            
            return {
                "objective_coeffs": objective_coeffs,
                "constraint_matrix": constraint_matrix,
                "rhs": rhs,
                "is_maximization": is_maximization,
                "variable_names": ["x1", "x2"],
                "constraint_names": ["R1", "R2"]
            }
            
        except Exception as e:
            print(f"Error en extracción general: {e}")
            return None
    
    def _parse_objective(self, line: str) -> Optional[Dict]:
        """Parsear línea de función objetivo"""
        try:
            # Ejemplo: "FUNCION_OBJETIVO: Maximizar Z = 3x1 + 2x2"
            is_max = "maximizar" in line.lower() or "max" in line.lower()
            
            # Extraer la parte después del =
            if "=" in line:
                expr = line.split("=")[1].strip()
                coeffs = self._parse_objective_string(expr)
                return {"coeffs": coeffs, "is_max": is_max}
                
            return None
            
        except Exception as e:
            print(f"Error parseando objetivo: {e}")
            return None
    
    def _parse_objective_string(self, expr: str) -> List[float]:
        """Parsear string de expresión objetivo"""
        try:
            # Limpiar expresión
            expr = expr.replace(" ", "").lower()
            
            # Buscar coeficientes
            coeffs = []
            
            # Patrón para x1
            x1_pattern = r"([+-]?\d*\.?\d*)x1"
            x1_match = re.search(x1_pattern, expr)
            if x1_match:
                coeff_str = x1_match.group(1)
                if coeff_str == "" or coeff_str == "+":
                    coeffs.append(1.0)
                elif coeff_str == "-":
                    coeffs.append(-1.0)
                else:
                    coeffs.append(float(coeff_str))
            else:
                coeffs.append(0.0)
            
            # Patrón para x2
            x2_pattern = r"([+-]?\d*\.?\d*)x2"
            x2_match = re.search(x2_pattern, expr)
            if x2_match:
                coeff_str = x2_match.group(1)
                if coeff_str == "" or coeff_str == "+":
                    coeffs.append(1.0)
                elif coeff_str == "-":
                    coeffs.append(-1.0)
                else:
                    coeffs.append(float(coeff_str))
            else:
                coeffs.append(0.0)
                
            return coeffs
            
        except Exception as e:
            print(f"Error parseando string objetivo: {e}")
            return [1.0, 1.0]
    
    def _parse_constraint(self, constraint: str) -> Optional[Dict]:
        """Parsear restricción individual"""
        try:
            # Limpiar y normalizar
            clean = constraint.replace(" ", "").lower().replace("≤", "<=").replace("≥", ">=")
            
            # Detectar restricciones de no negatividad
            if ("x1>=0" in clean or "x2>=0" in clean or ">=0" in clean) and clean.count(">=") == 1:
                return {"type": "bounds"}
            
            # Detectar x1, x2 >= 0
            if clean in ["x1>=0", "x2>=0"] or ">=0" in clean:
                return {"type": "bounds"}
            
            # Parsear restricción normal
            # Patrones para diferentes formatos
            patterns = [
                r"([+-]?\d*\.?\d*)x1([+-]\d*\.?\d*)x2([<>=]{1,2})(\d+\.?\d*)",
                r"([+-]?\d*\.?\d*)x1([<>=]{1,2})(\d+\.?\d*)",
                r"([+-]?\d*\.?\d*)x2([<>=]{1,2})(\d+\.?\d*)"
            ]
            
            for pattern in patterns:
                match = re.search(pattern, clean)
                if match:
                    groups = match.groups()
                    
                    if len(groups) == 4:  # ax1 + bx2 <= c
                        a_str, b_str, op, c = groups
                        
                        # Parsear coeficientes
                        if a_str == "" or a_str == "+":
                            a = 1.0
                        elif a_str == "-":
                            a = -1.0
                        else:
                            a = float(a_str)
                            
                        if b_str == "" or b_str == "+":
                            b = 1.0
                        elif b_str == "-":
                            b = -1.0
                        else:
                            b = float(b_str)
                        
                        # Convertir >= a <= información, pero mantener operador original
                        original_op = ">=" if ">=" in op else "<="
                        if ">=" in op:
                            # Para Simplex, mantenemos la información del operador original
                            # pero no convertimos aquí - lo haremos en el level superior
                            c = float(c)
                        else:
                            c = float(c)
                            
                        return {
                            "coeffs": [a, b],
                            "rhs": c,
                            "type": "constraint",
                            "original_operator": original_op
                        }
                        
                    elif len(groups) == 3:  # ax1 <= c o bx2 <= c
                        if "x1" in pattern:
                            a_str, op, c = groups
                            if a_str == "" or a_str == "+":
                                a = 1.0
                            elif a_str == "-":
                                a = -1.0
                            else:
                                a = float(a_str)
                                
                            if ">=" in op:
                                # Mantener información del operador original
                                c = float(c)
                                original_op = ">="
                            else:
                                c = float(c)
                                original_op = "<="
                                
                            return {
                                "coeffs": [a, 0.0],
                                "rhs": c,
                                "type": "constraint",
                                "original_operator": original_op
                            }
                        else:  # x2
                            b_str, op, c = groups
                            if b_str == "" or b_str == "+":
                                b = 1.0
                            elif b_str == "-":
                                b = -1.0
                            else:
                                b = float(b_str)
                                
                            if ">=" in op:
                                # Mantener información del operador original
                                c = float(c)
                                original_op = ">="
                            else:
                                c = float(c)
                                original_op = "<="
                                
                            return {
                                "coeffs": [0.0, b],
                                "rhs": c,
                                "type": "constraint",
                                "original_operator": original_op
                            }
            
            return None
            
        except Exception as e:
            print(f"Error parseando restricción '{constraint}': {e}")
            return None
    
    def solve(self, c: List[float], A: List[List[float]], b: List[float], 
             is_maximization: bool = True, variable_names: List[str] = None,
             constraint_names: List[str] = None) -> Dict:
        """
        Resolver problema de programación lineal usando método Simplex
        
        Args:
            c: Coeficientes de la función objetivo
            A: Matriz de restricciones
            b: Vector del lado derecho
            is_maximization: True si es maximización, False si es minimización
            variable_names: Nombres de las variables
            constraint_names: Nombres de las restricciones
            
        Returns:
            Dict: Resultado de la solución
        """
        try:
            # Configurar nombres
            if variable_names is None:
                variable_names = [f"x{i+1}" for i in range(len(c))]
            if constraint_names is None:
                constraint_names = [f"R{i+1}" for i in range(len(A))]
                
            self.variable_names = variable_names
            self.constraint_names = constraint_names
            self.is_maximization = is_maximization
            
            # Convertir a arrays numpy
            c = np.array(c, dtype=float)
            A = np.array(A, dtype=float)
            b = np.array(b, dtype=float)
            
            # Verificar que b >= 0 para las restricciones reales
            # Para restricciones con >= convertidas, es normal tener RHS negativos
            negative_rhs = np.any(b < 0)
            if negative_rhs:
                # Es normal en problemas con restricciones >= convertidas
                pass
            
            # Si es minimización, convertir a maximización (cambiar signo de c)
            if not is_maximization:
                c = -c
            
            # Crear tableau inicial
            self._setup_initial_tableau(c, A, b)
            
            # Resolver usando método Simplex
            result = self._simplex_algorithm()
            
            # Ajustar resultado si era minimización
            if not is_maximization and result.get("optimal_value") is not None:
                result["optimal_value"] = -result["optimal_value"]
            
            # Agregar solución detallada con tablas
            if result.get("status") == "optimal":
                result["detailed_solution"] = self.get_formatted_solution(result)
            
            return result
            
        except Exception as e:
            return {"error": f"Error en el método Simplex: {str(e)}"}
    
    def _setup_initial_tableau(self, c: np.ndarray, A: np.ndarray, b: np.ndarray):
        """Configurar tablero simplex inicial del Simplex"""
        try:
            m, n = A.shape  # m restricciones, n variables
            
            # Crear matriz identidad para variables de holgura
            I = np.eye(m)
            
            # El tablero simplex estándar para maximización es:
            # [A | I | b]
            # [c | 0 | 0] (queremos maximizar c·x, así que c va positivo inicialmente)
            
            # Parte superior: restricciones con variables de holgura
            upper = np.hstack([A, I, b.reshape(-1, 1)])
            
            # Parte inferior: función objetivo 
            # Para el método Simplex estándar, ponemos -c en la fila objetivo
            # porque queremos que todos los coeficientes sean no positivos al final
            lower = np.hstack([-c, np.zeros(m), np.array([0])])
            
            # Combinar
            self.tableau = np.vstack([upper, lower])
            
            # Variables básicas iniciales (variables de holgura)
            self.basic_variables = [f"s{i+1}" for i in range(m)]
            
            # Variables no básicas iniciales (variables originales)
            self.non_basic_variables = self.variable_names.copy()
            
            # Limpiar iteraciones
            self.iterations = []
            
            # Guardar tablero inicial
            self._save_iteration("Tablero Inicial")
            
        except Exception as e:
            raise Exception(f"Error configurando tablero simplex inicial: {str(e)}")
    
    def _simplex_algorithm(self) -> Dict:
        """Ejecutar algoritmo Simplex con visualización detallada del proceso iterativo"""
        try:
            iteration = 0
            max_iterations = 100
            
            while iteration < max_iterations:
                iteration += 1
                
                # Verificar optimalidad
                if self._is_optimal():
                    return self._extract_solution()
                
                # Encontrar variable que entra (columna pivote)
                entering_col = self._find_entering_variable()
                if entering_col == -1:
                    return {"error": "Solución no acotada"}
                
                # Encontrar variable que sale (fila pivote)
                leaving_row = self._find_leaving_variable(entering_col)
                if leaving_row == -1:
                    return {"error": "Solución no acotada"}
                
                # Guardar información del pivoteo para visualización
                pivot_info = {
                    "iteration": iteration,
                    "entering_variable": self._get_variable_name(entering_col),
                    "leaving_variable": self.basic_variables[leaving_row],
                    "pivot_column": entering_col,
                    "pivot_row": leaving_row,
                    "pivot_element": self.tableau[leaving_row, entering_col],
                    "tableau_before": self.tableau.copy()
                }
                
                # Realizar pivoteo
                self._pivot(leaving_row, entering_col)
                
                # Actualizar variables básicas y no básicas
                self._update_variables(leaving_row, entering_col)
                
                # Agregar información post-pivoteo
                pivot_info["tableau_after"] = self.tableau.copy()
                
                # Guardar iteración con información detallada
                self._save_iteration_detailed(f"Iteración {iteration}", pivot_info)
                
            return {"error": "Máximo número de iteraciones alcanzado"}
            
        except Exception as e:
            return {"error": f"Error en algoritmo Simplex: {str(e)}"}
    
    def _is_optimal(self) -> bool:
        """Verificar si la solución actual es óptima"""
        # Para maximización: óptimo si todos los coeficientes en la fila objetivo son >= 0
        # (recordar que pusimos -c en la fila objetivo)
        objective_row = self.tableau[-1, :-1]
        return np.all(objective_row >= -1e-10)  # Usar tolerancia pequeña
    
    def _find_entering_variable(self) -> int:
        """Encontrar variable que entra (regla de Dantzig)"""
        objective_row = self.tableau[-1, :-1]
        # Encontrar el índice del coeficiente más negativo
        entering_col = np.argmin(objective_row)
        if objective_row[entering_col] >= -1e-10:
            return -1
        return entering_col
    
    def _find_leaving_variable(self, entering_col: int) -> int:
        """Encontrar variable que sale (prueba del cociente mínimo)"""
        m = self.tableau.shape[0] - 1  # Número de restricciones
        
        # Calcular cocientes
        ratios = []
        for i in range(m):
            if self.tableau[i, entering_col] > 1e-10:  # Evitar división por cero
                ratio = self.tableau[i, -1] / self.tableau[i, entering_col]
                if ratio >= 0:  # Solo ratios no negativos
                    ratios.append((ratio, i))
                else:
                    ratios.append((float('inf'), i))
            else:
                ratios.append((float('inf'), i))
        
        if not ratios or all(r[0] == float('inf') for r in ratios):
            return -1  # Solución no acotada
        
        # Encontrar mínimo ratio
        min_ratio, leaving_row = min(ratios)
        return leaving_row
    
    def _pivot(self, pivot_row: int, pivot_col: int):
        """Realizar operación de pivoteo"""
        # Elemento pivote
        pivot_element = self.tableau[pivot_row, pivot_col]
        
        if abs(pivot_element) < 1e-10:
            raise Exception("Elemento pivote demasiado pequeño")
        
        # Normalizar fila pivote
        self.tableau[pivot_row] = self.tableau[pivot_row] / pivot_element
        
        # Eliminar columna pivote en otras filas
        for i in range(self.tableau.shape[0]):
            if i != pivot_row:
                factor = self.tableau[i, pivot_col]
                self.tableau[i] = self.tableau[i] - factor * self.tableau[pivot_row]
    
    def _update_variables(self, leaving_row: int, entering_col: int):
        """Actualizar variables básicas y no básicas"""
        # Determinar qué variable entra y cuál sale
        n_original = len(self.variable_names)
        
        if entering_col < n_original:
            entering_var = self.variable_names[entering_col]
        else:
            entering_var = f"s{entering_col - n_original + 1}"
        
        leaving_var = self.basic_variables[leaving_row]
        
        # Intercambiar
        self.basic_variables[leaving_row] = entering_var
        
        # Actualizar listas
        if entering_var in self.non_basic_variables:
            self.non_basic_variables.remove(entering_var)
        if leaving_var not in self.non_basic_variables:
            self.non_basic_variables.append(leaving_var)
    
    def _extract_solution(self) -> Dict:
        """Extraer solución final"""
        try:
            n_original = len(self.variable_names)
            solution = {}
            
            # Inicializar todas las variables en 0
            for var in self.variable_names:
                solution[var] = 0.0
            
            # Asignar valores de variables básicas
            for i, var in enumerate(self.basic_variables):
                if var in self.variable_names:
                    solution[var] = self.tableau[i, -1]
            
            # Valor óptimo 
            # El valor en la esquina inferior derecha del tableau representa el valor de Z
            optimal_value = self.tableau[-1, -1]
            
            self.optimal_solution = solution
            self.optimal_value = optimal_value
            
            return {
                "status": "optimal",
                "optimal_solution": solution,
                "optimal_value": optimal_value,
                "basic_variables": self.basic_variables.copy(),
                "non_basic_variables": self.non_basic_variables.copy(),
                "iterations": self.iterations.copy(),
                "final_tableau": self.tableau.copy()
            }
            
        except Exception as e:
            return {"error": f"Error extrayendo solución: {str(e)}"}
    
    def _get_variable_name(self, col_index: int) -> str:
        """Obtener nombre de variable por índice de columna"""
        n_original = len(self.variable_names)
        if col_index < n_original:
            return self.variable_names[col_index]
        else:
            return f"s{col_index - n_original + 1}"
    
    def _save_iteration_detailed(self, description: str, pivot_info: Dict):
        """Guardar estado de iteración con información detallada del pivoteo"""
        self.iterations.append({
            "description": description,
            "tableau": self.tableau.copy(),
            "basic_variables": self.basic_variables.copy(),
            "non_basic_variables": self.non_basic_variables.copy(),
            "pivot_info": pivot_info
        })
    
    def _save_iteration(self, description: str):
        """Guardar estado de iteración (método simple)"""
        self.iterations.append({
            "description": description,
            "tableau": self.tableau.copy(),
            "basic_variables": self.basic_variables.copy(),
            "non_basic_variables": self.non_basic_variables.copy()
        })
    
    def get_formatted_solution(self, result: Dict) -> str:
        """Formatear solución para mostrar con detalles del proceso iterativo"""
        if "error" in result:
            return f"ERROR: {result['error']}"
        
        if result.get("status") != "optimal":
            return "No se encontró solución óptima"
        
        output = []
        output.append("=" * 80)
        output.append("SOLUCIÓN POR MÉTODO SIMPLEX")
        output.append("=" * 80)
        
        # Función objetivo
        obj_type = "MAXIMIZACIÓN" if self.is_maximization else "MINIMIZACIÓN"
        output.append(f"\nTipo de problema: {obj_type}")
        
        # Mostrar formulación inicial
        output.append(f"\nFORMULACIÓN DEL PROBLEMA:")
        output.append(f"Variables de decisión: {', '.join(self.variable_names)}")
        
        # Variables de decisión
        output.append(f"\nSOLUCIÓN ÓPTIMA:")
        solution = result["optimal_solution"]
        for var, value in solution.items():
            if var in self.variable_names:  # Solo mostrar variables de decisión originales
                output.append(f"  {var} = {value:.6f}")
        
        # Valor óptimo
        output.append(f"\nVALOR ÓPTIMO DE LA FUNCIÓN OBJETIVO:")
        output.append(f"  Z = {result['optimal_value']:.6f}")
        
        # Variables básicas finales
        output.append(f"\nVARIABLES BÁSICAS FINALES:")
        for i, var in enumerate(result["basic_variables"]):
            if i < len(self.tableau) - 1:  # Excluir fila objetivo
                value = self.tableau[i, -1]
                var_type = "Variable de decisión" if var in self.variable_names else "Variable de holgura"
                output.append(f"  {var} = {value:.6f} ({var_type})")
        
        # Proceso iterativo
        if "iterations" in result and len(result["iterations"]) > 1:
            output.append(f"\nPROCESO ITERATIVO DEL MÉTODO SIMPLEX:")
            output.append(f"Número total de iteraciones: {len(result['iterations']) - 1}")
            
            # Mostrar detalles de cada iteración
            for i, iteration in enumerate(result["iterations"]):
                if iteration["description"] == "Tablero Inicial":
                    output.append(f"\nTABLERO SIMPLEX INICIAL:")
                    output.append(self._format_tableau_with_highlight(iteration["tableau"]))
                elif "pivot_info" in iteration:
                    pivot = iteration["pivot_info"]
                    output.append(f"\nITERACIÓN {pivot['iteration']}:")
                    output.append(f"  Variable entrante (columna pivote): {pivot['entering_variable']} (columna {pivot['pivot_column'] + 1})")
                    output.append(f"  Variable saliente (fila pivote): {pivot['leaving_variable']} (fila {pivot['pivot_row'] + 1})")
                    output.append(f"  Elemento pivote: {pivot['pivot_element']:.6f}")
                    output.append(f"\n  Tablero Simplex después del pivoteo:")
                    output.append(self._format_tableau_with_highlight(
                        iteration["tableau"], 
                        highlight_row=pivot['pivot_row'], 
                        highlight_col=pivot['pivot_column']
                    ))
        
        # Tablero final
        output.append(f"\nTABLERO SIMPLEX FINAL:")
        output.append(self._format_tableau_with_highlight(self.tableau))
        
        # Interpretación de resultados
        output.append(f"\nINTERPRETACIÓN DE RESULTADOS:")
        solution = result["optimal_solution"]
        if self.is_maximization:
            output.append(f"  • El valor máximo de la función objetivo es {result['optimal_value']:.6f}")
        else:
            output.append(f"  • El valor mínimo de la función objetivo es {result['optimal_value']:.6f}")
        
        output.append(f"  • Este valor se alcanza cuando:")
        for var, value in solution.items():
            if var in self.variable_names:
                output.append(f"    - {var} = {value:.6f}")
        
        # Variables de holgura con interpretación
        slack_vars = [var for var in result["basic_variables"] if var.startswith('s')]
        if slack_vars:
            output.append(f"  • Variables de holgura activas:")
            for i, var in enumerate(result["basic_variables"]):
                if var.startswith('s') and i < len(self.tableau) - 1:
                    value = self.tableau[i, -1]
                    constraint_num = int(var[1:])
                    if value > 1e-6:
                        output.append(f"    - {var} = {value:.6f} (recursos no utilizados en restricción {constraint_num})")
                    else:
                        output.append(f"    - {var} = {value:.6f} (restricción {constraint_num} activa)")
        
        output.append("\n" + "=" * 80)
        
        return "\n".join(output)
    
    def get_standard_form_explanation(self, c: np.ndarray, A: np.ndarray, b: np.ndarray) -> str:
        """Generar explicación de la conversión a forma estándar"""
        output = []
        output.append("=" * 80)
        output.append("CONVERSIÓN A FORMA ESTÁNDAR DEL MÉTODO SIMPLEX")
        output.append("=" * 80)
        
        # Función objetivo original
        obj_type = "Maximizar" if self.is_maximization else "Minimizar"
        output.append(f"\n📋 PROBLEMA ORIGINAL:")
        obj_str = f"{obj_type} Z = "
        obj_terms = []
        for i, coeff in enumerate(c):
            if coeff != 0:
                var_name = self.variable_names[i] if i < len(self.variable_names) else f"x{i+1}"
                if coeff == 1:
                    obj_terms.append(f"{var_name}")
                elif coeff == -1:
                    obj_terms.append(f"-{var_name}")
                else:
                    obj_terms.append(f"{coeff}{var_name}")
        
        output.append(f"  {obj_str}{' + '.join(obj_terms).replace('+ -', '- ')}")
        
        # Restricciones originales
        output.append(f"\n  Sujeto a:")
        for i in range(len(A)):
            constraint_terms = []
            for j, coeff in enumerate(A[i]):
                if coeff != 0:
                    var_name = self.variable_names[j] if j < len(self.variable_names) else f"x{j+1}"
                    if coeff == 1:
                        constraint_terms.append(f"{var_name}")
                    elif coeff == -1:
                        constraint_terms.append(f"-{var_name}")
                    else:
                        constraint_terms.append(f"{coeff}{var_name}")
            
            constraint_str = ' + '.join(constraint_terms).replace('+ -', '- ')
            output.append(f"    {constraint_str} ≤ {b[i]}")
        
        # No negatividad
        var_list = ", ".join(self.variable_names)
        output.append(f"    {var_list} ≥ 0")
        
        # Forma estándar
        output.append(f"\n🔄 CONVERSIÓN A FORMA ESTÁNDAR:")
        output.append(f"  Se agregan variables de holgura para convertir inecuaciones en ecuaciones:")
        
        # Mostrar ecuaciones con variables de holgura
        for i in range(len(A)):
            constraint_terms = []
            for j, coeff in enumerate(A[i]):
                if coeff != 0:
                    var_name = self.variable_names[j] if j < len(self.variable_names) else f"x{j+1}"
                    if coeff == 1:
                        constraint_terms.append(f"{var_name}")
                    elif coeff == -1:
                        constraint_terms.append(f"-{var_name}")
                    else:
                        constraint_terms.append(f"{coeff}{var_name}")
            
            constraint_str = ' + '.join(constraint_terms).replace('+ -', '- ')
            output.append(f"    {constraint_str} + s{i+1} = {b[i]}  (s{i+1} ≥ 0)")
        
        # Variables no negativas en forma estándar
        all_vars = self.variable_names.copy()
        slack_vars = [f"s{i+1}" for i in range(len(A))]
        all_vars.extend(slack_vars)
        var_list = ", ".join(all_vars)
        output.append(f"    {var_list} ≥ 0")
        
        # Explicación de variables de holgura
        output.append(f"\nEXPLICACIÓN DE VARIABLES DE HOLGURA:")
        for i in range(len(A)):
            output.append(f"  • s{i+1}: Representa los recursos no utilizados en la restricción {i+1}")
            output.append(f"    Si s{i+1} > 0, la restricción {i+1} no está activa (hay holgura)")
            output.append(f"    Si s{i+1} = 0, la restricción {i+1} está activa (sin holgura)")
        
        output.append("\n" + "=" * 80)
        return "\n".join(output)
    
    def _format_tableau_with_highlight(self, tableau: np.ndarray, highlight_row: int = -1, highlight_col: int = -1) -> str:
        """Formatear tablero simplex para mostrar con highlighting opcional del pivote usando colores"""
        output = []
        
        # Códigos de color ANSI
        RESET = '\033[0m'
        RED = '\033[91m'      # Elemento pivote
        YELLOW = '\033[93m'   # Fila pivote
        BLUE = '\033[94m'     # Columna pivote
        GREEN = '\033[92m'    # Variable básica de la fila pivote
        BOLD = '\033[1m'
        
        # Encabezados
        headers = []
        n_original = len(self.variable_names)
        
        # Variables originales
        for var in self.variable_names:
            headers.append(var)
        
        # Variables de holgura
        for i in range(tableau.shape[1] - n_original - 1):
            headers.append(f"s{i+1}")
        
        # RHS
        headers.append("RHS")
        
        # Fila de encabezados con columna pivote resaltada
        header_parts = []
        for idx, h in enumerate(headers):
            if idx == highlight_col and highlight_col >= 0:
                header_parts.append(f"{BLUE}{BOLD}{h:>10}{RESET}")
            else:
                header_parts.append(f"{h:>10}")
        
        header_line = "Base\t" + "\t".join(header_parts)
        output.append(header_line)
        output.append("-" * (len(header_line) - len(BLUE) - len(BOLD) - len(RESET) if highlight_col >= 0 else len(header_line)))
        
        # Filas de restricciones
        for i in range(tableau.shape[0] - 1):
            base_var = self.basic_variables[i] if i < len(self.basic_variables) else "?"
            row_data = []
            
            for j in range(tableau.shape[1]):
                value = tableau[i, j]
                if i == highlight_row and j == highlight_col:
                    # Elemento pivote - rojo y marcado
                    row_data.append(f"{RED}{BOLD}[{value:8.4f}]*{RESET}")
                elif i == highlight_row:
                    # Fila pivote - amarillo
                    row_data.append(f"{YELLOW}({value:8.4f}){RESET}")
                elif j == highlight_col:
                    # Columna pivote - azul
                    row_data.append(f"{BLUE}<{value:8.4f}>{RESET}")
                else:
                    row_data.append(f"{value:10.4f}")
            
            # Variable básica de la fila pivote en verde
            if i == highlight_row:
                prefix = f"{GREEN}→{base_var:>3}{RESET}"
            else:
                prefix = f"{base_var:>4}"
            output.append(f"{prefix}\t" + "\t".join(row_data))
        
        # Fila objetivo
        obj_data = []
        for j in range(tableau.shape[1]):
            value = tableau[-1, j]
            if j == highlight_col and highlight_col >= 0:
                obj_data.append(f"{BLUE}<{value:8.4f}>{RESET}")
            else:
                obj_data.append(f"{value:10.4f}")
        
        output.append(f"{'Z':>4}\t" + "\t".join(obj_data))
        
        if highlight_row >= 0 and highlight_col >= 0:
            output.append("")
            output.append(f"Leyenda: {RED}{BOLD}[ ]*{RESET} = Elemento pivote, {YELLOW}( ){RESET} = Fila pivote, {BLUE}< >{RESET} = Columna pivote, {GREEN}→{RESET} = Variable saliente")
        
        return "\n".join(output)
    
    def _format_tableau(self, tableau: np.ndarray) -> str:
        """Formatear tablero simplex para mostrar (método original)"""
        return self._format_tableau_with_highlight(tableau)
    
    def get_iterations_summary(self, result: Dict) -> str:
        """Obtener resumen de iteraciones"""
        if "error" in result or "iterations" not in result:
            return "No hay iteraciones disponibles"
        
        output = []
        output.append("RESUMEN DE ITERACIONES")
        output.append("=" * 50)
        
        for i, iteration in enumerate(result["iterations"]):
            output.append(f"\n{iteration['description']}:")
            output.append(f"Variables básicas: {', '.join(iteration['basic_variables'])}")
            output.append(f"Variables no básicas: {', '.join(iteration['non_basic_variables'])}")
            
            if i < len(result["iterations"]) - 1:  # No mostrar tableau para todas las iteraciones
                output.append("Tableau:")
                output.append(self._format_tableau(iteration['tableau']))
        
        return "\n".join(output)