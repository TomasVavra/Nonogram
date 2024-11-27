def generate_combinations(l_spaces, l_positions):
    def helper(spaces_left, current_combination, current_position):
        if spaces_left == 0:
            l_combinations.append(current_combination[:])
            return
        if current_position >= positions:
            return

        for i in range(spaces_left + 1):
            current_combination[current_position] = i
            helper(spaces_left - i, current_combination, current_position + 1)
            current_combination[current_position] = 0  # Reset for the next iteration

    l_combinations = []
    initial_combination = [0] * positions
    helper(spaces, initial_combination, 0)
    return l_combinations


# Example usage
spaces = 20
positions = 8
combinations = generate_combinations(spaces, positions)

# Print all valid combinations
for combo in combinations:
    print(type(combo))

print(combinations[0])
print(type(combinations[0]))
print(type(combinations))


