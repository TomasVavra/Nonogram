import re
import numpy as np
from multiprocessing import Pool, cpu_count
from typing import List     # for Function Annotations in python 3.8


# Find number of rows and columns in instruction file.
def find_dimensions(input_file) -> List[int]:
    with open(input_file,"r") as file:
        result = [0, 0]
        for line in file:
            if "rows" in line:
                result [0] = int(re.search(r'\d+', line)[0])
            if "columns" in line:
                result  [1]= int(re.search(r'\d+', line)[0])
    return result

# Finds instructions for rows in instruction file, output them as 2D list of int.
def find_instructions_row(input_file, number_of_rows: int) -> List[List[int]]:
    with open(input_file, "r") as file:
        result = []
        no_of_lines_below_keyword = 0
        was_keyword = False
        for line in file:
            if "rows" in line:      # takes correct number of rows under the "rows" keyword
                was_keyword = True
            if was_keyword:
                if 0 < no_of_lines_below_keyword <= number_of_rows:   # starts 1 line below keyword
                    raw_line = []
                    result_line = []
                    raw_line = re.findall(r'\d+', line)     # list of strings
                    for item in raw_line:
                        result_line.append(int(item))              # convert to list of int
                    result.append(result_line)
                no_of_lines_below_keyword += 1
    return result

# Finds instructions for columns in instruction file, output them as 2D list of int.
def find_instructions_col(input_file, number_of_cols: int) -> List[List[int]]:
    with open(input_file, "r") as file:
        result = []
        no_of_lines_below_keyword = 0
        was_keyword = False
        for line in file:
            if "columns" in line:   # takes correct number of columns under the "columns" keyword
                was_keyword = True
            if was_keyword:
                if 0 < no_of_lines_below_keyword <= number_of_cols:   # starts 1 line below keyword
                    raw_line = []
                    result_line = []
                    raw_line = re.findall(r'\d+', line)     # list of strings
                    for item in raw_line:
                        result_line.append(int(item))              # convert to list of int
                    result.append(result_line)
                no_of_lines_below_keyword += 1
    return result

# sum of all rows instructions must be equal to the sum of all columns instructions
def is_instruction_valid(rows_instruction, cols_instruction):
    sum_row = 0
    for row in rows_instruction:
        for item in row:
            sum_row += item
    sum_col = 0
    for row in cols_instruction:
        for item in row:
            sum_col += item
    # error handling
    if sum_row != sum_col:
        raise ValueError("sum of row instruction != sum of cols instruction")
    else:
        print("instructions valid")

# Print solution matrix with column and row indexes and separator every 5 rows and columns
def print_matrix_debug(matrix) -> None:
    # print column indexes
    print("    ", end="")
    for idx, item in enumerate(matrix[0]):    # print col indexes
        if idx % 5 == 0:                        # column separator at the beginning of the row and every 5 columns
            print("|  ", end="")
        print(idx, " ", end="")
        if idx < 10:                            # 1 extra space for single digit indexes
            print(" ", end="")
    print()
    # print matrix
    for idx, row in enumerate(matrix):
        if idx % 5 == 0:                        # row separator every 5 rows
            print("      ", end="")
            [print("----", end="") for item in matrix[0]]
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
def print_picture(matrix):
    for row in matrix:
        for item in row:
            print(item, " ", end="") if item == "#" else print("   ", end="")
        print()

# Line can be row or column of solution matrix.
# Maximum length of the pack is according to the number in instructions.
# If we move the whole pack to the one end of space available and then to the second end, there might be overlap.
# This overlap must be painted "#". It occurs for large pack in lines with small extra spaces.
# Function updates given line in solution matrix according to instructions for the same line
def paint_overlap_in_line(matrix_line: np.ndarray, instruction_line: List[int]) -> None:
    offset = 0      # minimal distance from the beginning of the line, where new pack can start
    for instruction_line_item in instruction_line:
        min_number_of_spaces = len(instruction_line) - 1      # at least 1 space between each packs of painted cells
        min_number_of_occupied_cells = sum(instruction_line) + min_number_of_spaces
        overlap = instruction_line_item + min_number_of_occupied_cells - len(matrix_line)
        if overlap > 0:  # paint overlap number of cells in the middle of available space for the pack
            for i in range(offset + instruction_line_item - overlap, offset + instruction_line_item):
                matrix_line[i] = "#"
        offset += instruction_line_item + 1     # mandatory space between each packs of painted cells

# Paint all overlaps for all rows and columns in solution matrix.
def paint_overlap (matrix: np.ndarray, rows_instruction: List[List[int]], cols_instruction: List[List[int]]) -> None:
    for row_index, row in enumerate(rows_instruction):
        paint_overlap_in_line(matrix[row_index,:], rows_instruction[row_index])
    for col_index, col in enumerate(cols_instruction):
        paint_overlap_in_line(matrix[:,col_index], cols_instruction[col_index])

# Line can be row or column.
# Checks, if line of solution matrix fulfill instruction line.
# Counts the length of the packs of painted cells and compare it with the instruction line.
def is_line_valid(matrix_line: np.ndarray, instruction_line: List[int]) -> bool:
    packs = []
    no_of_hashes = 0
    was_hash = False
    is_hash = False
    for item in matrix_line:
        if item == "#":
            is_hash = True
            no_of_hashes += 1                       # count number of painted cells in pack
        elif item == ".":
            is_hash = False
        if is_hash == False and was_hash == True:   # at the end of the pack, there is "." behind "#"
            packs.append(no_of_hashes)              # saves the pack length
            no_of_hashes = 0
        was_hash = is_hash
    if matrix_line[-1] == "#":                    # Pack can end at the end of the line, so there is no "." behind the pack
        packs.append(no_of_hashes)
    return packs == instruction_line              # compares packs lengths with instruction line

# Check, if each row and column of solution matrix fulfill instructions.
def is_solution_valid(matrix: np.ndarray, rows_instruction: List[List[int]], cols_instruction: List[List[int]]) -> bool:
    for row_index, row in enumerate(rows_instruction):
        if not is_line_valid(matrix[row_index,:], rows_instruction[row_index]):
            raise ValueError(f"solution not valid in row {row_index}")
    for col_index, row in enumerate(cols_instruction):
        if not is_line_valid(matrix[:,col_index], cols_instruction[col_index]):
            raise ValueError(f"solution not valid in column {col_index}")
    print("Solution is valid")

# Returns the first solution for the line,
# all packs of cells are as close to the beginning of the line as possible
# Only 1 space between each pack is inserted.
# Only instructions for given line are considered. Independent of other lines.
def get_line_without_extra_spaces(matrix_line: np.ndarray, instruction_line: List[int]) -> np.ndarray:
    result = np.array([col for col in range(len(matrix_line))], dtype=object)     # empty line
    offset = 0                  # minimal distance from the beginning of the line, where new pack can start
    for instruction_line_index, instruction_line_item in enumerate(instruction_line):
        for i in range(offset, offset + instruction_line_item):
            result[i] = "#"
            offset += 1
        if instruction_line_index < len(instruction_line) - 1:    #no space behind last instruction
            result[offset] = "."                                    #space behind every instruction
            offset += 1
    return result

# generate list of all combinations how to distribute the fixed number of extra spaces to the fixed number of positions
# for example one of the combination of 6 spaces to 5 positions: [2,0,4,0,0], 2 spaces on 0th position and 4 spaces to 2nd position
def generate_combinations(spaces: int, no_of_positions: int) -> np.ndarray:
    def helper(spaces_left: int, current_combination: List[int] , current_position: int):
        if spaces_left == 0:                    # stop if we run out of spaces
            combinations.append(current_combination.copy())
            return
        if current_position >= no_of_positions:     # stop if we run out of positions
            return
        for i in range(spaces_left + 1):
            current_combination[current_position] = i
            helper(spaces_left - i, current_combination, current_position + 1)
            current_combination[current_position] = 0  # Reset for the next iteration

    combinations = []
    initial_combination = [0] * no_of_positions
    helper(spaces, initial_combination, 0)
    return np.array(combinations)

# Takes line without extra spaces and
# add extra spaces to positions according the single combination (single_combination_of_spaces)
# for example for combination [2,0,4,0,0], add 2 spaces on 0th position and 4 spaces to 2nd position
# output 1 possible solution for matrix line
def add_spaces_to_positions_in_line(possible_matrix_line: np.ndarray, instruction_line: List[int], single_combination_of_spaces: List[int]) -> np.ndarray:
    result = possible_matrix_line.copy()
    inserted_spaces = 0
    for combination_index, no_of_spaces_to_insert in enumerate(single_combination_of_spaces):
        if combination_index == 0:      #extra spaces at the beginning
            position = inserted_spaces
        else:
            position = sum(instruction_line[:combination_index]) + combination_index - 1 + inserted_spaces
        for space in range(no_of_spaces_to_insert):
            result = np.insert(result, position, ".")
            inserted_spaces += 1
    # We inserted spaces to the line. Extra elements at the end should be numbers, obsolete col indexes.
    # Check, if extra elements, which will be cut away, are not painted cells or spaces.
    # to do: check all deleted elements and check, if there is no col indexes left in the remaining line
    if (result[-inserted_spaces] == "#" or result[-inserted_spaces] == ".") and inserted_spaces > 0:
        raise ValueError("Too much spaces inserted. The extra element is . or # ")
    return result[:len(possible_matrix_line)]     # Cuts extra elements at the end of the line.

# 2D array of all possible solutions for single line. Each row is valid solution to the line according to the instructions
# It takes line without extra spaces and fill in extra spaces according to the single combination of spaces.
# And repeats it for all possible solutions for single line.
# All solutions belong to specific line, solved independently of other lines (rows or columns)
def create_all_possibilities_for_line(matrix_line: np.ndarray, instruction_line: List[int]) -> np.ndarray:
    result = []
    line_without_extra_spaces = get_line_without_extra_spaces(matrix_line, instruction_line)
    extra_spaces = len(matrix_line) - (sum(instruction_line) + len(instruction_line) - 1)     # extra spaces to fill line_without_extra_spaces
    no_of_positions = len(instruction_line) + 1

    all_combinations_of_spaces = generate_combinations(extra_spaces, no_of_positions)
    # no_of_combinations = 0       # for debugging, number of all combinations
    for single_combination_of_spaces in all_combinations_of_spaces:
        possible_line = add_spaces_to_positions_in_line(line_without_extra_spaces,instruction_line, single_combination_of_spaces)
        if not is_line_obsolete(matrix_line, possible_line):      # check, if possible line is not in conflict with partly solved matrix
            result.append(possible_line)
    #         no_of_combinations += 1
    #         if no_of_combinations % 10000 == 0:
    #             print(no_of_combinations)
    # print(no_of_combinations)
    return np.array(result)

# All solutions for individual lines are created in parallel on multiple cpu cores.
# Each line (row or column) is solved in it's cpu core.
def worker_task(matrix_line: np.ndarray, instruction_line: List[int], line_index: int, is_row: bool) -> np.ndarray:
    result = create_all_possibilities_for_line(matrix_line, instruction_line)
    if is_row:
        print("row ", line_index)
    else:
        print("col ", line_index)
    return result

# 3D array of all solutions for all rows or columns.
# List of 2D arrays of all solutions for each line.
def create_all_possibilities_for_all_lines(matrix: np.ndarray, rows_or_cols_instruction: List[List[int]], is_row: bool) -> List[np.ndarray]:
    tasks = []
    if is_row:
        tasks = [(matrix[line_index, :], instruction_line, line_index, is_row) for line_index, instruction_line in
                 enumerate(rows_or_cols_instruction)]
    else:
        tasks = [(matrix[:, line_index], instruction_line, line_index, is_row) for line_index, instruction_line in
                 enumerate(rows_or_cols_instruction)]

    with Pool(processes=cpu_count()) as pool:
        result = pool.starmap(worker_task, tasks)

    return result

# Go through all possible solutions of single line. Find cells, which are always "#" or "."
# write 100% sure cells to solution matrix line
def possibilities_overlap_for_line(matrix_line: np.ndarray, single_line_possibilities: np.ndarray):
    for col_index_in_possibilities in range(len(matrix_line)):
        # check, if specific element in all possibilities is the same as the element in first possibility
        all_same = np.all(single_line_possibilities[:,col_index_in_possibilities] == single_line_possibilities[0,col_index_in_possibilities])
        if all_same:
            matrix_line[col_index_in_possibilities] = single_line_possibilities[0,col_index_in_possibilities]

# Go through all possible solutions of all rows and cols. Paint cells, which are always "#" or ".".
def possibilities_overlap(matrix: np.ndarray, all_rows_possibilities: List[np.ndarray], all_cols_possibilities: List[np.ndarray]):
    for row_index, single_row_possibilities in enumerate(all_rows_possibilities):
        possibilities_overlap_for_line(matrix[row_index,:], single_row_possibilities)
    for col_index, single_col_possibilities in enumerate(all_cols_possibilities):
        possibilities_overlap_for_line(matrix[:,col_index], single_col_possibilities)

# Is possible solution for line in conflict with partly solved matrix?
def is_line_obsolete(matrix_line: np.ndarray, line_possibility: np.ndarray) -> bool:
    for matrix_index_in_line, matrix_item in enumerate(matrix_line):
        if (matrix_item == "#" or matrix_item == ".") and matrix_item != line_possibility[matrix_index_in_line]:
            return True
    return False


# Takes all possibilities for single line. Check, if some of them are in conflict with partly solved matrix and
# deletes them from list of all possibilities.
def delete_obsolete_possibilities_for_line(matrix_line: np.ndarray, single_line_possibilities: np.ndarray) -> np.ndarray:
    indexes_of_rows_to_delete = []
    for row_index, row in enumerate(single_line_possibilities):
        if is_line_obsolete(matrix_line, np.array(row)):
            indexes_of_rows_to_delete.append(row_index)
    result = np.delete(single_line_possibilities, indexes_of_rows_to_delete, axis=0)
    return result

# delete possibilities of all lines (all rows or all cols), which are already in conflict with partly solved matrix. Return the rest.
def delete_obsolete_possibilities_for_all_lines(matrix: np.ndarray, all_lines_possibilities: List[np.ndarray], is_row: bool) -> List[np.ndarray]:
    result = []
    for line_index, single_line_possibilities in enumerate(all_lines_possibilities):
        if is_row:
            result.append(delete_obsolete_possibilities_for_line(matrix[line_index, :], single_line_possibilities))
        else:
            result.append(delete_obsolete_possibilities_for_line(matrix[:, line_index], single_line_possibilities))
    return result