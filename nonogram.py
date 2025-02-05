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

# Finds instructions for rows in instruction file, output them as 2D list of int.
def find_instructions_row(l_number_of_rows: int) -> List[List[int]]:
    with open(input_file, "r") as file:
        result = []
        no_of_lines_below_keyword = 0
        was_keyword = False
        for line in file:
            if "rows" in line:      # takes correct number of rows under the "rows" keyword
                was_keyword = True
            if was_keyword:
                if 0 < no_of_lines_below_keyword <= l_number_of_rows:   # starts 1 line below keyword
                    raw_line = []
                    result_line = []
                    raw_line = re.findall(r'\d+', line)     # list of strings
                    for item in raw_line:
                        result_line.append(int(item))              # convert to list of int
                    result.append(result_line)
                no_of_lines_below_keyword += 1
    return result

# Finds instructions for columns in instruction file, output them as 2D list of int.
def find_instructions_col(l_number_of_cols: int) -> List[List[int]]:
    with open(input_file, "r") as file:
        result = []
        no_of_lines_below_keyword = 0
        was_keyword = False
        for line in file:
            if "columns" in line:   # takes correct number of columns under the "columns" keyword
                was_keyword = True
            if was_keyword:
                if 0 < no_of_lines_below_keyword <= l_number_of_cols:   # starts 1 line below keyword
                    raw_line = []
                    result_line = []
                    raw_line = re.findall(r'\d+', line)     # list of strings
                    for item in raw_line:
                        result_line.append(int(item))              # convert to list of int
                    result.append(result_line)
                no_of_lines_below_keyword += 1
    return result

# sum of all rows instructions must be equal to the sum of all columns instructions
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

# Print solution matrix with column and row indexes and separator every 5 rows and columns
def print_matrix_debug(l_matrix) -> None:
    # print column indexes
    print("    ", end="")
    for idx, item in enumerate(l_matrix[0]):    # print col indexes
        if idx % 5 == 0:                        # column separator at the beginning of the row and every 5 columns
            print("|  ", end="")
        print(idx, " ", end="")
        if idx < 10:                            # 1 extra space for single digit indexes
            print(" ", end="")
    print()
    # print matrix
    for idx, row in enumerate(l_matrix):
        if idx % 5 == 0:                        # row separator every 5 rows
            print("      ", end="")
            [print("----", end="") for item in l_matrix[0]]
            print()
        print(idx, " ",end="")                  # row indexes
        if idx < 10:                            # 1 extra space for single digit indexes
            print(" ",end="")
        for idy, item in enumerate(row):
            if idy % 5 == 0:                    # column separator at the beginning of the row and every 5 columns
                print("|  ", end="")
            print(item," ",end="")
            if type(item) != int or item < 10:  # 1 extra space for single digit indexes
                print(" ",end="")
        print("|")                              # separator at the end of every row

# print final picture with only "#", so picture is clearly visible
def print_picture(l_matrix):
    for row in l_matrix:
        for item in row:
            print(item, " ", end="") if item == "#" else print("   ", end="")
        print()

# Line can be row or column of solution matrix.
# Maximum length of the pack is according to the number in instructions.
# If we move the whole pack to the one end of space available and then to the second end, there might be overlap.
# This overlap must be painted "#". It occurs for large pack in lines with small extra spaces.
# Function updates given line in solution matrix according to instructions for the same line
def paint_overlap_in_line(l_matrix_line: np.ndarray, l_instruction_line: List[int]) -> None:
    offset = 0      # minimal distance from the beginning of the line, where new pack can start
    for instruction_line_item in l_instruction_line:
        min_number_of_spaces = len(l_instruction_line) - 1      # at least 1 space between each packs of painted cells
        min_number_of_occupied_cells = sum(l_instruction_line) + min_number_of_spaces
        overlap = instruction_line_item + min_number_of_occupied_cells - len(l_matrix_line)
        if overlap > 0:  # paint overlap number of cells in the middle of available space for the pack
            for i in range(offset + instruction_line_item - overlap, offset + instruction_line_item):
                l_matrix_line[i] = "#"
        offset += instruction_line_item + 1     # mandatory space between each packs of painted cells

# Paint all overlaps for all rows and columns in solution matrix.
def paint_overlap (l_matrix: np.ndarray, l_rows_instruction: List[List[int]], l_cols_instruction: List[List[int]]) -> None:
    for row_index, row in enumerate(l_rows_instruction):
        paint_overlap_in_line(l_matrix[row_index,:], l_rows_instruction[row_index])
    for col_index, col in enumerate(l_cols_instruction):
        paint_overlap_in_line(l_matrix[:,col_index], l_cols_instruction[col_index])

# Line can be row or column.
# Checks, if line of solution matrix fulfill instruction line.
# Counts the length of the packs of painted cells and compare it with the instruction line.
def is_line_valid(l_matrix_line: np.ndarray, l_instruction_line: List[int]) -> bool:
    packs = []
    no_of_hashes = 0
    was_hash = False
    is_hash = False
    for item in l_matrix_line:
        if item == "#":
            is_hash = True
            no_of_hashes += 1                       # count number of painted cells in pack
        elif item == ".":
            is_hash = False
        if is_hash == False and was_hash == True:   # at the end of the pack, there is "." behind "#"
            packs.append(no_of_hashes)              # saves the pack length
            no_of_hashes = 0
        was_hash = is_hash
    if l_matrix_line[-1] == "#":                    # Pack can end at the end of the line, so there is no "." behind the pack
        packs.append(no_of_hashes)
    return packs == l_instruction_line              # compares packs lengths with instruction line

# Check, if each row and column of solution matrix fulfill instructions.
def is_solution_valid(l_matrix: np.ndarray, l_rows_instruction: List[List[int]], l_cols_instruction: List[List[int]]) -> bool:
    for row_index, row in enumerate(l_rows_instruction):
        if not is_line_valid(l_matrix[row_index,:], l_rows_instruction[row_index]):
            raise ValueError(f"solution not valid in row {row_index}")
    for col_index, row in enumerate(l_cols_instruction):
        if not is_line_valid(l_matrix[:,col_index], l_cols_instruction[col_index]):
            raise ValueError(f"solution not valid in row {col_index}")
    return True

# Returns the first solution for the line,
# all packs of cells are as close to the beginning of the line as possible
# Only 1 space between each pack is inserted.
# Only instructions for given line are considered. Independent of other lines.
def get_line_without_extra_spaces(l_matrix_line: np.ndarray, l_instruction_line: List[int]) -> np.ndarray:
    result = np.array([col for col in range(len(l_matrix_line))], dtype=object)     # empty line
    offset = 0                  # minimal distance from the beginning of the line, where new pack can start
    for instruction_line_index, instruction_line_item in enumerate(l_instruction_line):
        for i in range(offset, offset + instruction_line_item):
            result[i] = "#"
            offset += 1
        if instruction_line_index < len(l_instruction_line) - 1:    #no space behind last instruction
            result[offset] = "."                                    #space behind every instruction
            offset += 1
    return result

# generate list of all combinations how to distribute the fixed number of extra spaces to the fixed number of positions
# for example one of the combination of 6 spaces to 5 positions: [2,0,4,0,0], 2 spaces on 0th position and 4 spaces to 2nd position
def generate_combinations(l_spaces: int, l_no_of_positions: int) -> np.ndarray:
    def helper(spaces_left: int, current_combination: List[int] , current_position: int):
        if spaces_left == 0:                    # stop if we run out of spaces
            l_combinations.append(current_combination.copy())
            return
        if current_position >= l_no_of_positions:     # stop if we run out of positions
            return
        for i in range(spaces_left + 1):
            current_combination[current_position] = i
            helper(spaces_left - i, current_combination, current_position + 1)
            current_combination[current_position] = 0  # Reset for the next iteration

    l_combinations = []
    initial_combination = [0] * l_no_of_positions
    helper(l_spaces, initial_combination, 0)
    return np.array(l_combinations)

# Takes line without extra spaces and
# add extra spaces to positions according the single combination (l_single_combination_of_spaces)
# for example for combination [2,0,4,0,0], add 2 spaces on 0th position and 4 spaces to 2nd position
# output 1 possible solution for matrix line
def add_spaces_to_positions_in_line(l_possible_matrix_line: np.ndarray, l_instruction_line: List[int], l_single_combination_of_spaces: List[int]) -> np.ndarray:
    result = l_possible_matrix_line.copy()
    inserted_spaces = 0
    for combination_index, no_of_spaces_to_insert in enumerate(l_single_combination_of_spaces):
        if combination_index == 0:      #extra spaces at the beginning
            position = inserted_spaces
        else:
            position = sum(l_instruction_line[:combination_index]) + combination_index - 1 + inserted_spaces
        for space in range(no_of_spaces_to_insert):
            result = np.insert(result, position, ".")
            inserted_spaces += 1
    # We inserted spaces to the line. Extra elements at the end should be numbers, obsolete col indexes.
    # Check, if extra elements, which will be cut away, are not painted cells or spaces.
    # to do: check all deleted elements and check, if there is no col indexes left in the remaining line
    if (result[-inserted_spaces] == "#" or result[-inserted_spaces] == ".") and inserted_spaces > 0:
        raise ValueError("Too much spaces inserted. The extra element is . or # ")
    return result[:len(l_possible_matrix_line)]     # Cuts extra elements at the end of the line.

# 2D array of all possible solutions for single line. Each row is valid solution to the line according to the instructions
# It takes line without extra spaces and fill in extra spaces according to the single combination of spaces.
# And repeats it for all possible solutions for single line.
# All solutions belong to specific line, solved independently of other lines (rows or columns)
def create_all_possibilities_for_line(l_matrix_line: np.ndarray, l_instruction_line: List[int]) -> np.ndarray:
    result = []
    line_without_extra_spaces = get_line_without_extra_spaces(l_matrix_line, l_instruction_line)
    extra_spaces = len(l_matrix_line) - (sum(l_instruction_line) + len(l_instruction_line) - 1)     # extra spaces to fill line_without_extra_spaces
    no_of_positions = len(l_instruction_line) + 1

    all_combinations_of_spaces = generate_combinations(extra_spaces, no_of_positions)
    # count = 0       # for debugging, number of all combinations
    for single_combination_of_spaces in all_combinations_of_spaces:
        possible_line = add_spaces_to_positions_in_line(line_without_extra_spaces,l_instruction_line, single_combination_of_spaces)
        if not is_line_obsolete(l_matrix_line, possible_line):      # check, if possible line is not in conflict with partly solved matrix
            result.append(possible_line)
    #         count += 1
    #         if count % 10000 == 0:
    #             print(count)
    # print(count)
    return np.array(result)

# All solutions for individual lines are created in parallel on multiple cpu cores
# Each line (row or column) is solved in it's cpu core.
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
    return False

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

rows_instruction = find_instructions_row(number_of_rows)
cols_instruction = find_instructions_col(number_of_cols)

is_instruction_valid(rows_instruction, cols_instruction)

matrix = np.array([[col for col in range(number_of_cols)] for row in range(number_of_rows)], dtype=object)
previous_matrix = np.array([[0 for col in range(number_of_cols)] for row in range(number_of_rows)], dtype=object)

paint_overlap(matrix, rows_instruction, cols_instruction)

print()
print_matrix_debug(matrix)
print()

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
