class RecurrentRatioSolver:
    __n: Symbol
    __roots: Dict
    __coefficients_LHRR: List
    __coefficients_LNRR: List

    def __init__(self, parameters: Collection, d_n: Expr, initial_conditions: Collection):
        self.__parameters = parameters
        self.__d_n = d_n
        self.__initial_conditions = initial_conditions
        self.__n = symbols('n')