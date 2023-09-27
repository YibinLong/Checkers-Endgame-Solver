# Checkers Endgame Solver

This checkers endgame solver finds the optimal moves for a given checkers endgame position in order to win. 

The solver uses the minimax algorithm with alpha-beta pruning to find the optimal moves. Node ordering is implemented so that maximum pruning occurs. The solver also uses state caching, which allows the solver to check if a given state is already in the cached dictionary, reducing repetitive evaluations of states.

## Usage
1. Clone the repository and navigate to the directory
2. Use the following command, specifying the necessary input files and the output file:

`python checkers.py --inputfile <input file> --outputfile <output file>`

- Replace `<input file>` with an input board state file.
- Replace `<output file>` with the new output file name.

## Example
If we have the starting checkers board state board1.txt, and we want the optimal solution for the red player output to output.txt, we would run the following command:

`python checkers.py --inputfile board1.txt --outputfile output.txt`

## Input File Format
- A checkers board state is a grid of 64 characters, with eight rows and eight characters per row.
- ’.’ is an empty square.
- ’r’ is a red piece,
- ’b’ is a black piece,
- ’R’ is a red king,
- ’B’ is a black king.