import numpy as np
def is_valid(matrix, row_constraints, col_constraints):
    for i, row in enumerate(matrix):
        if not check_line(row, row_constraints[i]):
            return False
    for j, col in enumerate(matrix.T):
        if not check_line(col, col_constraints[j]):
            return False
    return True

def check_line(line, constraints):
    groups = []
    count = 0
    for cell in line:
         if cell == 1:
             count += 1
         elif count > 0:
             groups.append(count)
             count = 0
    if count > 0:
        groups.append(count)
    return groups == constraints

def solve_nonogram(matrix, row_constraints, col_constraints, row=0, col=0):
    if row == len(matrix):
        return is_valid(matrix, row_constraints, col_constraints)
    if col == len(matrix[0]):
        return solve_nonogram(matrix, row_constraints, col_constraints, row + 1, 0)
    for value in [0, 1]:
        matrix[row][col] = value
        if solve_nonogram(matrix, row_constraints, col_constraints, row, col + 1):
            return True
        matrix[row][col] = -1
    return False

def print_matrix(matrix):
    for row in matrix:
        print("".join(['#' if cell == 1 else '.' for cell in row]))

# Example constraints
row_constraints = [[3], [2, 1], [3], [1, 1], [5]]
col_constraints = [[1, 1], [3], [1, 1], [3], [1, 1]]
# Initialize the matrix with -1 (unknown)
matrix = np.full((len(row_constraints), len(col_constraints)), -1)
if solve_nonogram(matrix, row_constraints, col_constraints):
    print("Solution found:")
    print_matrix(matrix)
else:
    print("No solution found.")




