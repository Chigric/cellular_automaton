from graphics import *
from square import *
from functools import reduce
import types


def print_cell(point):
    print("\t", point.getX(), point.getY())


def print_cells(cells):
    print("\nCells (X Y):")
    for i in cells:
        print_cell(i)


def func_scroll(delta_time: float, window: GraphWin, text: Text):
    # Ticks (time)
    all_time = 0
    x_end = 10
    y_end = 10
    x_stat = 0
    y_stat = 0

    def scroll(ticks: float):
        nonlocal x_stat, y_stat, x_end, y_end
        # Window
        x_end += ticks
        y_end += ticks
        x_stat -= ticks
        y_stat -= ticks
        # Text
        text.move(ticks * 0.8, ticks * -0.9)
        text.setText("Ticks: " + str(all_time))
        print("All Ticks: " + str(all_time))
        window.setCoords(x_stat, y_stat, x_end, y_end)

    def next_moment():
        nonlocal all_time

        # Scroll Window
        scroll(1)
        # Подсчёт времени
        all_time += delta_time
        # Sleep
        time.sleep(0.5)

        return all_time

    return next_moment


def draw_step(cells, window, time_scroll):
    for i in cells:
        i.draw(window)

    time_scroll()

    for i in cells:
        i.undraw()

    return draw_step(step(cells), window, time_scroll)


def get_neighbors(pt: Cell):
    return [Cell(Point(pt.getX() + i, pt.getY() + j))
            for i in range(-1, 2, 1) for j in range(-1, 2, 1) if j != 0 or i != 0]


def compare_points(left: Point, right: Point):
    return True \
        if (left.getX() == right.getX()
            and left.getY() == right.getY()) \
        else False


def alive_rools(neighbors_quant: int):
    return neighbors_quant == 3


def live_rools(neighbors_quant: int):
    if neighbors_quant <= 1 or neighbors_quant > 3:
        return True
    elif neighbors_quant in [2, 3]:
        return False
    else:
        return None


def step(cells: list):
    # Возращает кол-во соседей-клеток вокруг cur_point
    def look_at_neighbors(cur_point: Cell):
        return len([x for x in get_neighbors(cur_point) if x in cells])

    # Добавляет в other_neighbors всех соседей cur_pt,
    # которых нет в cells и в other_neighbors уже не присутствуют
    def new_other_neighbors(cur_pt: Cell, other_neighbors: list):
        neighbors = get_neighbors(cur_pt)
        for i in neighbors:
            # Условие которое должно достигать (len(cells) - 1)
            # для подтверждения, что i нет в cells
            proof = 0
            proof += len(list(filter(lambda j: i != j and j != cur_pt, cells)))
            # Нет ли i уже в other_neighbors?
            save_proof = proof
            for k in other_neighbors:
                if not i == k:
                    proof += 1
                else:
                    break  # i есть в other_neighbors!
            if proof >= len(other_neighbors) + save_proof:
                proof = save_proof
            if proof == len(cells) - 1:
                other_neighbors.append(i)

    # Возвращает все клетки, которые могут быть возраждены (оживлены)
    def revive_cells(other_neighbors: list):
        return filter(lambda x: alive_rools(look_at_neighbors(x)),
                      other_neighbors)

    # Живые клетки на следующей итерации
    new_cells = cells.copy()
    other_neighbors = []
    for pt in cells:
        # Выживет ли клетка на след. итерации
        neighbors_quant = look_at_neighbors(pt)
        if live_rools(neighbors_quant):
            new_cells.remove(pt)
        # Генерируем клетки, которые можно оживить
        new_other_neighbors(pt, other_neighbors)
        will_revive_cells = revive_cells(other_neighbors)  # Клетки для оживления
        # Проверка уникальности значений will_revive_cells относительно newCells
        new_cells.extend(filter(lambda x: not (x in new_cells), will_revive_cells))

    return new_cells


def draw_text(win: GraphWin):
    score = 0
    txt = Text(Point(9, 0.5), "All time: " + str(score))
    txt.setOutline('white')
    txt.setFace('arial')
    txt.draw(win)
    return txt


def draw_main_window():
    mainWin = GraphWin(title="MINE", width=500, height=500) # create a window
    mainWin.setCoords(0, 0, 10, 10)  # set the coordinates of the window; bottom left is (0, 0) and top right is (10, 10)
    mainWin.setBackground(color_rgb(105, 100, 95))  # some gray color
    return mainWin


def create_glider(set_x, set_y):
    return cell_factory([Point(set_x-1, set_y+1), Point(set_x, set_y), Point(set_x+1, set_y+1),
                         Point(set_x+1, set_y), Point(set_x, set_y-1)])


def create_line_glider_Ox(len: int, start_x, start_y):
    step_x = 5
    all_cells = []
    for i in range(len):
        all_cells.extend(create_glider(start_x + (step_x * i), start_y))
    return all_cells


if __name__ == '__main__':
    # Рисование окна
    mainWin = draw_main_window()
    # Некий счётчк на экране
    txt = draw_text(mainWin)
    # Набор клеток
    list_cells = cell_factory([Point(4, 5), Point(5, 5), Point(6, 5), Point(5, 6)])
    draw_step(list_cells, mainWin, func_scroll(1, mainWin, txt))

    mainWin.getMouse()  # Pause before closing (to view result)
    mainWin.isClosed()  # Close window when done
