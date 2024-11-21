import numpy as np

original_array = np.array([10, 20, 30, 40, 50])
print(original_array)
copied_array = np.copy(original_array)
new_arr = np.insert(copied_array, 2, 25)
print(original_array)
print(copied_array)
print(new_arr)

# def fce(number):
#     number = 5
# def gce(ar):
#     ar[0] = 9
# x= 7
# fce(x)
# print(x)
#
# arr = [0,0]
# gce(arr)
# print(arr)