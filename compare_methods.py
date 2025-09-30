#!/usr/bin/env python3

from simplex_solver import SimplexSolver

# Mismo problema que estaba dando resultados diferentes
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

print("="*60)
print("COMPARACIÓN: MÉTODO GRÁFICO vs MÉTODO SIMPLEX")
print("="*60)

# Resolver con Simplex
print("\n🔹 MÉTODO SIMPLEX:")
print("-" * 30)
solver = SimplexSolver()
simplex_result = solver.solve_from_text(problem_text)

if "error" in simplex_result:
    print(f"Error Simplex: {simplex_result['error']}")
else:
    print(f"Estado: {simplex_result['status']}")
    print(f"Valor óptimo: {simplex_result['optimal_value']}")
    print(f"Variables: {simplex_result['optimal_solution']}")

# Resolver manualmente método gráfico
print("\n🔹 ANÁLISIS MANUAL DEL MÉTODO GRÁFICO:")
print("-" * 30)

print("Restricciones:")
print("1. x1 + 3x2 ≤ 200")
print("2. x1 + x2 ≤ 100") 
print("3. x1 ≥ 20")
print("4. x2 ≥ 10")
print("5. x1 ≥ 0, x2 ≥ 0")

print("\nPuntos de intersección:")
print("• Intersección (1) y (2): x1 + 3x2 = 200 y x1 + x2 = 100")
print("  Resolviendo: x1 = 100 - x2, sustituyendo: (100 - x2) + 3x2 = 200")
print("  100 + 2x2 = 200 → x2 = 50, x1 = 50")
print("  Punto: (50, 50)")

print("\n• Intersección (1) y (3): x1 + 3x2 = 200 y x1 = 20")
print("  20 + 3x2 = 200 → x2 = 60")
print("  Punto: (20, 60)")

print("\n• Intersección (2) y (3): x1 + x2 = 100 y x1 = 20")
print("  20 + x2 = 100 → x2 = 80")
print("  Punto: (20, 80)")

print("\n• Intersección (2) y (4): x1 + x2 = 100 y x2 = 10")
print("  x1 + 10 = 100 → x1 = 90")
print("  Punto: (90, 10)")

print("\n• Intersección (1) y (4): x1 + 3x2 = 200 y x2 = 10")
print("  x1 + 30 = 200 → x1 = 170")
print("  Punto: (170, 10)")

print("\n• Intersección (3) y (4): x1 = 20 y x2 = 10")
print("  Punto: (20, 10)")

print("\nVerificando factibilidad de los puntos:")
vertices_candidates = [(50, 50), (20, 60), (20, 80), (90, 10), (170, 10), (20, 10)]

def check_feasibility(x1, x2):
    constraints = [
        (x1 + 3*x2 <= 200, f"x1 + 3x2 = {x1 + 3*x2} ≤ 200"),
        (x1 + x2 <= 100, f"x1 + x2 = {x1 + x2} ≤ 100"),
        (x1 >= 20, f"x1 = {x1} ≥ 20"),
        (x2 >= 10, f"x2 = {x2} ≥ 10"),
        (x1 >= 0, f"x1 = {x1} ≥ 0"),
        (x2 >= 0, f"x2 = {x2} ≥ 0")
    ]
    
    feasible = True
    for constraint, desc in constraints:
        if not constraint:
            print(f"    ❌ {desc}")
            feasible = False
        else:
            print(f"    ✅ {desc}")
    
    return feasible

feasible_vertices = []
for vertex in vertices_candidates:
    x1, x2 = vertex
    print(f"\nPunto ({x1}, {x2}):")
    if check_feasibility(x1, x2):
        feasible_vertices.append(vertex)
        print(f"  → FACTIBLE")
    else:
        print(f"  → NO FACTIBLE")

print(f"\nVértices factibles: {feasible_vertices}")

print("\nEvaluando función objetivo Z = 30x1 + 50x2:")
optimal_value = -float('inf')
optimal_point = None

for vertex in feasible_vertices:
    x1, x2 = vertex
    z_value = 30*x1 + 50*x2
    print(f"• ({x1}, {x2}): Z = 30({x1}) + 50({x2}) = {z_value}")
    
    if z_value > optimal_value:
        optimal_value = z_value
        optimal_point = vertex

print(f"\n🎯 RESULTADO MÉTODO GRÁFICO MANUAL:")
print(f"Punto óptimo: {optimal_point}")
print(f"Valor óptimo: {optimal_value}")

print("\n" + "="*60)
print("COMPARACIÓN FINAL:")
print("="*60)
print(f"Simplex:  Punto = {simplex_result.get('optimal_solution', 'N/A')}, Valor = {simplex_result.get('optimal_value', 'N/A')}")
print(f"Gráfico:  Punto = {optimal_point}, Valor = {optimal_value}")

if simplex_result.get('optimal_value') == optimal_value:
    print("✅ AMBOS MÉTODOS COINCIDEN")
else:
    print("❌ HAY DISCREPANCIA - Revisar implementación del método gráfico")