class Coord:

    def __init__(self, newX=0, newY=0, newCoord=None):
        self.x = newX
        self.y = newY

        if(newCoord is not None):
            self.x = newCoord.x
            self.y = newCoord.y

    def __str__(self):
        return "({},{})".format(self.x, self.y)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.x == other.y and self.y == other.y
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def copy(self, coord):
        self.x = coord.x
        self.y = coord.y
