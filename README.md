py-TJ-Wriggle Solver
=================

A messy solver for TJ-Wriggle using A* search that reads in a puzzle file through command line. More information on the TJ-Wriggle puzzle [here](http://www.clickmazes.com/tjwrig/ixjwrig.htm)

Only tested with Python 3. The library [pyTree](https://github.com/caesar0301/pyTree) is modified and included in this repo. 

##How to Run
Install requirements

To run with default puzzle: python main.py

To run with an alternate puzzle: python main.py foobar.txt

##How Puzzles Are Defined
Puzzles are defined with their width, height, and number of wrigglers
on the first line, followed by a grid of characters representing the
puzzle. An `e` represents an empty space, and an `x` represents a wall.
Wrigglers are represented with their head as one of {`U`, `D`, `L`, `R`},
representing the direction of the next segment. Internal segments are
represented as one of {`^`, `v`, `<`, `>`}, an arrow pointing at the next segment.
The tail is represented as a number, the index of the wriggler.
The blue "player" wriggler that must reach the goal has index 0.

##Solution Files
We display each move in the solution ending with the move to the final state, display the final board state, display the wall time expended, and display the amount of moves in the solution. Each move must be displayed in a separate row consisting of the wriggler ID as specified in the puzzle file, followed by a bit indicating whether the head (0) or tail (1) is being moved, followed by an ordered pair of coordinates (column, row) designating the destination space where the top-left corner is designated as `0 0`. After outputting the path, we output the final board state, followed by a number indicating wall time, followed by a row containing an integer indicating the number of moves in your solution.

