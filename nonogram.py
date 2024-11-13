import re
from typing import List     #for Function Annotations in python 3.8, not

input_file = "instruction.txt"

def find_number_of_rows() -> int:
    with open(input_file,"r") as file:
        for line in file:
            if "rows" in line:
                result = int(re.search(r'\d+', line)[0])
    return result

def find_number_of_cols() -> int:
    with open(input_file, "r") as file:
        for line in file:
            if "columns" in line:
                result = int(re.search(r'\d+', line)[0])
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

#sum of numbers in each row or column + number of spaces
def make_sum_row_or_col(l_number_of_rows_or_cols: int, l_rows_or_cols_instruction: List[List[int]]) -> List[int]:
    result = [0 for row in range(l_number_of_rows_or_cols)]
    for index, row in enumerate(l_rows_or_cols_instruction):
        numbers = 0
        for item in row:
            result [index] += int(item)
            numbers += 1                 #at least 1 space between ech numbers
        result[index] += numbers - 1     #numbers -1 = spaces
    return result

# number_of_cols for rows_instruction to iterate through items in 1 row
def paint_overlap (l_matrix: List[List[int]], l_number_of_rows_or_cols: int, l_rows_or_cols_instruction: List[List[int]], sum_row_or_col: List[int], is_row: bool) -> None:
    for row_or_col_index, row_or_col in enumerate(l_rows_or_cols_instruction):
        offset = 0
        for item_in_instruction in row_or_col:
            overlap = int(item_in_instruction) + sum_row_or_col[int(row_or_col_index)] - l_number_of_rows_or_cols
            if overlap > 0:
                counter = 0                 #is finished
                for i in range(offset + int(item_in_instruction) - overlap, offset + int(item_in_instruction)):     #paint overlap in row
                    if is_row:
                        l_matrix[row_or_col_index][i] = "#"
                        counter += 1
                    else:
                        l_matrix[i][row_or_col_index] = "#"
                        counter += 1
                if counter == int(item_in_instruction) and i+1 < l_number_of_rows_or_cols:  #is finished
                    l_matrix[row_or_col_index][i + 1] = "."                                 #is finished
            offset += int(item_in_instruction) + 1

#předělat, pokud je pocet skupinek = počet čisel v zadani, můžu vyškrtávat
def is_finished (l_matrix: List[List[int]], l_number_of_rows_or_cols: int, l_rows_or_cols_instruction: List[List[int]], is_row: bool) -> None:
    for row_or_col_index, row_or_col in enumerate(l_rows_or_cols_instruction):
        for item_in_instruction in row_or_col:
            counter = 0
            for i in range(l_number_of_rows_or_cols):
                if is_row:
                    counter = counter + 1 if l_matrix[row_or_col_index][i] == "#" else 0
                    if counter == int(item_in_instruction) and i+1 < l_number_of_rows_or_cols:
                        l_matrix[row_or_col_index][i+1] = "."
                        print("x")
                else:
                    counter +=1 if l_matrix[i][row_or_col_index] == "#" else 0
                    if counter == item_in_instruction and i+1 < l_number_of_rows_or_cols:
                        l_matrix[i+1][row_or_col_index] = "."



number_of_rows = find_number_of_rows()
number_of_cols = find_number_of_cols()
rows_raw_instruction = find_raw_instruction_rows(number_of_rows)
cols_raw_instruction = find_raw_instruction_cols(number_of_rows)
rows_instruction = convert_raw_instruction_to_2d_array(rows_raw_instruction)
cols_instruction = convert_raw_instruction_to_2d_array(cols_raw_instruction)
sum_row = make_sum_row_or_col(number_of_rows, rows_instruction)
sum_col = make_sum_row_or_col(number_of_cols, cols_instruction)
print(sum_row)
print(sum_col)
print()

matrix = [[col for col in range(number_of_cols)] for row in range(number_of_rows)]
paint_overlap(matrix, number_of_cols, rows_instruction, sum_row, is_row = True)     # number_of_cols to iterate through item in 1 row
#is_finished(matrix, number_of_rows, rows_instruction, is_row = True)


paint_overlap(matrix, number_of_rows, cols_instruction, sum_col, is_row = False)






for idx, row in enumerate(matrix):
    print(idx, " ",end="")
    if idx < 10:
        print(" ",end="")
    print("| ",end="")
    for item in row:
        print(item," ",end="")
        if type(item) != int or item < 10:
            print(" ",end="")
    print("|")

# for idx, row in enumerate(matrix):
#     print(idx,end="")
#     for item in row:
#         if type(item) == int:
#             print(" ",item," ",end="")
#         else:
#             print(item,end="")

#     print(idx, row)
# print()
# print(matrix[2][0])