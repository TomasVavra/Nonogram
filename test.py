import re
import numpy as np
import itertools            # for combinatorics
from typing import List     # for Function Annotations in python 3.8

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

number_of_rows = 10
number_of_cols = 15
matrix = np.array([[col for col in range(number_of_cols)] for row in range(number_of_rows)], dtype=object)
for index, item in enumerate(matrix[4,:]):
    matrix[4,index] = 20

print_matrix(matrix)
matrix = np.delete(matrix,4, axis =0)

print()
print_matrix(matrix)