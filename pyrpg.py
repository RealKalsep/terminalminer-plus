import random as rd

class generationError(Exception):
    def __init__(self, txt):
        self.text = txt

class Object:
    pass

class Grid:
    grid = []
    gridWidth = None
    gridHeight = None

    def clearGrid(self):
        if self.grid == []:
            return False
        else:
            self.grid = []
            return True

    def monoGenerate(self, fillObject, amount):
        if type(fillObject) is Object:
            for i in range(0, amount):
                self.grid.append(fillObject)
        else:
            raise generationError("Need an object to generate a grid")

    def markup(self, step):
        if self.grid == []:
            raise generationError("Can't markup an empty grid")
        else:
            for i in range(0, len(self.grid)):
                if i % step == 0 and i != 0:
                    self.grid[i] = "\n"
                #if self.grid[:-1] != "\n":
                    #self.grid.append("\n")

            self.grid.pop(0)

    def multiGenerate(self, amount, *args):
        for i in range(0, amount):
            self.grid.append(rd.choice(args))

    def setProperties(self):
        if self.grid == []:
            raise generationError("Can't set properties of an empty grid")
        else:
            x = 0

            self.gridHeight = self.grid.count("\n")

            for i in self.grid:
                if type(i) is Object:
                    x += 1
                elif i == "\n":
                    break

            self.gridWidth = x

grid = Grid()
grid.multiGenerate(10, "k", "s")
grid.markup(3)
print(grid.grid)
input()