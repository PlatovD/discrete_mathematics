from functools import wraps
from itertools import product
from typing import List

true_table = []


def print_true_table(table: List) -> None:
    print(' '.join(num_to_char(i) for i in range(len(table[0]) - 1)) + ' f')
    for row in table:
        print(' '.join(str(num) for num in row))


def num_to_char(var_num: int) -> str:
    return chr(ord('x') + var_num)


# logic operation
def pierce_arrow(x: int, y: int) -> bool:
    return not (x or y)


# logic function
def function(x: int, y: int, z: int) -> bool:
    return (not x or (pierce_arrow(not y, z))) or not (x and y)


def test_func(x, y, z) -> bool:
    return x and y and (z or not z)


def test_func2(x, y, z) -> bool:
    return x <= y


def build_dual(func: callable) -> callable:
    @wraps(func)
    def wrapper(*args):
        return not func(*[not arg for arg in args])

    return wrapper

# exercise 1.2.1
def build_true_table(func: callable, table: List, parameters_cnt: int) -> None:
    table.clear()
    args = product([0, 1], repeat=parameters_cnt)
    for arg_row in args:
        table.append([*arg_row] + [func(*arg_row) * 1])


# exercise 1.3
def find_fictitious_variables(func: callable, table: List, parameters_cnt: int) -> None:
    build_true_table(func, table, parameters_cnt)
    fictitious_cnt = 0
    for var_num in range(parameters_cnt):
        is_fictitious = True
        for row in range(2 ** parameters_cnt):
            custom_row = table[row][:parameters_cnt]  # создаю именно копию строки
            custom_row[var_num] = not custom_row[var_num]
            if func(*custom_row) != table[row][parameters_cnt]:
                is_fictitious = False
                break
        if is_fictitious:
            fictitious_cnt += 1
            print(f"{num_to_char(var_num)} фиктивна")
    if fictitious_cnt == 0:
        print("Нет фиктивных переменных")


# exercise 1.4
def build_dual_and_simplify(func: callable, parameters_cnt: int) -> None:
    dual_func = build_dual(func)
    build_true_table(func, true_table, parameters_cnt)
    if sum(row[-1] for row in true_table) > parameters_cnt / 2:
        build_sdnf(dual_func, true_table, parameters_cnt)
    else:
        build_sknf(dual_func, true_table, parameters_cnt)


# exercise 1.6(a)
def build_sdnf(func: callable, table: List, parameters_cnt: int) -> None:
    build_true_table(func, table, parameters_cnt)

    parts = set()
    for row in table:
        if row[-1]:
            parts.add(
                '(' + ' ∧ '.join(
                    ('¬' + num_to_char(i)) if not row[i] else num_to_char(i) for i in range(parameters_cnt)) + ')'
            )

    print(' ∨ '.join(parts))


# exercise 1.6(b)
def build_sknf(func: callable, table: List, parameters_cnt: int) -> None:
    build_true_table(func, table, parameters_cnt)

    parts = set()
    for row in table:
        if not row[-1]:
            parts.add(
                '(' + ' ∨ '.join(
                    ('¬' + num_to_char(i)) if row[i] else num_to_char(i) for i in range(parameters_cnt)) + ')'
            )

    print(' ∧ '.join(parts))


print("Таблица истинности")
build_true_table(function, true_table, 3)
print_true_table(true_table)
print()

print("Фиктивность")
find_fictitious_variables(function, true_table, 3)
print()

print("Построение двойственной функции")
build_dual_and_simplify(function, 3)
print()

print("СДНФ и СКНФ")
build_sdnf(function, true_table, 3)
build_sknf(function, true_table, 3)
print()
