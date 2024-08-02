from impl import *
from random import randint, choice

N = 9  # размер стороны игрового поля
fields = init_fields(2, N)
ship_specs = [(4, 1), (3, 2), (2, 3), (1, 4)]  # (длина, количество)
def add_all_ships(field: list, ship_specs: list):
    for ship_len, count in ship_specs:
        for _ in range(count):
            while True:
                head_coord = (choice('АБВГДЕЖЗИК'), randint(1, len(field)))
                is_horizontal = choice([True, False])
                if add_ship(field, ship_len, head_coord, is_horizontal):
                    break

add_all_ships(fields[0], ship_specs)
add_all_ships(fields[1], ship_specs)

draw_fields(fields)
play_game(fields, N)



