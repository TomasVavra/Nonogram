# This program solves nonogram operates with multiple arrays:
#   1) Solution matrix in format of numpy array. The final nonogram is displayed here.
#       "#" represents painted cells and "." empty cells (spaces between packs of painted cels).
#       Only 100% known cell are painted here as "#" or ".". Rest has column index
#   2) 2 arrays for rows and columns instructions. Both in format of list of list of int.
#       Instruction lines has different length. Rows and Columns instructions are in same format,
#       although columns instruction are usually vertical.
#   3) List od 2D numpy arrays of all solutions for all lines (row or column).
#       Each element of the list are all possible solutions for single line.
#       Each row of 2D array is one of possible solution for the same line.

import re
import numpy as np
import itertools            # for combinatorics
from typing import List     # for Function Annotations in python 3.8

input_file = "instruction3.txt"

# Find number of rows and columns in instruction file.
def find_dimensions() -> List[int]:
    with open(input_file,"r") as file:
        result = [0 for x in range(2)]
        for l_line in file:
            if "rows" in l_line:
                result [0] = int(re.search(r'\d+', l_line)[0])
            if "columns" in l_line:
                result  [1]= int(re.search(r'\d+', l_line)[0])
    return result

# Finds instructions for rows in instruction file, output them as list of text.
def find_raw_instruction_rows(l_number_of_rows: int) -> List[str]:
    with open(input_file, "r") as file:
        result = []
        counter = 0
        start_counter = False
        for line in file:
            if "rows" in line:
                start_counter = True
            if start_counter:
                if 0 < counter <= l_number_of_rows:
                    result.append(line.strip())
                counter += 1
    return result

# Finds instructions for columns in instruction file, output them as list of text.
def find_raw_instruction_cols(l_number_of_cols: int) -> List[str]:
    with open(input_file, "r") as file:
        result = []
        counter = 0
        start_counter = False
        for line in file:
            if "columns" in line:
                start_counter = True
            if start_counter:
                if 0 < counter <= l_number_of_cols:
                    result.append(line.strip())
                counter += 1
    return result

# Converts instruction from the list of text to 2D list of int.
def convert_raw_instruction_to_2d_array(l_raw_instruction: List[str]) -> List[List[int]]:     #from list of strings to list of arrays
    result = []
    for line in l_raw_instruction:
        result.append(re.findall(r'\d+', line))     #find numbers, but it is List[List[str]
    for i, row in enumerate(result):                       #convert them to int
        for j, item in enumerate(row):
            result[i][j] = int(item)
    return result

# Combines functions to find instructions and convert them to 2D list of int.
def find_row_instruction() -> List[List[int]]:
    l_dimension = find_dimensions()
    rows_raw_instruction = find_raw_instruction_rows(l_dimension[0])
    result = convert_raw_instruction_to_2d_array(rows_raw_instruction)
    return result

# Combines functions to find instructions and convert them to 2D list of int.
def find_col_instruction() -> List[List[int]]:
    l_dimension = find_dimensions()
    cols_raw_instruction = find_raw_instruction_cols(l_dimension[1])
    result = convert_raw_instruction_to_2d_array(cols_raw_instruction)
    return result

# Print solution matrix in nice way with col and row indexes
def print_matrix(l_matrix) -> None:
    print("    ", end="")
    for idx, item in enumerate(l_matrix[0]):    #print col indexes
        if idx % 5 == 0:
            print("|  ", end="")
        print(idx, " ", end="")
        if idx < 10:
            print(" ", end="")
    print()
    for idx, row in enumerate(l_matrix):
        if idx%5 == 0:
            print("      ", end="")
            [print("----", end="") for item in l_matrix[0]]
            print()
        print(idx, " ",end="")
        if idx < 10:
            print(" ",end="")
        for idy, item in enumerate(row):
            if idy % 5 == 0:
                print("|  ", end="")
            print(item," ",end="")
            if type(item) != int or item < 10:
                print(" ",end="")
        print("|")

# Line can be row or column of solution matrix.
# If the line is densely occupied, there are overlaps in packs of cells, which must be painted "#"
def paint_overlap_in_line(l_matrix_line: np.ndarray, l_instruction_line: List[int]) -> None:
    offset = 0
    for instruction_line_item in l_instruction_line:
        overlap = instruction_line_item + sum(l_instruction_line) + len(l_instruction_line) - 1 - len(l_matrix_line)     #spaces = numbers in instruction(len()) -1
        if overlap > 0:
            for i in range(offset + instruction_line_item - overlap, offset + instruction_line_item):  # paint overlap in row
                l_matrix_line[i] = "#"
        offset += instruction_line_item + 1

# Paint all overlap for all rows and columns in solution matrix.
def paint_overlap (l_matrix: np.ndarray, l_rows_instruction: List[List[int]], l_cols_instruction: List[List[int]]) -> None:
    for row_index, row in enumerate(l_rows_instruction):
        paint_overlap_in_line(l_matrix[row_index,:], l_rows_instruction[row_index])
    for col_index, col in enumerate(l_cols_instruction):
        paint_overlap_in_line(l_matrix[:,col_index], l_cols_instruction[col_index])

# Check, if line of solution matrix fulfill instruction.
def is_line_valid(l_matrix_line: np.ndarray, l_instruction_line: List[int]) -> bool:
    groups = []
    counter = 0
    for item in l_matrix_line:
        if item == "#":
            counter += 1
        elif item == ".":
            groups.append(counter)
            counter = 0
    if counter > 0:
        groups.append(counter)
    return groups == l_instruction_line

# Check, if solution matrix fulfill instruction.
def is_solution_valid(l_matrix: np.ndarray, l_rows_instruction: List[List[int]], l_cols_instruction: List[List[int]]) -> bool:
    for row_index, row in enumerate(l_rows_instruction):
        l_matrix_line = l_matrix[row_index,:]
        if not is_line_valid(l_matrix_line, l_rows_instruction[row_index]):
            return False
    for col_index, row in enumerate(l_cols_instruction):
        l_matrix_line = l_matrix[:,col_index]
        if not is_line_valid(l_matrix_line, l_cols_instruction[col_index]):
            return False
    return True

# First solution for the line, all packs of cells are as left as possible.
# Only necessary spaces between packs are inserted.
# Only instructions for given line are considered. Independent of other lines.
def line_without_extra_spaces(l_matrix_line: np.ndarray, l_instruction_line: List[int]) -> np.ndarray:
    result = np.array([col for col in range(len(l_matrix_line))], dtype=object)
    matrix_line_index = 0
    for instruction_line_index, instruction_line_item in enumerate(l_instruction_line):
        for i in range(matrix_line_index, matrix_line_index + instruction_line_item):
            result[i] = "#"
            matrix_line_index += 1
        if instruction_line_index < len(l_instruction_line) - 1:    #no space behind last instruction
            result[matrix_line_index] = "."                         #space behind every instruction
            matrix_line_index += 1
    return result

# Add space to the position between two packs or at the beginning or at the end.
def add_space_to_single_position_in_line(l_matrix_line: np.ndarray, desired_position: int):
    result = np.copy(l_matrix_line)
    is_hash = False
    current_position = 0
    for index, item in enumerate(result):
        was_hash = is_hash
        is_hash = True if item == "#" else False
        if was_hash and not is_hash and desired_position == current_position or desired_position ==0:
            result = np.insert(result, index, ".")
            break
        if was_hash == False and is_hash == True:
            current_position +=1

    # error handling, too much spaces is inserted
    if result[-1] == "#" or result[-1] == ".":
        raise ValueError("Too much spaces is inserted. The extra element is . or # ")
    # copy result to original line without excess element
    for index, item in enumerate(l_matrix_line):
        l_matrix_line[index] = result[index]

# Add more spaces to more positions according the list
# for example [0,2,4,0,0], 2 spaces on 1st position and 4 spaces to 2nd position
def add_spaces_to_many_positions_in_line(l_matrix_line: np.ndarray, spaces_positions: List[int]):
    for position_index, spaces in enumerate(spaces_positions):
        for space in range(spaces):
            add_space_to_single_position_in_line(l_matrix_line, position_index)

# 2D array of all possible solutions for single line. Each row is valid solution to the line according to instructions
# All solutions belongs to specific line, solved independently of other lines (rows or columns)
def all_possibilities_for_line(l_matrix_line: np.ndarray, l_instruction_line: List[int]) -> np.ndarray:
    result = []
    extra_spaces = len(l_matrix_line) - (sum(l_instruction_line) + len(l_instruction_line) - 1)
    positions = len(l_instruction_line)+1

    #Generate all possible distributions of extra spaces to positions
    variations_with_replacement = list(itertools.product(range(extra_spaces +1), repeat=positions))
    count = 0       # for debugging, number of all variations
    for spaces_positions in variations_with_replacement:
        l_sum = 0
        for number in spaces_positions:
            l_sum += number
        if l_sum == extra_spaces:
            possible_line = np.copy(line_without_extra_spaces(l_matrix_line, l_instruction_line))
            add_spaces_to_many_positions_in_line(possible_line, spaces_positions)
            result.append(possible_line)
            count += 1
    return np.array(result)

# 3D array of all solutions for all rows or columns.
# List of 2D arrays of all solutions for each line.
def all_possibilities_for_all_lines(l_matrix: np.ndarray, l_rows_or_cols_instruction: List[List[int]], is_row: bool) -> List[np.ndarray]:
    result = []
    for line_index, instruction_line in enumerate(l_rows_or_cols_instruction):
        if is_row:
            result.append(all_possibilities_for_line(l_matrix[line_index,:], instruction_line))
        else:
            result.append(all_possibilities_for_line(l_matrix[:,line_index], instruction_line))
    return result

# Go through all possible solutions of single line. Paint cells, which are always "#" or ".".
def possibilities_overlap_for_line(l_matrix_line: np.ndarray, l_solutions: np.ndarray)
    for col_index_in_solutions in range(len(l_matrix_line)):
        all_same = np.all(l_solutions[:,col_index_in_solutions] == l_solutions[0,col_index_in_solutions])
        if all_same:
            l_matrix_line[col_index_in_solutions] = l_solutions[0,col_index_in_solutions]

# Go through all possible solutions of all rows and cols. Paint cells, which are always "#" or ".".
def possibilities_overlap(l_matrix: np.ndarray, l_rows_possibilities: List[np.ndarray], l_cols_possibilities: List[np.ndarray]):
    for row_index, row_possibilities in enumerate(l_rows_possibilities):
        possibilities_overlap_for_line(l_matrix[row_index,:], row_possibilities)
    for col_index, col_possibilities in enumerate(l_cols_possibilities):
        possibilities_overlap_for_line(l_matrix[:,col_index], col_possibilities)


dimension = find_dimensions()
number_of_rows = dimension[0]
number_of_cols = dimension[1]
rows_instruction = find_row_instruction()
cols_instruction = find_col_instruction()

matrix = np.array([[col for col in range(number_of_cols)] for row in range(number_of_rows)], dtype=object)

paint_overlap(matrix, rows_instruction, cols_instruction)


print()
print_matrix(matrix)
print()


matrix = np.array([[col for col in range(number_of_cols)] for row in range(number_of_rows)], dtype=object)

print()
print_matrix(matrix)
print()

rows_possibilities = all_possibilities_for_all_lines(matrix,rows_instruction, is_row = True)
cols_possibilities = all_possibilities_for_all_lines(matrix,cols_instruction, is_row = False)

possibilities_overlap(matrix, rows_possibilities, cols_possibilities)






print()
print_matrix(matrix)
print()











