from sympy import symbols

from task2 import RecurrentLinearSolver

n = symbols('n')
rls = RecurrentLinearSolver([-3, 0, 4], 18 * n - 33, {0: 2, 1: 5, 2: 10}, n)
print(rls.find_general_solution_lhrr())
print(rls.find_private_solution_lnrr(1))
print(rls.find_general_heterogeneous_solution(1))
