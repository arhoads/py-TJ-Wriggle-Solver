from Maze import *
import time
import static


def stepThroughSolution(maze, solText):
    maze.clearMaze()
    for line in solText.split("\n"):
        data = line.split(' ')
        if(len(data)) <= 1:
            break
        bHead = (data[1] == '0')
        wriggler = maze.wrigglers[int(data[0])]
        movedCoord = Coord(int(data[2]), int(data[3]))

        if(bHead):
            symbol = wriggler.getSymbol(wriggler.location[0], movedCoord)
        else:
            symbol = wriggler.getSymbol(wriggler.location[2], movedCoord)
        symbol = wriggler.convertToHeadSymbol(symbol)
        wriggler.move(symbol, bHead, True)
        print('\nNext move')
        printBoard()
        time.sleep(1)


# board must be 2d list
def printBoard(graph=None):
    string = ''
    if(graph is None):
        xRange = static.columns
        yRange = static.rows
        graph = static.board
    else:
        xRange = len(graph[0])
        yRange = len(graph)

    # x: columns, y:rows
    for y in range(yRange):
        for x in range(xRange):
            string += str(graph[x][y]) + " "
            print(str(graph[x][y]) + " ", end='')
        string += "\n"
        print("")  # newline
    return string
