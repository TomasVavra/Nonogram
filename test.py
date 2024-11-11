with open("instruction.txt", "r") as file:
    columns_instruction = []
    counter = 0
    number_of_columns = 15
    start_counter = False
    for line in file:
        if "columns" in line:
            start_counter = True
        if start_counter:
            if counter>0 and counter <= number_of_columns:
                columns_instruction.append(line.strip())
            counter +=1
print(columns_instruction)
