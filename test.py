from sympy import symbols, pretty

from task2 import RecurrentLinearSolver

# n = symbols('n')
# t = 4
# rls = RecurrentLinearSolver([21, -111, 91], n * 4 ** n, {0: 1, 1: 2, 2: 3}, n)
# print(pretty(rls.find_general_solution_lhrr()))
# print()
# print(pretty(rls.find_private_solution_lnrr(t)))
# print()
# print(pretty(rls.find_general_heterogeneous_solution(t)))
# print()
#
# print(pretty(rls.get_n_element_by_general_member_formula(3, t)))
# print(pretty(rls.get_n_element_by_general_member_formula(4, t)))
# print(pretty(rls.get_n_element_by_general_member_formula(5, t)))
# print(pretty(rls.get_n_element_by_recurrent(3)))
# print(pretty(rls.get_n_element_by_recurrent(4)))
# print(pretty(rls.get_n_element_by_recurrent(5)))

print()
print()
n = symbols('n')
t = 4
rls = RecurrentLinearSolver([3.5, -4, 1.5], -1 * (4) ** n, {0: 1, 1: 2, 2: 3}, n)
print(pretty(rls.find_general_solution_lhrr()))
print()
print(pretty(rls.find_private_solution_lnrr(t)))
print()
print(pretty(rls.find_general_heterogeneous_solution(t)))
print()

print(pretty(rls.get_n_element_by_general_member_formula(3, t)))
print(pretty(rls.get_n_element_by_general_member_formula(4, t)))
print(pretty(rls.get_n_element_by_general_member_formula(5, t)))
print(pretty(rls.get_n_element_by_recurrent(3)))
print(pretty(rls.get_n_element_by_recurrent(4)))
print(pretty(rls.get_n_element_by_recurrent(5)))
