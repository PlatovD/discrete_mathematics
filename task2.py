from typing import List, Dict, Any

from sympy import symbols, Eq, roots, Symbol, degree, solve, Expr


class RecurrentLinearSolver:
    __roots: Dict
    __coefficients_LHRR: List
    __coefficients_LNRR: List

    def __init__(self, parameters: List, d_n: Expr, initial_conditions: Dict, variable_n: Symbol):
        self.__parameters = parameters
        self.__d_n = d_n
        self.__initial_conditions = initial_conditions
        self.__n = variable_n
        self.__coefficients_LHRR = []
        self.__coefficients_LNRR = []

    def find_general_solution_lhrr(self):
        # инициализирую все необходимые переменные
        n = len(self.__parameters)
        # составляю первое уравнение и решаю его
        self.__find__roots()
        # обрабатываю кратные корни
        solutions = self.__handle_frendering()
        # генерирую уравнение ЛОРС
        self.__coefficients_LHRR = symbols(f'c1:{len(solutions) + 1}')
        return sum(self.__coefficients_LHRR[i] * solutions[i] for i in range(n))

    def __find__roots(self):
        n = len(self.__parameters)
        q = symbols('q')
        eq = Eq(q ** n, sum(q ** (n - i - 1) * self.__parameters[i] for i in range(n)))
        self.__roots = roots(eq, q)

    def __handle_frendering(self) -> List:
        solutions_new = []
        for key, val in self.__roots.items():
            solutions_new.append(key ** self.__n)
            if val > 1:
                n = 1
                while val > 1:
                    solutions_new.append(key ** self.__n * self.__n ** n)
                    val -= 1
        return solutions_new

    def find_private_solution_lnrr(self, t):
        funcs = []
        n = len(self.__parameters)
        for i in range(n + 1):
            new_func = self.__get_equal_function()
            new_func *= t ** self.__n
            if t in self.__roots:
                new_func *= self.__n ** self.__roots[t]
            new_func = new_func.subs(self.__n, self.__n + i)
            funcs.append(new_func)

        eq = Eq(funcs[n], sum(self.__parameters[n - i - 1] * funcs[i] for i in range(n)) + self.__d_n)
        solutions = solve(eq, self.__coefficients_LNRR)
        res = self.__get_equal_function(eternal=solutions)
        res *= t ** self.__n
        if t in self.__roots:
            res *= self.__n ** self.__roots[t]
        return res

    def __get_equal_function(self, eternal: Dict | Any = None):
        power = degree(self.__d_n)
        if len(self.__coefficients_LNRR) == 0:
            self.__coefficients_LNRR = symbols(f'c0:{power + 1}')
        if eternal:
            coeffs = [val for val in eternal.values()]
            new_func = (sum(coeffs[i] * self.__n ** i for i in range(power + 1)))
        else:
            new_func = (sum(self.__coefficients_LNRR[i] * self.__n ** i for i in range(power + 1)))
        return new_func

    def find_general_heterogeneous_solution(self, t):
        exp = self.find_general_solution_lhrr() + self.find_private_solution_lnrr(t)
        eq_system = []
        for n, res in self.__initial_conditions.items():
            row_exp = exp.subs(self.__n, n)
            eq = Eq(res, row_exp)
            eq_system.append(eq)
        solution = solve(eq_system, self.__coefficients_LHRR)
        return exp.subs(solution)

    def get_n_element_by_recurrent(self, n: int):
        if n < 0:
            raise RuntimeError('N should not be negative')
        if n in self.__initial_conditions.keys():
            return self.__initial_conditions.get(n)
        if len(self.__parameters) > len(self.__initial_conditions):
            raise RuntimeError('Initial conditions is too small to find next element')
        return self.__get_n_element_by_recurrent(n, len(self.__parameters))

    def __get_n_element_by_recurrent(self, n: int, depth: int):
        if all(_ in self.__initial_conditions.keys() for _ in range(n - 1, n - depth - 1, -1)):
            res = sum(self.__parameters[i - 1] * self.get_n_element_by_recurrent(n - i) for i in
                      range(1, depth + 1)) + self.__d_n.subs(self.__n, n - depth)
            self.__initial_conditions[n] = res
            return res

    def get_n_element_by_general_member_formula(self, n: int, t: int):
        formula = self.find_general_heterogeneous_solution(t)
        return formula.subs(self.__n, n)
