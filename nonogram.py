import re
import numpy as np
from typing import List     #for Function Annotations in python 3.8

input_file = "instruction.txt"

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
    print("      ", end="")
    for idx, item in enumerate(l_matrix[0]):
        print(idx, " ", end="")
        if idx < 10:
            print(" ", end="")
    print()
    print("      ", end="")
    [print("----", end="") for item in l_matrix[0]]
    print()
    for idx, row in enumerate(l_matrix):
        print(idx, " ",end="")
        if idx < 10:
            print(" ",end="")
        print("| ",end="")
        for item in row:
            print(item," ",end="")
            if type(item) != int or item < 10:
                print(" ",end="")
        print("|")

# line can be row or column
# not working for columns
def paint_overlap_in_line(l_matrix_line: List[int], l_instruction_line: List[int]) -> None:
    offset = 0
    for instruction_line_item in l_instruction_line:
        overlap = instruction_line_item + sum(l_instruction_line) + len(l_instruction_line) - 1 - len(l_matrix_line)     #spaces = numbers in instruction(len()) -1
        if overlap > 0:
            for i in range(offset + instruction_line_item - overlap, offset + instruction_line_item):  # paint overlap in row
                l_matrix_line[i] = "#"
        offset += instruction_line_item + 1

# number_of_cols for rows_instruction to iterate through items in 1 row
def paint_overlap (l_matrix: List[List[int]], l_rows_or_cols_instruction: List[List[int]], is_row: bool) -> None:
    for row_or_col_index, row_or_col in enumerate(l_rows_or_cols_instruction):
        #l_matrix_line = get_row(l_matrix, row_or_col_index) if is_row else get_col(l_matrix, row_or_col_index)
        l_matrix_line = l_matrix[row_or_col_index,:]  if is_row else l_matrix[:,row_or_col_index]
        paint_overlap_in_line(l_matrix_line, l_rows_or_cols_instruction[row_or_col_index])

def count_packs_of_hashes_in_line(l_matrix_line: List[int]) -> int:
    result = 0
    hash_counter = 0
    for item in l_matrix_line:
        hash_counter = hash_counter + 1 if item == "#" else 0
        if hash_counter == 1:
            result += 1
    return result

# test line fails, for completely solved line works well
def is_line_finished(l_matrix_line: List[int], l_instruction_line: List[int]) -> None:
    l_packs = count_packs_of_hashes_in_line(l_matrix_line)
    if l_packs == len(l_instruction_line):
        offset = 0
        for instruction_line_item in l_instruction_line:
            hash_counter = 0
            for i in range(offset, len(l_matrix_line)):
                hash_counter = hash_counter + 1 if l_matrix_line[i] == "#" else 0
                if hash_counter == instruction_line_item and i+1 < len(l_matrix_line):
                    l_matrix_line[i+1] = "."
                    print("xxxxxx")
                    break  # exit the loop once the dot is placed
            offset += instruction_line_item + 1


#předělat, pokud pocet skupinek = počet čisel v zadani, můžu vyškrtávat
def is_finished (l_matrix: List[List[int]], l_rows_or_cols_instruction: List[List[int]], is_row: bool) -> None:
    for row_or_col_index, row_or_col in enumerate(l_rows_or_cols_instruction):
        l_matrix_line = l_matrix[row_or_col_index,:]  if is_row else l_matrix[:,row_or_col_index]
        is_line_finished(l_matrix_line, l_rows_or_cols_instruction[row_or_col_index])


dimension = find_dimensions()
number_of_rows = dimension[0]
number_of_cols = dimension[1]
print(number_of_rows,number_of_cols)
print()
rows_instruction = find_row_instruction()
cols_instruction = find_col_instruction()
print(cols_instruction)
matrix = np.array([[col for col in range(number_of_cols)] for row in range(number_of_rows)], dtype=object)

paint_overlap(matrix, rows_instruction, is_row = True)
paint_overlap(matrix, cols_instruction, is_row = False)


print_matrix(matrix)
print()


# test_row = ['#', '0', '#', '#', '0', '#', '0', 0, '#', '#', '0', '#', '#', 0, '#']
# test_row_instruction = [1,2,1,3,2,1]
# is_line_finished(test_row, test_row_instruction)
# print(test_row)








