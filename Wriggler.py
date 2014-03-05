import static
from Coord import *


class Wriggler:

    def __init__(self, wriggler=None):
        self.location = []  # Comprised of [hCoord, [list of body cords], tCoord]

        if(wriggler is not None):
            self.location.append(Coord(newCoord=wriggler.location[0]))
            self.location.append([Coord(newCoord=coord) for coord in wriggler.location[1]])
            self.location.append(Coord(newCoord=wriggler.location[2]))
            self.id = wriggler.id
        else:
            self.id = -1

    def __lt__(self, other):
        return self.id < other.id

    def __str__(self):
        # ''.join([str(coord) for coord in self.location[1]]) # For the whole body
        bodyLength = len(self.location[1])
        if(bodyLength > 0):
            return "{}{}{}{}{}".format(self.id, self.location[0], self.location[2], self.location[1][0], self.location[1][bodyLength - 1])
        else:
            return "{}{}{}".format(self.id, self.location[0], self.location[2])

    def __hash__(self):
        return str(self)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if(self.id != other.id or self.location[0] != other.location[0] or self.location[2] != other.location[2]):
                return False
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    # move direction uses head symbol
    def move(self, direction, moveHead, updateMaze=False):
        if(moveHead):
            coord = Coord(newCoord=self.location[0])
        else:
            coord = Coord(newCoord=self.location[2])

        if(direction == 'U'):
            coord.y -= 1
        elif(direction == 'D'):
            coord.y += 1
        elif(direction == 'L'):
            coord.x -= 1
        elif(direction == 'R'):
            coord.x += 1
        else:
            assert False, "direction: " + str(direction)

        assert static.board[coord.x][coord.y] == static.EMPTY, "wriggler(" + str(
            self.id) + ") tried to move into invalid spot: " + str(static.board[coord.x][coord.y])

        if(len(self.location[1]) == 0):
            if(moveHead):
                static.board[self.location[2].x][self.location[2].y] = static.EMPTY
                self.location[2] = self.location[0]
                self.location[0] = Coord(newCoord=coord)
            else:
                static.board[self.location[0].x][self.location[0].y] = static.EMPTY
                self.location[0] = self.location[2]
                self.location[2] = Coord(newCoord=coord)
        else:
            if(moveHead):
                headCoord = Coord(newCoord=self.location[0])
                newTailCoord = Coord(newCoord=self.location[1][len(self.location[1]) - 1])
                self.location[0] = Coord(newCoord=coord)
            else:
                tailCoord = Coord(newCoord=self.location[2])
                newHeadCoord = Coord(newCoord=self.location[1][0])
                self.location[2] = Coord(newCoord=coord)

            bodyLength = len(self.location[1])

            if(moveHead):
                for i in range(bodyLength):
                    if i == 0:
                        oldCoord = self.location[1][i]
                        self.location[1][0] = Coord(newCoord=headCoord)
                        continue

                    newCoord = self.location[1][i]
                    self.location[1][i] = oldCoord
                    oldCoord = newCoord

                static.board[self.location[2].x][self.location[2].y] = static.EMPTY
                self.location[2] = newTailCoord
            else:
                for i in range(bodyLength - 1, -1, -1):
                    if i == bodyLength - 1:
                        oldCoord = self.location[1][i]
                        self.location[1][bodyLength - 1] = Coord(newCoord=tailCoord)
                        continue

                    newCoord = self.location[1][i]
                    self.location[1][i] = oldCoord
                    oldCoord = newCoord

                static.board[self.location[0].x][self.location[0].y] = static.EMPTY
                self.location[0] = newHeadCoord

        if(updateMaze):
            self.updateMaze()

    def updateMaze(self):
        if(len(self.location[1]) == 0):
            headSymbol = self.convertToHeadSymbol(self.getSymbol(self.location[0], self.location[2]))
            static.board[self.location[0].x][self.location[0].y] = headSymbol
        else:
            headSymbol = self.convertToHeadSymbol(self.getSymbol(self.location[0], self.location[1][0]))
            static.board[self.location[0].x][self.location[0].y] = headSymbol  # + '_t'

        for i in range(len(self.location[1])):
            if(i == len(self.location[1]) - 1):
                toChange = self.location[1][len(self.location[1]) - 1]
                toCompare = self.location[2]
                symbol = self.getSymbol(toChange, toCompare)
            else:
                toChange = self.location[1][i]
                toCompare = self.location[1][i + 1]

            symbol = self.getSymbol(toChange, toCompare)
            static.board[toChange.x][toChange.y] = symbol

        static.board[self.location[2].x][self.location[2].y] = str(self.id)  # + "_t"

    def getPossibleMoves(self):
        moves = []

        headCoord = self.location[0]
        tailCoord = self.location[2]

        isHead = True
        for coord in [headCoord, tailCoord]:
            rightCoord = Coord(coord.x + 1, coord.y)
            if(self.isEmpty(rightCoord)):
                moves.append((rightCoord, isHead))
            leftCoord = Coord(coord.x - 1, coord.y)
            if(self.isEmpty(leftCoord)):
                moves.append((leftCoord, isHead))
            downCoord = Coord(coord.x, coord.y + 1)
            if(self.isEmpty(downCoord)):
                moves.append((downCoord, isHead))
            upCoord = Coord(coord.x, coord.y - 1)
            if(self.isEmpty(upCoord)):
                moves.append((upCoord, isHead))
            isHead = False

        return moves

    def isEmpty(self, coord):
        if(not self.isOutOfBounds(coord) and static.board[coord.x][coord.y] == static.EMPTY):
            return True
        return False

    def isOutOfBounds(self, coord):
        x = coord.x
        if(x >= static.columns or x < 0):
            return True

        y = coord.y
        if(y >= static.rows or y < 0):
            return True
        return False

    # Get correct symbol to put on board
    def getSymbol(self, toChange, toCompare):
            if(toCompare.y > toChange.y):
                return static.DOWN
            elif(toCompare.y < toChange.y):
                return static.UP
            elif(toCompare.x > toChange.x):
                return static.RIGHT
            elif(toCompare.x < toChange.x):
                return static.LEFT

    # returns the coordinate of next body part
    def followBody(self, coord, isHead=False):
        value = static.board[coord.x][coord.y].split('_')[0]

        if(isHead):
            if(value == static.HEADS[0]):  # 'U'
                coord.y -= 1
            elif(value == static.HEADS[1]):  # 'D'
                coord.y += 1
            elif(value == static.HEADS[2]):  # 'L'
                coord.x -= 1
            elif(value == static.HEADS[3]):  # 'R'
                coord.x += 1
            else:
                assert False, "Unexpected value: " + str(value)
        else:
            if(value == static.UP):  # '^'
                coord.y -= 1
            elif(value == static.DOWN):  # 'v'
                coord.y += 1
            elif(value == static.LEFT):  # '<'
                coord.x -= 1
            elif(value == static.RIGHT):  # '>'
                coord.x += 1
            elif(self.isTail(coord)):
                return(coord, True)
            else:
                assert False, "Unexpected value: " + str(value)

        return(coord, False)

    def isHead(self, x, y):
        for i in range(len(static.HEADS)):
            if(static.HEADS[i] == static.board[x][y]):
                return True
        return False

    def isBody(self, x, y):
        val = static.board[x][y]

        if(val == static.UP or val == static.DOWN or val == static.LEFT or val == static.RIGHT):
            return True
        return False

    def isTail(self, coord):
        val = static.board[coord.x][coord.y]

        for item in static.POSSIBLE_IDS:
            if(val == str(item)):
                return True
        return False

    # opposite of static var provided
    def oppositeDir(self, value, bHead=False):
        if(bHead):
            if(value == static.HEADS[0]):  # 'U'
                opp = static.HEADS[1]
            elif(value == static.HEADS[1]):  # 'D'
                opp = static.HEADS[0]
            elif(value == static.HEADS[2]):  # 'L'
                opp = static.HEADS[3]
            elif(value == static.HEADS[3]):  # 'R'
                opp = static.HEADS[2]
            else:
                assert False, "unknown value"
        else:
            if(value == static.UP):  # '^'
                opp = static.DOWN
            elif(value == static.DOWN):  # 'v'
                opp = static.UP
            elif(value == static.LEFT):  # '<'
                opp = static.RIGHT
            elif(value == static.RIGHT):  # '>'
                opp = static.LEFT
            else:
                assert False, "unknown value"

        return opp

    def convertToHeadSymbol(self, value):
        if(value == static.UP):  # '^'
            symbol = static.HEADS[0]
        elif(value == static.DOWN):  # 'v'
            symbol = static.HEADS[1]
        elif(value == static.LEFT):  # '<'
            symbol = static.HEADS[2]
        elif(value == static.RIGHT):  # '>'
            symbol = static.HEADS[3]
        else:
            assert False, "unknown value: " + str(value)
        return symbol

    def printCoords(self):
        string = str(self.location[0]) + " "
        for coord in self.location[1]:
            string += str(coord) + " "
        string += str(self.location[2])
        print(string)
