from typing import List, Dict, Any

from sympy import symbols, Eq, roots, Function, Symbol, degree, solve

a = 21
b = -111
c = 91
n = symbols('n')
d = n * 4 ** n
start_roots = {}

coefficients_start = []
coefficients = []


def find_general_solution_lors(factors: List):
    global coefficients_start
    # инициализирую все необходимые переменные
    n = len(factors)
    q, a, var = symbols('q aₙ n')
    # составляю первое уравнение и решаю его
    eq = Eq(q ** n, sum(q ** (n - i - 1) * factors[i] for i in range(n)))
    # обрабатываю кратные корни
    start_roots = roots(eq, q)
    solutions = __handle_frendering(start_roots, var)
    # генерирую уравнение ЛОРС
    coefficients_start = symbols(f'c1:{len(solutions) + 1}')
    return sum(coefficients_start[i] * solutions[i] for i in range(n))


def __handle_frendering(solutions: Dict, var: Symbol) -> List:
    solutions_new = []
    for key, val in solutions.items():
        solutions_new.append(key ** var)
        if val > 1:
            n = 1
            while val > 1:
                solutions_new.append(key ** var * var ** n)
                val -= 1
    return solutions_new


# exercise 1
a_general = find_general_solution_lors([21, -111, 91])
print(a_general)


def find_private_solution_lnrs(func, factors, t):
    global n
    funcs = []
    for i in range(len(factors) + 1):
        new_func = __get_equal_function(func, i)
        new_func *= t ** (n + i)
        if t in start_roots:
            new_func *= (n + i) ** start_roots[t]
        funcs.append(new_func)

    eq = Eq(funcs[len(factors)], sum(factors[len(factors) - i - 1] * funcs[i] for i in range(len(factors))) + func)
    solutions = solve(eq, coefficients)
    res = __get_equal_function(func, eternal=solutions)
    res *= t ** n
    if t in start_roots:
        res *= n ** start_roots[t]
    return res


def __get_equal_function(func, additional: int = 0, eternal: Dict | Any = None):
    global coefficients

    power = degree(func)
    if len(coefficients) == 0:
        coefficients = symbols(f'c0:{power + 1}')
    if eternal:
        coefs = [val for val in eternal.values()]
        new_func = (sum(coefs[i] * (n + additional) ** i for i in range(power + 1)))
    else:
        new_func = (sum(coefficients[i] * (n + additional) ** i for i in range(power + 1)))
    return new_func


# exercise 2
a_private = find_private_solution_lnrs(d, [21, -111, 91], 4)
print(a_private)


def find_general_heterogeneous_solution():
    pass

# exercise 3

