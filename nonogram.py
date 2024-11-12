import re
from typing import List

def find_number_of_rows() -> int:
    with open("instruction.txt","r") as file:
        for line in file:
            if "rows" in line:
                result = int(re.search(r'\d+', line)[0])
    return result

def find_number_of_columns() -> int:
    with open("instruction.txt", "r") as file:
        for line in file:
            if "columns" in line:
                result = int(re.search(r'\d+', line)[0])
    return result

def find_raw_instruction_rows(l_number_of_rows: int):
    with open("instruction.txt", "r") as file:
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

def find_raw_instruction_columns(l_number_of_columns: int) -> List[str]:
    with open("instruction.txt", "r") as file:
        result = []
        counter = 0
        start_counter = False
        for line in file:
            if "columns" in line:
                start_counter = True
            if start_counter:
                if 0 < counter <= l_number_of_columns:
                    result.append(line.strip())
                counter += 1
    return result

def convert_raw_instruction_to_2d_array(l_raw_instruction: List[str]) -> List[List[int]]:     #from list of strings to list of arrays
    result = []
    for line in l_raw_instruction:
        #print(type(line))
        result.append(re.findall(r'\d+', line))
    return result

def make_sum_row(l_number_of_rows: int, l_rows_instruction: List[List[int]]) -> List[int]:
    result = [0 for row in range(l_number_of_rows)]
    for index, row in enumerate(l_rows_instruction):
        numbers = 0
        for item in row:
            result [index] += int(item)
            numbers += 1                 #at least 1 space between ech numbers
        result[index] += numbers - 1     #numbers -1 = spaces
    return result

def make_sum_column(l_number_of_columns: int, l_columns_instruction: List[List[int]]) -> List[int]:
    result = [0 for column in range(l_number_of_columns)]
    for index, column in enumerate(l_columns_instruction):
        numbers = 0
        for item in column:
            result [index] += int(item)
            numbers += 1                 #at least 1 space between ech numbers
        result[index] += numbers - 1     #numbers -1 = spaces
    return result

number_of_rows = find_number_of_rows()
number_of_columns = find_number_of_columns()
rows_raw_instruction = find_raw_instruction_rows(number_of_rows)
columns_raw_instruction = find_raw_instruction_columns(number_of_rows)
rows_instruction = convert_raw_instruction_to_2d_array(rows_raw_instruction)
columns_instruction = convert_raw_instruction_to_2d_array(columns_raw_instruction)
sum_row = make_sum_row(number_of_rows,rows_instruction)
sum_column = make_sum_column(number_of_columns,columns_instruction)
print(sum_row)
print(sum_column)
print()

matrix = [[row for row in range(number_of_rows)] for column in range(number_of_columns)]

#overlap
for row_index, row in enumerate(rows_instruction):
    for item in row:
        overlap = int(item) - number_of_rows + sum_row[int(row_index)]
        if overlap > 0:
            for matrix_item in matrix[row_index]:
                matrix_item = "#"
                print(matrix_item, end=" ")
            print()


# for row in matrix:
#   print(row)