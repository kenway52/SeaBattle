from random import randint, choice

# коды содержимого ячеек
EMPTY = 0  # пустая ячейка
SHIP  = 1  # ячейка с кораблем
MISS  = 5  # удар мимо
HIT   = 6  # удар в корабль
NEAR  = 7  # окорестность корабля

def init_fields(fields_number, side):
    return [[[0 for j in range(side)] for i in range(side)] for k in range(fields_number)]

def draw_fields(fields):
    SPACE_FIELDS = 4  # Space between fields
    SPACE_CELLS = 2   # Space between cells in field
    SPACE_VERT_LEGEND = '  '  # Space equal to letters legend column

    upper_legend_row = ' '
    for k in range(len(fields)):
        for j in range(len(fields[0])):
            n = coord_atou(0, j)[1]
            upper_legend_row += f"{n:>2}" + ' ' * (SPACE_CELLS - 1)  # Values >9 are displayed correctly
        upper_legend_row += ' ' * SPACE_FIELDS + SPACE_VERT_LEGEND
    print(upper_legend_row)

    for i in range(len(fields[0])):
        for k in range(len(fields)):
            print(coord_atou(i, 0)[0], end=' ')
            for j in range(len(fields[0])):
                print(get_cell_symbol(fields[k][i][j]), end=' ' * SPACE_CELLS)
            print(' ' * SPACE_FIELDS, sep='', end='')
        print()

def get_cell_symbol(value):
    if value == EMPTY:
        symbol = '.'
    elif value == SHIP:
        symbol = '#'
    elif value == MISS:
        symbol = '~'
    elif value == HIT:
        symbol = 'X'
    elif value == NEAR:
        symbol = '-'
    else:
        symbol = '?'
    return symbol

def coord_utoa(vert, horiz):
    """Преобразует пользовательские координаты в индексы массива"""
    return ({'А':0, 'Б':1, 'В':2, 'Г':3, 'Д':4, 'Е':5, 'Ж':6, 'З':7, 'И':8, 'К':9 }[vert], horiz - 1)

def coord_atou(i, j):
    """Преобразует индексы массива в координаты"""
    return ('АБВГДЕЖЗИК'[i], str(j + 1))

def is_on_field(field: list, i, j):
    return (0 <= i < len(field)) and (0 <= j < len(field))

def get_near_coords(i, j) -> list:
    return [(i-1, j-1),(i, j-1),(i+1, j-1),(i, j-1),(i,j+1),(i-1, j+1),(i, j+1),(i+1, j+1)]

def add_ship(field: list, ship_len: int, head_coord: tuple, is_horizontal: bool) -> bool:
    if isinstance(head_coord[0], str):
        head_coord_a = coord_utoa(head_coord[0], head_coord[1])
    else:
        head_coord_a = head_coord

    ship_cells = []
    for m in range(ship_len):
        i = head_coord_a[0] + (m if not is_horizontal else 0)
        j = head_coord_a[1] + (m if is_horizontal else 0)
        if not is_on_field(field, i, j):
            return False
        ship_cells.append((i, j))

    for i, j in ship_cells:
        if field[i][j] != EMPTY:
            return False
        near_coords = get_near_coords(i, j)
        for a, b in near_coords:
            if is_on_field(field, a, b) and field[a][b] == SHIP:
                return False

    for i, j in ship_cells:
        near_coords = get_near_coords(i, j)
        for a, b in near_coords:
            if is_on_field(field, a, b) and field[a][b] == EMPTY:
                field[a][b] = NEAR

    for i, j in ship_cells:
        field[i][j] = SHIP

    return True


def get_user_input(field_size):
    """Пользователю предлагается ввести координаты для атаки в формате "А1", 
    где "А" — это буква, обозначающая строку, а "1" — это цифра, обозначающая столбец.
    Введенная строка приводится к верхнему регистру с помощью метода strip().upper(), 
    чтобы обеспечить соответствие формату ввода.
"""
    while True:
        coord = input("Введите координаты для атаки (например, А1): ").strip().upper()
        if len(coord) == 2 and coord[0] in 'АБВГДЕЖЗИК' and coord[1] in '123456789':
            row = 'АБВГДЕЖЗИК'.index(coord[0])
            col = int(coord[1]) - 1
            if 0 <= row < field_size and 0 <= col < field_size:
                return row, col
        print("Некорректные координаты. Попробуйте снова.")


def play_game(fields, field_size):
    """Цикл while True создает бесконечный цикл, который будет продолжаться до тех пор
    пока не будет определено, что один из игроков победил."""
    while True:
        for i, field in enumerate(fields):
            print(f"Ход игрока {i + 1}")
            row, col = get_user_input(field_size)
            if field[row][col] == SHIP:
                field[row][col] = HIT
                print("Попадание!")
            elif field[row][col] == EMPTY:
                field[row][col] = MISS
                print("Мимо!")
            draw_fields(fields)
            if all(cell != SHIP for row in field for cell in row):
                print(f"Игрок {i + 1} победил!")
                return
            

def check_winner(field):
    """Функция check_winner используется для определения, 
    остались ли на игровом поле еще корабли. 
    Она проверяет каждую ячейку поля и возвращает True
    если все корабли уничтожены (то есть на поле нет ячеек со значением SHIP)."""
    return all(cell != SHIP for row in field for cell in row)
#all(iterable) — это встроенная функция Python, которая возвращает True
#если все элементы в итерируемом объекте 
#(в данном случае, списке) являются истинными (True). 
#Если хотя бы один элемент в списке ложный (False), функция all вернет False.