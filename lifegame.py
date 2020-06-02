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
    all_time = 0
    loop_time = 0
    x_end = 10
    y_end = 10
    x_stat = 0
    y_stat = 0

    def next_moment():
        nonlocal all_time, loop_time, x_stat, y_stat, x_end, y_end
        # Увеличение масштаба
        if loop_time > 1.0:
            # Time
            loop_time = 0
            # Window
            x_end += 5
            y_end += 5
            x_stat -= 5
            y_stat -= 5
            # Text
            text.move(4, -4.5)
            text.setText("All time: " + str(all_time))
            print("All time: " + str(all_time))
            window.setCoords(x_stat, y_stat, x_end, y_end)
        # Подсчёт времени
        all_time += delta_time
        loop_time += delta_time

        return all_time

    return next_moment


def draw_step(cells, window, time_scroll):
    for i in cells:
        i.draw(window)

    time_scroll()
    time.sleep(0.5)

    for i in cells:
        i.undraw()

    return draw_step(step(cells), window, time_scroll)

# Переписать с for'ами (по-человечески)
def get_neighbors(pt):
    return [Cell(Point(pt.getX(), pt.getY() + 1))
        , Cell(Point(pt.getX(), pt.getY() - 1))
        , Cell(Point(pt.getX() + 1, pt.getY()))
        , Cell(Point(pt.getX() + 1, pt.getY() + 1))
        , Cell(Point(pt.getX() + 1, pt.getY() - 1))
        , Cell(Point(pt.getX() - 1, pt.getY()))
        , Cell(Point(pt.getX() - 1, pt.getY() + 1))
        , Cell(Point(pt.getX() - 1, pt.getY() - 1))]


def compare_points(left: Point, right: Point):
    return True \
        if (left.getX() == right.getX()
            and left.getY() == right.getY()) \
        else False


def compare_points_closure(left: Point):
    def crutch(right: Point):
        return True \
            if (left.getX() == right.getX()
                and left.getY() == right.getY()) \
            else False
    return crutch


def __eq__(self: Point, right_point: Point):
    return True \
        if (self.getX() == right_point.getX()
            and self.getY() == right_point.getY()) \
        else False


def alive_rools(neighbors_quant):
    return neighbors_quant == 3


def live_rools(neighbors_quant):
    if neighbors_quant <= 1 or neighbors_quant > 3:
        return True
    elif neighbors_quant in [2, 3]:
        return False


"""
Как это работает... (так предпологалось)
    (pt in cells).lookAtNeighbors()
    
        1. get_neighbors
        
        2.1. Who in cells is neighbors? 
        - (pt in cells).getX and getY == (neig in neighbors).getX and getY
        2.2. Other are NOTcells
        
        3. neighbors_quant from 2.1. !!!
        *   == 1 --- delete
        *   == 2 or 3 --- nothing
        *   > 3 --- delete 
        
    neighbors_quant from 2.2. !!!
        *   == 1 --- delete
        *   == 2 or 3 --- nothing
        *   > 3 --- delete
"""


def step(cells: list):
    def getCellsFromNeighbors(curPoint: Point, neighbors: list):
        cells_neighbors = []
        not_cells_neighbors = []
        for pt in cells:
            if not compare_points(pt, curPoint):
                for neig in neighbors:
                    if compare_points(pt, neig):
                        cells_neighbors.append(pt)

        return cells_neighbors

    # Возращает кол-во соседей-клеток pt
    def lookAtNeighbors(pt: Point):
        neighbors = get_neighbors(pt)
        neig_cells = getCellsFromNeighbors(pt, neighbors)
        neighbors_quant = len(neig_cells)

        return neighbors_quant

    # Добавляет в other_neighbors всех соседей curPoint,
    # которых не в cells и там не присутствуют
    def new_other_neighbors(curPoint: Point, other_neighbors: list):
        neighbors = get_neighbors(curPoint)
        for i in neighbors:
            # Условие которое должно достигать (len(cells) - 1)
            # для подтверждения, что i нет в cells
            proof = 0
            for j in cells:
                if not compare_points(i, j) and not compare_points(j, curPoint):
                    proof += 1
                    # нужно выйти из цикла cells
                    continue

            # Нет ли i уже в other_neighbors?
            save_proof = proof
            for k in other_neighbors:
                if not compare_points(i, k):
                    proof += 1
                    # нужно выйти из цикла cells и other_neighbors
                    continue
                else:
                    # i есть в other_neighbors!
                    break
            if proof >= len(other_neighbors) + save_proof:
                proof = save_proof

            if proof == len(cells) - 1:
                other_neighbors.append(i)



    # Возвращает все клетки, которые не могут быть возраждены (оживлены)
    def revive_cells(other_neighbors):
        will_revive_cells = []
        for pt in other_neighbors:
            quant = lookAtNeighbors(pt)
            if alive_rools(quant):
                will_revive_cells.append(pt)

        return will_revive_cells

    newCells = cells.copy()
    other_neighbors = []
    for pt in cells:
        neighbors_quant = lookAtNeighbors(pt)
        if live_rools(neighbors_quant):
            newCells.remove(pt)

        new_other_neighbors(pt, other_neighbors)
        will_revive_cells = revive_cells(other_neighbors)

        # Проверка уникальности значений will_revive_cells относительно newCells
        #newCells.extend(will_revive_cells)
        for i in will_revive_cells:
            proof = 0
            for j in newCells:
                if not compare_points(i, j):
                    proof += 1
            if proof == len(newCells):
                newCells.append(i)

    return newCells


def drawText(win: GraphWin):
    score = 0
    txt = Text(Point(9, 0.5), "All time: " + str(score))
    txt.setOutline('white')
    txt.setFace('arial')
    txt.draw(win)

    return txt


def drawMainWindow():
    mainWin = GraphWin(title="MINE", width=500, height=500) # create a window
    mainWin.setCoords(0, 0, 10, 10)  # set the coordinates of the window; bottom left is (0, 0) and top right is (10, 10)
    mainWin.setBackground(color_rgb(105, 100, 95))  # some gray color

    return mainWin


if __name__ == '__main__':
    # Рисование окна
    mainWin = drawMainWindow()
    # Некий счётчк на экране
    txt = drawText(mainWin)
    # Набор клеток
    list_cells = cell_factory([Point(4, 5), Point(5, 5), Point(6, 5), Point(5, 6)])

    draw_step(list_cells, mainWin, func_scroll(1, mainWin, txt))

    mainWin.getMouse()  # Pause before closing (to view result)
    mainWin.isClosed()  # Close window when done
