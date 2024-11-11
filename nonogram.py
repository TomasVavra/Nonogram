import re
print("hello","\n")

def find_number_of_rows_columns():
    with open("instruction.txt","r") as file:
        for line in file:
            if "rows" in line:
                number_of_rows = int(re.search(r'\d+', line)[0])
            if "columns" in line:
                number_of_columns = int(re.search(r'\d+', line)[0])
    return [number_of_rows,number_of_columns]

number_of_rows = find_number_of_rows_columns()[0]
number_of_columns = find_number_of_rows_columns()[1]


print(type(number_of_rows))
print(number_of_rows)
print(type(number_of_columns))
print(number_of_columns)


