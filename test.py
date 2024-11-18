import numpy as np

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



def get_line (l_matrix, index):
    result = []
    for row in matrix:
        result.append(row[index])
    return result

matrix = np.array([[col for col in range(4)] for row in range(6)])
print_matrix(matrix)
print()

line = matrix[:,1]
line *= 10

print_matrix(matrix)




