#!/usr/bin/python

import sys
import time

from Maze import *
import static
import util
import os

puzzle = 'puzzle1.txt'
folder = "puzzles/"

override_puzzle = sys.argv[1:]
if override_puzzle:
    puzzle = str(override_puzzle[0])
	
puzzle_path = os.path.normcase(folder + puzzle)

print("Using puzzle file: " + puzzle)

# Check to see if file exists, if not exit
try:
    with open(puzzle_path):
        pass
except IOError:
    print(puzzle + " does not exist. Quiting program")
    sys.exit(1)

start = time.clock()

maze = Maze(puzzle_path)
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
solution_dir = "solutions/"
solution_name = "solution_" + puzzle
solution_path = os.path.normcase(solution_dir + solution_name)

if not os.path.exists(solution_dir):
    os.makedirs(solution_dir)
	
with open(solution_path, 'w') as file:
    file.write(solText)
