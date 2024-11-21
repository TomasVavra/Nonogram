import re
import numpy as np
from typing import List     #for Function Annotations in python 3.8

input_file = "instruction3.txt"

def find_dimensions() -> List[int]:
    with open(input_file,"r") as file:
        result = [0 for x in range(2)]
        for l_line in file:
            if "rows" in l_line:
                result [0] = int(re.search(r'\d+', l_line)[0])
            if "columns" in l_line:
                result  [1]= int(re.search(r'\d+', l_line)[0])
    return result

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

def convert_raw_instruction_to_2d_array(l_raw_instruction: List[str]) -> List[List[int]]:     #from list of strings to list of arrays
    result = []
    for line in l_raw_instruction:
        result.append(re.findall(r'\d+', line))     #find numbers, but it is List[List[str]
    for i, row in enumerate(result):                       #convert them to int
        for j, item in enumerate(row):
            result[i][j] = int(item)
    return result

def find_row_instruction() -> List[List[int]]:
    l_dimension = find_dimensions()
    rows_raw_instruction = find_raw_instruction_rows(l_dimension[0])
    result = convert_raw_instruction_to_2d_array(rows_raw_instruction)
    return result

def find_col_instruction() -> List[List[int]]:
    l_dimension = find_dimensions()
    cols_raw_instruction = find_raw_instruction_cols(l_dimension[1])
    result = convert_raw_instruction_to_2d_array(cols_raw_instruction)
    return result

# in nice way with col and row indexes
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

# line can be row or column
def paint_overlap_in_line(l_matrix_line: np.ndarray, l_instruction_line: List[int]) -> None:
    offset = 0
    for instruction_line_item in l_instruction_line:
        overlap = instruction_line_item + sum(l_instruction_line) + len(l_instruction_line) - 1 - len(l_matrix_line)     #spaces = numbers in instruction(len()) -1
        if overlap > 0:
            for i in range(offset + instruction_line_item - overlap, offset + instruction_line_item):  # paint overlap in row
                l_matrix_line[i] = "#"
        offset += instruction_line_item + 1

def paint_overlap (l_matrix: np.ndarray, l_rows_or_cols_instruction: List[List[int]], is_row: bool) -> None:
    for row_or_col_index, row_or_col in enumerate(l_rows_or_cols_instruction):
        l_matrix_line = l_matrix[row_or_col_index,:]  if is_row else l_matrix[:,row_or_col_index]
        paint_overlap_in_line(l_matrix_line, l_rows_or_cols_instruction[row_or_col_index])

def check_solution_in_line(l_matrix_line: np.ndarray, l_instruction_line: List[int]) -> bool:
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

def check_solution(l_matrix: np.ndarray, l_rows_instruction: List[List[int]], l_cols_instruction: List[List[int]]) -> bool:
    for row_index, row in enumerate(l_rows_instruction):
        l_matrix_line = l_matrix[row_index,:]
        if not check_solution_in_line(l_matrix_line, l_rows_instruction[row_index]):
            return False
    for col_index, row in enumerate(l_cols_instruction):
        l_matrix_line = l_matrix[:,col_index]
        if not check_solution_in_line(l_matrix_line, l_cols_instruction[col_index]):
            return False
    return True

def extra_spaces_to_position_in_line(l_matrix_line: np.ndarray, l_instruction_line: List[int], extra_spaces: int, position: int) -> np.ndarray:
    result = np.array([col for col in range(len(l_matrix_line))], dtype=object)
    matrix_line_index = 0
    for instruction_line_index, instruction_line_item in enumerate(l_instruction_line):
        if instruction_line_index == position:      # extra spaces in front of instruction
            for i in range(matrix_line_index, matrix_line_index + extra_spaces):
                result[i] = "."
                matrix_line_index += 1
        for i in range(matrix_line_index, matrix_line_index + instruction_line_item):   #fill instruction
            result[i] = "#"
            matrix_line_index += 1
        if instruction_line_index < len(l_instruction_line) - 1:    #no space behind last instruction
            result[matrix_line_index] = "."                         #space behind every instruction
            matrix_line_index += 1
        if position == len(l_instruction_line) and instruction_line_index +1 == len(l_instruction_line):    #extra spaces behind last instruction if last position
            for i in range(matrix_line_index, matrix_line_index + extra_spaces):
                result[i] = "."
    return result

def add_space(l_matrix_line: np.ndarray, position: int):
    result = np.copy(l_matrix_line)
    number_of_first_dots = 0
    first_dot = True    #is it first dot after #?
    for index, item in enumerate(l_matrix_line):
        if position == number_of_first_dots or type(item) == int:
            result = np.insert(l_matrix_line,index,".")
            break  # extra space is placed, I don't want second one
        if item == "#":
            first_dot = True
        if item == "." and first_dot:
            number_of_first_dots += 1
            first_dot = False
    # error handling
    if result[-1] == "#" or result[-1] == ".":
        raise ValueError("The extra element is . or # ")
    # copy result to original line
    for index, item in enumerate(l_matrix_line):    #excess elements are not copied
        l_matrix_line[index] = result[index]



def all_solutions_for_line(l_matrix_line: np.ndarray, l_instruction_line: List[int]) -> np.ndarray:
    result = np.array([col for col in range(len(l_matrix_line))], dtype=object)
    extra_spaces = len(l_matrix_line) - (sum(l_instruction_line) + len(l_instruction_line) - 1)

    for position in range(len(l_instruction_line)+1):
        for spaces in range(extra_spaces+1):
            result = extra_spaces_to_position_in_line(l_matrix_line, l_instruction_line, spaces, position)
        print(result)


# def count_packs_of_hashes_in_line(l_matrix_line: np.ndarray) -> int:
#     result = 0
#     hash_counter = 0
#     for item in l_matrix_line:
#         hash_counter = hash_counter + 1 if item == "#" else 0
#         if hash_counter == 1:
#             result += 1
#     return result
#
# # test line fails, for completely solved line works well
# def is_line_finished(l_matrix_line: np.ndarray, l_instruction_line: List[int]) -> None:
#     l_packs = count_packs_of_hashes_in_line(l_matrix_line)
#     if l_packs == len(l_instruction_line):
#         offset = 0
#         for instruction_line_item in l_instruction_line:
#             hash_counter = 0
#             for i in range(offset, len(l_matrix_line)):
#                 hash_counter = hash_counter + 1 if l_matrix_line[i] == "#" else 0
#                 if hash_counter == instruction_line_item and i+1 < len(l_matrix_line):
#                     l_matrix_line[i+1] = "."
#                     print("xxxxxx")
#                     break  # exit the loop once the dot is placed
#             offset += instruction_line_item + 1
#
# #předělat, pokud pocet skupinek = počet čisel v zadani, můžu vyškrtávat
# def is_finished (l_matrix: np.ndarray, l_rows_or_cols_instruction: List[List[int]], is_row: bool) -> None:
#     for row_or_col_index, row_or_col in enumerate(l_rows_or_cols_instruction):
#         l_matrix_line = l_matrix[row_or_col_index,:]  if is_row else l_matrix[:,row_or_col_index]
#         is_line_finished(l_matrix_line, l_rows_or_cols_instruction[row_or_col_index])

dimension = find_dimensions()
number_of_rows = dimension[0]
number_of_cols = dimension[1]
rows_instruction = find_row_instruction()
cols_instruction = find_col_instruction()

matrix = np.array([[col for col in range(number_of_cols)] for row in range(number_of_rows)], dtype=object)

paint_overlap(matrix, rows_instruction, is_row = True)
paint_overlap(matrix, cols_instruction, is_row = False)

print()
print_matrix(matrix)
print()

test_row = np.array(['#', '.', '#', '#', '.', '#', '.', "#", '#', '#', '.', '#', '#', ".", '#'])
test_row_instruction = [1,2,1,3,2,1]
print(check_solution_in_line(test_row,test_row_instruction))
print()

print(matrix[13,:])
print(rows_instruction[13])
line = extra_spaces_to_position_in_line(matrix[13,:],rows_instruction[13],2,2)
print(line)
add_space(line,5)
print(line)
add_space(line,0)

print(line)

#all_solutions_for_line(matrix[13,:],rows_instruction[13])

print()


# test_row = ['#', '0', '#', '#', '0', '#', '0', 0, '#', '#', '0', '#', '#', 0, '#']
# test_row_instruction = [1,2,1,3,2,1]
# is_line_finished(test_row, test_row_instruction)
# print(test_row)








