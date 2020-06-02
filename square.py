from graphics import *


class Square(Rectangle):
    def __init__(self, p1: Point, length: int):
        Rectangle.__init__(self, p1, Point(p1.getX() + length, p1.getY() + length))
        self.length = length

    def __repr__(self):
        return "Square({}, {}, length = {})".format(str(self.p1), str(self.p2), str(self.length))

    def clone(self):
        other = Square(self.p1, self.length)
        other.config = self.config.copy()
        return other


class Cell(Square):
    def __init__(self, point: Point):
        Square.__init__(self, point, 1)
        self.setFill('black')
        #self.setOutline('white')
        #self.setOutline(color_rgb(115, 13, 115)) # фиолетовый
        self.setOutline(color_rgb(83, 0, 144)) # индиго (светлый)

    def __repr__(self):
        return "Cell({})".format(str(self.p1))

    def getX(self):
        return self.p1.getX()

    def getY(self):
        return self.p1.getY()


# Создаёт список Cells из списка Points
def cell_factory(list_pt: list):
    list_cells = []
    for ptr in list_pt:
        cell = Cell(ptr)
        list_cells.append(cell)
    return list_cells
