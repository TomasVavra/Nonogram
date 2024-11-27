import itertools


extra_spaces = 20
positions = 8
variations_with_replacement = list(itertools.product(range(extra_spaces +1), repeat=positions))
count = 0       # for debugging, number of all variations
for spaces_positions in variations_with_replacement:
    l_sum = 0
    for number in spaces_positions:
        l_sum += number
    if l_sum == extra_spaces:
        count += 1

print(count)