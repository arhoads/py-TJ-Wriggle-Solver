#!/usr/bin/python

import sys
import time

from Maze import *
import static
import util


puzzle = 'puzzle1.txt'

override_puzzle = sys.argv[1:]
if override_puzzle:
    puzzle = str(override_puzzle[0])

print("Using puzzle file: " + puzzle)

# Check to see if file exists, if not exit
try:
    with open(puzzle):
        pass
except IOError:
    print(puzzle + " does not exist. Quiting program")
    sys.exit(1)

start = time.clock()

maze = Maze(puzzle)
solNode = maze.a_star_normal()

end = time.clock()
timeDelta = str(end - start)

if(solNode is None):
    print("Solution NOT found!")
    sys.exit(1)

solText, solveLength = maze.generateSolution(solNode)

#util.stepThroughSolution(maze, solText) # Debugging function

print("\nSolved board")
for wriggler in solNode.state.wrigglers:
    wriggler.updateMaze()
boardStr = util.printBoard()

print("\nTime elapsed: " + timeDelta + " (seconds)")

solText += boardStr + timeDelta + "\n" + str(solveLength) + "\n"
filename = "solution_" + puzzle
with open(filename, 'w') as file:
    file.write(solText)
