import numpy as np

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


matrix = [[col for col in range(10)] for row in range(15)]
print(matrix[:][0])

print_matrix(matrix)