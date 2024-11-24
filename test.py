import itertools

variations_with_replacement = list(itertools.product(range(5), repeat=6))

count = 0
for line in variations_with_replacement:
    sum = 0
    for number in line:
        sum += number
    if sum == 4:
        print(line)
        count += 1

print()
print(count)
