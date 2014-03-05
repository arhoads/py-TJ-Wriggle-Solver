from Coord import *
from Wriggler import *
from State import *
from Action import *
import static
import util
import math

from treelib import *
from node import Node
from pqdict import PQDict


class Maze:

    def __init__(self, puzzleFile):
        self.wrigglers = []  # Sorted list by ID
        self.parsePuzzleFile(puzzleFile)
        self.tree = Tree()

    def parsePuzzleFile(self, filename):
        f = open(filename, 'r')

        columns, rows, numWrigglers = f.readline().split()
        static.columns = int(columns)
        static.rows = int(rows)

        static.board = [['-1' for y in range(static.rows)] for x in range(static.columns)]

        for y in range(static.rows):
            line = f.readline().split()
            for x in range(len(line)):
                static.board[x][y] = line[x]

        assert len(static.board) == static.columns
        assert len(static.board[0]) == static.rows

        static.goal = Coord(static.columns - 1, static.rows - 1)

        for _ in range(int(numWrigglers)):
            self.wrigglers.append(self.makeWriggler())

        self.wrigglers.sort()

        print("Empty board")
        util.printBoard()

    def clearMaze(self):
        for y in range(static.rows):
            for x in range(static.columns):
                if(static.board[x][y] != static.WALL):
                    static.board[x][y] = static.EMPTY

    def makeWriggler(self):
        wriggler = Wriggler()

        bodyCoords = []
        tailCoord = None

        breakOut = False
        # Find head
        for y in range(static.rows):
            for x in range(static.columns):
                if(wriggler.isHead(x, y)):
                    headCoord = Coord(x, y)
                    breakOut = True
                    break
            if(breakOut):
                break

        nextCoord = Coord(newCoord=headCoord)

        bFirst = True
        while(True):
            oldCoord = Coord(newCoord=nextCoord)

            if(bFirst):
                nextCoord, _ = wriggler.followBody(nextCoord, True)
                static.board[oldCoord.x][oldCoord.y] = static.EMPTY
                bFirst = False
            else:
                nextCoord, isTail = wriggler.followBody(nextCoord)

                if(isTail):
                    tailCoord = Coord(newCoord=nextCoord)
                    wrigglerID = int(static.board[tailCoord.x][tailCoord.y])
                    static.board[tailCoord.x][tailCoord.y] = static.EMPTY
                    break

                static.board[oldCoord.x][oldCoord.y] = static.EMPTY
                bodyCoords.append(Coord(newCoord=oldCoord))

        wrigglerCoords = [headCoord, bodyCoords, tailCoord]

        wriggler.location = wrigglerCoords
        wriggler.id = wrigglerID

        return wriggler

    def testGoal(self, state):
        inGoal = False
        wriggler = state.wrigglers[0]  # assuming sorted
        inGoal = self.checkGoal(wriggler.location[0]) or self.checkGoal(wriggler.location[2])
        if(inGoal):
            return True

        return inGoal

    # Returns true if coords are goal coords
    def checkGoal(self, coord):
        return coord.x == static.goal.x and coord.y == static.goal.y

    def getWrigglerLocations(self):
        wrigglerLocs = []
        for wriggler in self.wrigglers:
            wrigglerLocs.append(wriggler.location)
        return wrigglerLocs

    # Run normal heuristic
    def a_star_normal(self):
        return self.a_star(self.heuristic)

    def a_star(self, heuristic):
        node = self.tree.create_node(state=State(self.wrigglers), pathCost=0)
        node.heuristic = heuristic(node)

        frontier = PQDict()
        stateFrontier = {}
        explored = {}

        # Sacrifice memory to have a huge speed up being able to instantly check for state in frontier
        stateFrontier[str(node.state)] = node.heuristic
        frontier.additem(node._identifier, node.heuristic)

        while(True):
            if(len(frontier) == 0):
                return None

            nodeID = frontier.popitem()[0]
            node = self.tree.get_node(nodeID)
            nodeStateStr = str(node.state)

            del stateFrontier[nodeStateStr]

            if self.testGoal(node.state):
                return node

            explored[nodeStateStr] = -1  # we don't care what the hash matches
            actions = self.getActions(node.state)
            for action in actions:
                child = self.childNode(node, action)
                child.heuristic = heuristic(child)
                childStr = str(child.state)

                inExplored = False
                inFrontier = False

                if childStr in explored:
                    inExplored = True

                bGreater = False
                if childStr in stateFrontier:
                    if(stateFrontier[childStr] < child.heuristic + child.pathCost):
                        bGreater = True
                    inFrontier = True

                if(not inExplored and not inFrontier):
                    stateFrontier[childStr] = child.heuristic
                    frontier.additem(child._identifier, child.heuristic + child.pathCost)
                elif(bGreater):
                    bHappened = False
                    for key in frontier:
                        if(str(self.tree.get_node(key).state) == childStr):
                            bHappened = True
                            frontier.pop(key)
                            frontier.additem(child._identifier, child.heuristic + child.pathCost)
                            break
                    assert bHappened

    # Optimistic manhatten distance, but still terrible
    def heuristic(self, node):
        wriggler = node.state.wrigglers[0]

        headDiffX = static.goal.x - wriggler.location[0].x
        headDiffY = static.goal.y - wriggler.location[0].y
        headDiff = headDiffX + headDiffY

        tailDiffX = static.goal.x - wriggler.location[2].x
        tailDiffY = static.goal.y - wriggler.location[2].y
        tailDiff = tailDiffX + tailDiffY

        return min(headDiff, tailDiff)

    def euclidean_distance(self, coord0, coord1):
        return math.sqrt((coord0.x - coord1.x) ** 2 + (coord0.y - coord1.y) ** 2)

    def generateSolution(self, goalNode):
        parentID = goalNode._bpointer
        actions = []
        text = ''
        actions.append(goalNode.action)

        while(parentID is not None):
            parentNode = self.tree.get_node(parentID)
            actions.append(parentNode.action)
            parentID = parentNode._bpointer

        actLength = 0
        for action in reversed(actions):
            if(action is not None):
                if(action.headMoved):
                    headVal = '0'
                else:
                    headVal = '1'
                actLength += 1
                text += str(action.wrigglerID) + " " + headVal + " " + str(action.movedCoord.x) + " " + str(action.movedCoord.y) + "\n"

        return text, actLength

    def getActions(self, state):
        actions = []
        wrigglers = state.wrigglers

        self.clearMaze()
        self.updateAllMaze(state.wrigglers)

        for i in range(len(wrigglers)):
            moves = wrigglers[i].getPossibleMoves()

            for move in moves:
                actions.append(Action(wrigglerID=i, movedCoord=move[0], headMoved=move[1]))

        return actions

    def updateAllMaze(self, wrigglers, bNot0=False):
        if(bNot0):
            for i in range(1, len(wrigglers)):
                wrigglers[i].updateMaze()
        else:
            for wriggler in wrigglers:
                wriggler.updateMaze()

    def childNode(self, parent, action):
        newState = State(parent.state.wrigglers, True)

        wriggler = newState.wrigglers[action.wrigglerID]

        if(action.headMoved):
            symbol = wriggler.getSymbol(wriggler.location[0], action.movedCoord)
        else:
            symbol = wriggler.getSymbol(wriggler.location[2], action.movedCoord)
        symbol = wriggler.convertToHeadSymbol(symbol)
        wriggler.move(symbol, action.headMoved)

        return self.tree.create_node(pathCost=parent.pathCost + 1, parent=parent._identifier, state=newState, action=action)

    def getDepth(self, node):
        parentID = node._bpointer
        depth = 0
        if(parentID is None):
            return depth

        while(parentID is not None):
            depth += 1
            parentNode = self.tree.get_node(parentID)
            parentID = parentNode._bpointer

        return depth
