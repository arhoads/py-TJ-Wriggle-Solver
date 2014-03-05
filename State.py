from Wriggler import *


class State:

    def __init__(self, wrigglers, bCopy=False):
        if(not bCopy):
            self.wrigglers = wrigglers
        else:
            self.wrigglers = []
            for wriggler in wrigglers:
                self.wrigglers.append(Wriggler(wriggler))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            assert len(self.wrigglers) == len(other.wrigglers)

            for i in range(len(self.wrigglers)):
                if(self.wrigglers[i] != other.wrigglers[i]):
                    return False

            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return ''.join([str(wriggler) for wriggler in self.wrigglers])

    def __hash__(self):
        return hash(str(self))
