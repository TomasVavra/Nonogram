list = [1,2,3]
list_of_list = []
list_of_list2 = []

list_of_list.append(list)
list_of_list.append(list)

list_of_list2.append(list[:])
list_of_list2.append(list[:])

print(list)
print(list_of_list)
print(list_of_list2)

list[0] = 0

print(list)
print(list_of_list)
print(list_of_list2)