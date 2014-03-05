from Coord import *


class Action:

    def __init__(self, wrigglerID=None, headMoved=None, movedCoord=None, action=None):
        if(action is None):
            assert wrigglerID is not None and headMoved is not None and movedCoord is not None

            self.wrigglerID = wrigglerID
            self.headMoved = headMoved
            self.movedCoord = Coord(newCoord=movedCoord)
        else:
            self.wrigglerID = action.wrigglerID
            self.headMoved = action.headMoved
            self.movedCoord = Coord(newCoord=action.movedCoord)

    def __str__(self):
        return "({}) HeadMoved: {} movedCoord: {}".format(self.wrigglerID, self.headMoved, self.movedCoord)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if(self.wrigglerID != other.wrigglerID or self.headMoved != other.headMoved or self.movedCoord != other.movedCoord):
                return False
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)
