import numpy as np

def factorial(n):
    if n == 1 or n == 0:
        return 1
    return n*factorial(n-1)

print(factorial(5))


def distribute_dots(dots, positions):
    def helper(dots_left, current_distribution, current_position):
        if dots_left == 0:
            distributions.append(current_distribution[:])
            return
        if current_position >= positions:
            return

        for i in range(dots_left + 1):
            current_distribution[current_position] = i
            helper(dots_left - i, current_distribution, current_position + 1)
            current_distribution[current_position] = 0  # Reset for the next iteration

    distributions = []
    initial_distribution = [0] * positions
    helper(dots, initial_distribution, 0)
    return distributions


# Example usage
dots = 4
positions = 6
combinations = distribute_dots(dots, positions)

# Print all valid combinations
for combo in combinations:
    print(combo)

