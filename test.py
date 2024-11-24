import itertools


def generate_dot_distributions(spaces: int, positions: int):
    # Generate all combinations with repetition
    combinations = list(itertools.combinations_with_replacement(range(dots), positions))

    # Filter out valid distributions where sum of positions equals number of spaces
    valid_combinations = []
    for combo in combinations:
        # Count the number of dots in each position
        position_count = [0] * positions
        for pos in combo:
            position_count[pos] += 1
        if sum(position_count) == dots:
            valid_combinations.append(position_count)

    return valid_combinations


# Example usage
dots = 4
positions = 6
combinations = generate_dot_distributions(dots, positions)

# Print all valid combinations
for combo in combinations:
    print(combo)
