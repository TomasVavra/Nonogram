import re
print("hello","\n")

def find_number_of_rows():
    with open("instruction.txt","r") as file:
        for line in file:
            if "rows" in line:
                rows = int(re.search(r'\d+', line)[0])
    return rows

def find_number_of_columns():
    with open("instruction.txt", "r") as file:
        for line in file:
            if "columns" in line:
                columns = int(re.search(r'\d+', line)[0])
    return columns

def find_raw_instruction_rows(number_of_rows):
    with open("instruction.txt", "r") as file:
        rows_instruction = []
        counter = 0
        start_counter = False
        for line in file:
            if "rows" in line:
                start_counter = True
            if start_counter:
                if 0 < counter <= number_of_rows:
                    rows_instruction.append(line.strip())
                counter += 1
    return rows_instruction

def find_raw_instruction_columns(number_of_columns):
    with open("instruction.txt", "r") as file:
        columns_instruction = []
        counter = 0
        start_counter = False
        for line in file:
            if "columns" in line:
                start_counter = True
            if start_counter:
                if 0 < counter <= number_of_columns:
                    columns_instruction.append(line.strip())
                counter += 1
    return columns_instruction

def convert_raw_instruction_to_2d_array(raw_instruction):
    array_2d = []
    for line in raw_instruction:
        #print(type(line))
        array_2d.append(re.findall(r'\d+', line))
        #print(type(re.findall(r'\d+', line)))
    return array_2d


number_of_rows = find_number_of_rows()
number_of_columns = find_number_of_columns()
rows_raw_instruction = find_raw_instruction_rows(number_of_rows)
columns_raw_instruction = find_raw_instruction_columns(number_of_rows)
rows_instruction = convert_raw_instruction_to_2d_array(rows_raw_instruction)
columns_instruction = convert_raw_instruction_to_2d_array(columns_raw_instruction)

print(number_of_rows)
print(number_of_columns)
print(rows_instruction)
print(columns_instruction)