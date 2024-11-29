# Nonogram
solver for nonogram
https://en.wikipedia.org/wiki/Nonogram

This program operates with multiple arrays:
    1) Solution matrix in format of numpy array. The final nonogram is displayed here.
      "#" represents painted cells and "." empty cells (spaces between packs of painted cells).
      Only 100% known cell are painted here as "#" or ".". Rest has column index
    2) 2 arrays for rows and columns instructions. Both in format of list of list of int.
      Instruction lines has different length. Rows and Columns instructions are in same format,
      although columns instruction are usually vertical.
    3) List of 2D numpy arrays of all solutions for all lines (row or column).
      Each element of the list are all possible solutions for single line.
      Each row of 2D array is one of possible solution for the same line.
    4) List of all combinations, how to insert extra spaces to positions.
     For example [2,0,4,0,0], 2 spaces on 0th position and 4 spaces to 2nd position
     
     
     
Program steps:
    1) Reads instruction and picture dimensions from the file.
    2) Create empty matrix of given size.
    3) Fill the overlapping instruction to the matrix. 
    4) Create list of all possibilities, how to paint each row and column in the matrix.
    5) If any element is the same in all possibilities, only one solution is possible for the element.
       Program copy the element to the matrix.
    6) Program deletes all possibilities, which are in conflict with partly solved matrix.
    7) Repeat step 5) and 6) till nonogram is solved.
