"""
Archivo de prueba para el método Simplex
Ejecuta este archivo para probar la funcionalidad del solver sin la interfaz gráfica
"""

from simplex_solver import SimplexSolver

def test_simplex_solver():
    """Probar el solucionador Simplex con ejemplos"""
    
    solver = SimplexSolver()
    
    print("=" * 80)
    print("PRUEBA DEL MÉTODO SIMPLEX")
    print("=" * 80)
    
    # Ejemplo 1: Problema de maximización estándar
    print("\n1. PROBLEMA DE MAXIMIZACIÓN")
    print("-" * 40)
    print("Maximizar Z = 3x1 + 2x2")
    print("Sujeto a:")
    print("  x1 + x2 <= 6")
    print("  2x1 + x2 <= 8") 
    print("  x1 <= 4")
    print("  x1, x2 >= 0")
    
    # Coeficientes de la función objetivo
    c = [3, 2]
    
    # Matriz de restricciones (lado izquierdo)
    A = [
        [1, 1],    # x1 + x2 <= 6
        [2, 1],    # 2x1 + x2 <= 8
        [1, 0]     # x1 <= 4
    ]
    
    # Vector del lado derecho
    b = [6, 8, 4]
    
    # Resolver
    result1 = solver.solve(c, A, b, is_maximization=True, 
                          variable_names=["x1", "x2"], 
                          constraint_names=["R1", "R2", "R3"])
    
    print("\nRESULTADO:")
    if "error" in result1:
        print(f"Error: {result1['error']}")
    else:
        print(solver.get_formatted_solution(result1))
    
    # Ejemplo 2: Problema de minimización
    print("\n\n2. PROBLEMA DE MINIMIZACIÓN")
    print("-" * 40)
    print("Minimizar Z = 2x1 + 3x2")
    print("Sujeto a:")
    print("  x1 + x2 >= 4")
    print("  2x1 + x2 >= 6")
    print("  x1, x2 >= 0")
    
    # Para minimización con restricciones >=, necesitamos variables de exceso
    # Convertir >= a <= restando variables de exceso
    # x1 + x2 >= 4 se convierte en x1 + x2 - s1 = 4
    # Pero el Simplex estándar necesita <= así que usamos variables artificiales
    # Por simplicidad, usaremos Big M o dos fases, pero aquí mostraré la conversión directa
    
    c2 = [2, 3]
    # Convertir a forma estándar: agregar variables de exceso y artificiales
    A2 = [
        [1, 1],   # x1 + x2 >= 4
        [2, 1]    # 2x1 + x2 >= 6
    ]
    b2 = [4, 6]
    
    result2 = solver.solve(c2, A2, b2, is_maximization=False,
                          variable_names=["x1", "x2"],
                          constraint_names=["R1", "R2"])
    
    print("\nRESULTADO:")
    if "error" in result2:
        print(f"Error: {result2['error']}")
        print("NOTA: Este solver está optimizado para restricciones ≤")
        print("Para restricciones ≥ se necesita implementar el método de dos fases o Big M")
    else:
        print(solver.get_formatted_solution(result2))
    
    # Ejemplo 3: Prueba con texto estructurado
    print("\n\n3. PRUEBA CON ANÁLISIS DE TEXTO")
    print("-" * 40)
    
    # Simular texto de respuesta de Gemini
    sample_text = """
    Análisis del problema de programación lineal:
    
    Este es un problema típico de optimización que se puede resolver
    con el método Simplex.
    
    === DATOS PARA SIMPLEX ===
    TIPO: Maximizar
    FUNCION_OBJETIVO: Z = 5x1 + 3x2
    RESTRICCIONES:
    - 2x1 + 1x2 <= 10
    - 1x1 + 2x2 <= 8
    - 1x1 <= 4
    - x1 >= 0
    - x2 >= 0
    VARIABLES: x1, x2
    === FIN DATOS SIMPLEX ===
    
    La solución óptima se encuentra en uno de los vértices
    de la región factible.
    """
    
    result3 = solver.solve_from_text(sample_text)
    
    print("Resolviendo desde texto estructurado:")
    if "error" in result3:
        print(f"Error: {result3['error']}")
    else:
        print(solver.get_formatted_solution(result3))

def test_constraint_parsing():
    """Probar el parseo de restricciones"""
    
    print("\n\n4. PRUEBA DE PARSEO DE RESTRICCIONES")
    print("-" * 50)
    
    solver = SimplexSolver()
    
    test_constraints = [
        "2x1 + 3x2 <= 12",
        "x1 + x2 <= 6", 
        "3x1 - 2x2 >= 4",
        "x1 <= 5",
        "x2 >= 2",
        "x1 >= 0",
        "x2 >= 0"
    ]
    
    for constraint in test_constraints:
        result = solver._parse_constraint(constraint)
        print(f"'{constraint}' -> {result}")

if __name__ == "__main__":
    test_simplex_solver()
    test_constraint_parsing()
    
    input("\nPresiona Enter para continuar...")