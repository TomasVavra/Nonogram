import re
import numpy as np
from multiprocessing import Pool, cpu_count
from typing import List     # for Function Annotations in python 3.8

# not optimized for large input, as "instruction4.txt"
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

# sum of all instruction for row must be equal to the sum of all columns instruction
def is_instruction_valid(l_rows_instruction, l_cols_instruction):
    sum_row = 0
    for row in l_rows_instruction:
        for item in row:
            sum_row += item
    sum_col = 0
    for row in l_cols_instruction:
        for item in row:
            sum_col += item
    # error handling
    if sum_row != sum_col:
        raise ValueError("sum of row instruction != sum of cols instruction")

# Print solution matrix in nice way with col and row indexes
def print_matrix_debug(l_matrix) -> None:
    print("    ", end="")
    for idx, item in enumerate(l_matrix[0]):    #print col indexes
        if idx % 5 == 0:
            print("|  ", end="")
        print(idx, " ", end="")
        if idx < 10:
            print(" ", end="")
    print()
    for idx, row in enumerate(l_matrix):
        if idx%5 == 0:                          #row separator every 5 rows
            print("      ", end="")
            [print("----", end="") for item in l_matrix[0]]
            print()
        print(idx, " ",end="")
        if idx < 10:
            print(" ",end="")
        for idy, item in enumerate(row):
            if idy % 5 == 0:                    #col separator every 5 cols
                print("|  ", end="")
            print(item," ",end="")
            if type(item) != int or item < 10:
                print(" ",end="")
        print("|")

# print final picture with only "#"
def print_picture(l_matrix):
    for row in l_matrix:
        for item in row:
            print(item, " ", end="") if item == "#" else print("   ", end="")
        print()

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
    was_hash = False
    is_hash = False
    for item in l_matrix_line:
        if item == "#":
            is_hash = True
            counter += 1
        elif item == ".":
            is_hash = False
        if is_hash == False and was_hash == True:
            groups.append(counter)
            counter = 0
        was_hash = is_hash
    if l_matrix_line[-1] == "#":
        groups.append(counter)
    return groups == l_instruction_line

# Check, if solution matrix fulfill instruction.
def is_solution_valid(l_matrix: np.ndarray, l_rows_instruction: List[List[int]], l_cols_instruction: List[List[int]]) -> bool:
    for row_index, row in enumerate(l_rows_instruction):
        l_matrix_line = l_matrix[row_index,:]
        if not is_line_valid(l_matrix_line, l_rows_instruction[row_index]):
            raise ValueError(f"solution not valid in row {row_index}")
    for col_index, row in enumerate(l_cols_instruction):
        l_matrix_line = l_matrix[:,col_index]
        if not is_line_valid(l_matrix_line, l_cols_instruction[col_index]):
            raise ValueError(f"solution not valid in row {col_index}")
    return True

# First solution for the line, all packs of cells are as left as possible.
# Only necessary spaces between packs are inserted.
# Only instructions for given line are considered. Independent of other lines.
def get_line_without_extra_spaces(l_matrix_line: np.ndarray, l_instruction_line: List[int]) -> np.ndarray:
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

# generate list of all combinations how to distribute extra spaces to positions
def generate_combinations(l_spaces: int, l_positions: int) -> np.ndarray:
    def helper(spaces_left, current_combination, current_position):
        if spaces_left == 0:
            l_combinations.append(current_combination[:])
            return
        if current_position >= l_positions:
            return
        for i in range(spaces_left + 1):
            current_combination[current_position] = i
            helper(spaces_left - i, current_combination, current_position + 1)
            current_combination[current_position] = 0  # Reset for the next iteration

    l_combinations = []
    initial_combination = [0] * l_positions
    helper(l_spaces, initial_combination, 0)
    return np.array(l_combinations)

# Add extra spaces to positions according the list of combinations
# for example [2,0,4,0,0], 2 spaces on 0th position and 4 spaces to 2nd position
def add_spaces_to_positions_in_line(l_possible_matrix_line: np.ndarray, l_instruction_line: List[int], spaces_positions: List[int]) -> np.ndarray:
    result = l_possible_matrix_line
    inserted_spaces = 0
    for combination_index, combination_of_spaces in enumerate(spaces_positions):
        if combination_index == 0:  #extra spaces at the beginning
            position = 0 + inserted_spaces
        else:
            position = sum(l_instruction_line[:combination_index]) + combination_index -1 + inserted_spaces
        for space in range(combination_of_spaces):
            result = np.insert(result, position, ".")
            inserted_spaces += 1
    if (result[-inserted_spaces] == "#" or result[-inserted_spaces] == ".") and inserted_spaces > 0:
        raise ValueError("Too much spaces inserted. The extra element is . or # ")
    return result[:len(l_possible_matrix_line)]

# 2D array of all possible solutions for single line. Each row is valid solution to the line according to instructions
# All solutions belongs to specific line, solved independently of other lines (rows or columns)
def create_all_possibilities_for_line(l_matrix_line: np.ndarray, l_instruction_line: List[int]) -> np.ndarray:
    result = []
    extra_spaces = len(l_matrix_line) - (sum(l_instruction_line) + len(l_instruction_line) - 1)
    positions = len(l_instruction_line)+1
    line_without_extra_spaces = get_line_without_extra_spaces(l_matrix_line, l_instruction_line)

    combinations_of_spaces = generate_combinations(extra_spaces, positions)
    # count = 0       # for debugging, number of all combinations
    for spaces_positions in combinations_of_spaces:
        possible_line = add_spaces_to_positions_in_line(line_without_extra_spaces,l_instruction_line, spaces_positions)
        if not is_line_obsolete(l_matrix_line, possible_line):      #check possible line with matrix
            result.append(possible_line)
    #         count += 1
    #         if count % 10000 == 0:
    #             print(count)
    # print(count)
    return np.array(result)

# All solutions for individual lines are created in parallel on multiple cpu cores
def worker_task(l_matrix_line: np.ndarray, instruction_line: List[int], line_index: int, is_row: bool) -> np.ndarray:
    result = create_all_possibilities_for_line(l_matrix_line, instruction_line)
    if is_row:
        print("row ", line_index)
    else:
        print("col ", line_index)
    return result

# 3D array of all solutions for all rows or columns.
# List of 2D arrays of all solutions for each line.
def create_all_possibilities_for_all_lines(l_matrix: np.ndarray, l_rows_or_cols_instruction: List[List[int]], is_row: bool) -> List[np.ndarray]:
    tasks = []
    if is_row:
        tasks = [(l_matrix[line_index, :], instruction_line, line_index, is_row) for line_index, instruction_line in
                 enumerate(l_rows_or_cols_instruction)]
    else:
        tasks = [(l_matrix[:, line_index], instruction_line, line_index, is_row) for line_index, instruction_line in
                 enumerate(l_rows_or_cols_instruction)]

    with Pool(processes=cpu_count()) as pool:
        result = pool.starmap(worker_task, tasks)

    return result

# Go through all possible solutions of single line. Paint cells, which are always "#" or ".".
def possibilities_overlap_for_line(l_matrix_line: np.ndarray, l_single_line_possibilities: np.ndarray):
    for col_index_in_possibilities in range(len(l_matrix_line)):
        all_same = np.all(l_single_line_possibilities[:,col_index_in_possibilities] == l_single_line_possibilities[0,col_index_in_possibilities])
        if all_same:
            l_matrix_line[col_index_in_possibilities] = l_single_line_possibilities[0,col_index_in_possibilities]

# Go through all possible solutions of all rows and cols. Paint cells, which are always "#" or ".".
def possibilities_overlap(l_matrix: np.ndarray, l_all_rows_possibilities: List[np.ndarray], l_all_cols_possibilities: List[np.ndarray]):
    for row_index, single_row_possibilities in enumerate(l_all_rows_possibilities):
        possibilities_overlap_for_line(l_matrix[row_index,:], single_row_possibilities)
    for col_index, single_col_possibilities in enumerate(l_all_cols_possibilities):
        possibilities_overlap_for_line(l_matrix[:,col_index], single_col_possibilities)

# Is possible solution for line in conflict with partly solved matrix?
def is_line_obsolete(l_matrix_line: np.ndarray, l_line_possibility: np.ndarray) -> bool:
    for matrix_index, matrix_item in enumerate(l_matrix_line):
        if (matrix_item == "#" or matrix_item == ".") and matrix_item != l_line_possibility[matrix_index]:
            return True

# delete possibilities of single line, which are already in conflict with partly solved matrix. Return the rest.
def delete_obsolete_possibilities_for_line(l_matrix_line: np.ndarray, l_single_line_possibilities: np.ndarray) -> np.ndarray:
    rows_to_delete = []
    for row_index, row in enumerate(l_single_line_possibilities):
        if is_line_obsolete(l_matrix_line, np.array(row)):
            rows_to_delete.append(row_index)
    result = np.delete(l_single_line_possibilities, rows_to_delete, axis=0)
    return result

# delete possibilities of all lines (all rows or all cols), which are already in conflict with partly solved matrix. Return the rest.
def delete_obsolete_possibilities_for_all_lines(l_matrix: np.ndarray, l_all_lines_possibilities: List[np.ndarray], is_row: bool) -> List[np.ndarray]:
    result = []
    for line_index, single_line_possibilities in enumerate(l_all_lines_possibilities):
        if is_row:
            result.append(delete_obsolete_possibilities_for_line(l_matrix[line_index, :], single_line_possibilities))
        else:
            result.append(delete_obsolete_possibilities_for_line(l_matrix[:, line_index], single_line_possibilities))
    return result


dimension = find_dimensions()
number_of_rows = dimension[0]
number_of_cols = dimension[1]
rows_instruction = find_row_instruction()
cols_instruction = find_col_instruction()
is_instruction_valid(rows_instruction, cols_instruction)

matrix = np.array([[col for col in range(number_of_cols)] for row in range(number_of_rows)], dtype=object)
previous_matrix = np.array([[0 for col in range(number_of_cols)] for row in range(number_of_rows)], dtype=object)

paint_overlap(matrix, rows_instruction, cols_instruction)

print()
print_matrix_debug(matrix)
print()

# instruction_line = rows_instruction[15]
# matrix_line = matrix[15,:]
# spaces_positions = [0,0,0,0]
# l_possible_matrix_line = get_line_without_extra_spaces(matrix_line, instruction_line)
# print(instruction_line)
# print(matrix_line)
# print(l_possible_matrix_line)
# new_line = add_spaces_to_many_positions_in_line(l_possible_matrix_line, instruction_line, spaces_positions)
# print(new_line)

#create possibilities
rows_possibilities = create_all_possibilities_for_all_lines(matrix,rows_instruction, is_row = True)
cols_possibilities = create_all_possibilities_for_all_lines(matrix,cols_instruction, is_row = False)

#update possibilities and matrix till matrix is changing
while not np.array_equal(previous_matrix, matrix):
    previous_matrix = np.copy(matrix)
    possibilities_overlap(matrix, rows_possibilities, cols_possibilities)
    rows_possibilities = delete_obsolete_possibilities_for_all_lines(matrix, rows_possibilities, is_row = True)
    cols_possibilities = delete_obsolete_possibilities_for_all_lines(matrix, cols_possibilities, is_row = False)


print()
print_matrix_debug(matrix)
print()

print()
print_picture(matrix)
print()
print(" Is solution valid? ",is_solution_valid(matrix, rows_instruction, cols_instruction))
