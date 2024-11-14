import re
from typing import List     #for Function Annotations in python 3.8, not

input_file = "instruction2.txt"

def find_dimensions() -> List[int]:
    with open(input_file,"r") as file:
        result = [0 for x in range(2)]
        for line in file:
            if "rows" in line:
                result [0] = int(re.search(r'\d+', line)[0])
            if "columns" in line:
                result  [1]= int(re.search(r'\d+', line)[0])
    return result

def find_raw_instruction_rows(l_number_of_rows: int):
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
        #print(type(line))
        result.append(re.findall(r'\d+', line))
    return result

def find_row_instruction():
    l_dimension = find_dimensions()
    rows_raw_instruction = find_raw_instruction_rows(l_dimension[0])
    result = convert_raw_instruction_to_2d_array(rows_raw_instruction)
    return result

def find_col_instruction():
    l_dimension = find_dimensions()
    cols_raw_instruction = find_raw_instruction_cols(l_dimension[1])
    result = convert_raw_instruction_to_2d_array(cols_raw_instruction)
    return result


#sum of the numbers in each row or column + number of spaces
def make_sum_row_or_col(l_rows_or_cols_instruction: List[List[int]]) -> List[int]:
    #result = [0 for row in range(l_number_of_rows_or_cols)]
    result = []
    for row_or_col in l_rows_or_cols_instruction:
        sum = 0
        for item in row_or_col:
            sum += int(item) +1
        result.append(sum-1)     #numbers -1 = spaces
    return result

def print_matrix(l_matrix):     # in nice way with col and row indexes
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

def paint_overlap_in_line(l_matrix_row_or_col: List[int]):
    pass

# number_of_cols for rows_instruction to iterate through items in 1 row
def paint_overlap (l_matrix: List[List[int]], l_number_of_cols_or_rows: int, l_rows_or_cols_instruction: List[List[int]], sum_row_or_col: List[int], is_row: bool) -> None:
    for row_or_col_index, row_or_col in enumerate(l_rows_or_cols_instruction):
        offset = 0
        for item_in_instruction in row_or_col:
            overlap = int(item_in_instruction) + sum_row_or_col[int(row_or_col_index)] - l_number_of_cols_or_rows
            if overlap > 0:
                for i in range(offset + int(item_in_instruction) - overlap, offset + int(item_in_instruction)):     #paint overlap in row
                    if is_row:
                        l_matrix[row_or_col_index][i] = "#"
                    else:
                        l_matrix[i][row_or_col_index] = "#"
            offset += int(item_in_instruction) + 1

def count_packs_of_hashes_in_line(l_matrix_row_or_col: List[int]) -> int:
    result = 0
    hash_counter = 0
    for item in l_matrix_row_or_col:
        hash_counter = hash_counter + 1 if item == "#" else 0
        if hash_counter == 1:
            result += 1
    return result

#předělat, pokud pocet skupinek = počet čisel v zadani, můžu vyškrtávat
def is_finished (l_matrix: List[List[int]], l_number_of_cols_or_rows: int, l_rows_or_cols_instruction: List[List[int]], is_row: bool) -> None:
    for row_or_col_index, row_or_col in enumerate(l_rows_or_cols_instruction):
        for item_in_instruction in row_or_col:
            hash_counter = 0
            for i in range(l_number_of_cols_or_rows):
                if is_row:
                    hash_counter = hash_counter + 1 if l_matrix[row_or_col_index][i] == "#" else 0
                    if hash_counter == 1:
                        pass


            if pack_counter == len(row_or_col):
                for i in range(l_number_of_cols_or_rows):
                    if is_row:
                        hash_counter = hash_counter + 1 if l_matrix[row_or_col_index][i] == "#" else 0
                        if hash_counter == int(item_in_instruction) and i+1 < l_number_of_cols_or_rows:
                            l_matrix[row_or_col_index][i+1] = "."
                            # print("x")
                # else:
                #     hash_counter +=1 if l_matrix[i][row_or_col_index] == "#" else 0
                #     pass# if hash_counter == item_in_instruction and i+1 < l_number_of_cols_or_rows:
                #     #     l_matrix[i+1][row_or_col_index] = "."


dimension = find_dimensions()
number_of_rows = dimension[0]
number_of_cols = dimension[1]
print(number_of_rows,number_of_cols)

rows_instruction = find_row_instruction()
cols_instruction = find_col_instruction()

sum_row = make_sum_row_or_col(rows_instruction)
sum_col = make_sum_row_or_col(cols_instruction)
print(sum_row)
print(sum_col)
print()

matrix = [[col for col in range(number_of_cols)] for row in range(number_of_rows)]
paint_overlap(matrix, number_of_cols, rows_instruction, sum_row, is_row = True)     # number_of_cols to iterate through item in 1 row

print(matrix[7])
packs = count_packs_of_hashes_in_line(matrix[7])
print(packs)

column = [row[5] for row in matrix]
print(column)
packs = count_packs_of_hashes_in_line(column)
print(packs)

#is_finished(matrix, number_of_cols, rows_instruction, is_row = True)

#paint_overlap(matrix, number_of_rows, cols_instruction, sum_col, is_row = False)
print()
print_matrix(matrix)

