#!/usr/bin/env python3

from simplex_solver import SimplexSolver

# Datos del problema según la imagen
problem_text = """
=== DATOS PARA GRÁFICA ===
TIPO: Maximizar
FUNCION_OBJETIVO: Z = 30x1 + 50x2
RESTRICCIONES:
- 1x1 + 3x2 <= 200
- 1x1 + 1x2 <= 100
- x1 >= 20
- x2 >= 10
- x1 >= 0
- x2 >= 0
VARIABLES: x1, x2
=== FIN DATOS ===
"""

solver = SimplexSolver()
print("Analizando problema...")
result = solver.solve_from_text(problem_text)

if "error" in result:
    print(f"Error: {result['error']}")
else:
    print("Solución encontrada:")
    print(f"Estado: {result.get('status', 'desconocido')}")
    if result.get('optimal_value'):
        print(f"Valor óptimo: {result['optimal_value']}")
        print(f"Variables: {result['optimal_solution']}")
        
    # Mostrar solución detallada con tablas
    if 'detailed_solution' in result:
        print("\n" + "="*50)
        print("SOLUCIÓN DETALLADA CON TABLAS:")
        print("="*50)
        detailed = solver.get_formatted_solution(result)
        print(detailed)