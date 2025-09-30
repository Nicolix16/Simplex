"""
Ejemplo específico para mostrar la conversión a forma estándar del método Simplex
"""

from simplex_solver import SimplexSolver
import numpy as np

def test_standard_form():
    """Probar la explicación de forma estándar"""
    
    solver = SimplexSolver()
    
    print("=" * 80)
    print("EJEMPLO: CONVERSIÓN A FORMA ESTÁNDAR")
    print("=" * 80)
    
    # Problema de ejemplo: Maximizar Z = 3x1 + 2x2
    # Sujeto a:
    #   x1 + x2 <= 6
    #   2x1 + x2 <= 8
    #   x1 <= 4
    #   x1, x2 >= 0
    
    c = np.array([3, 2])  # Coeficientes función objetivo
    A = np.array([
        [1, 1],    # x1 + x2 <= 6
        [2, 1],    # 2x1 + x2 <= 8
        [1, 0]     # x1 <= 4
    ])
    b = np.array([6, 8, 4])  # Lado derecho
    
    # Configurar solver
    solver.is_maximization = True
    solver.variable_names = ["x1", "x2"]
    
    # Mostrar explicación de forma estándar
    explanation = solver.get_standard_form_explanation(c, A, b)
    print(explanation)
    
    print("\n" + "="*80)
    print("AHORA RESOLVIENDO EL PROBLEMA...")
    print("="*80)
    
    # Resolver el problema
    result = solver.solve(c, A, b, is_maximization=True, variable_names=["x1", "x2"])
    
    if "error" not in result:
        solution = solver.get_formatted_solution(result)
        print(solution)
    else:
        print(f"Error: {result['error']}")

if __name__ == "__main__":
    test_standard_form()
    input("\nPresiona Enter para continuar...")