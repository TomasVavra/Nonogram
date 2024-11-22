
def distribute_dots(extra_spaces, positions):
    def helper(result, spaces_left, current_position):

        if spaces_left == 0:
            print(result)
            return
        if current_position >= positions:
            return
        for i in range(spaces_left + 1):
            result[current_position] = i
            helper(result, spaces_left - i, current_position + 1)
            result[current_position] = 0  # Reset for the next iteration

    result = []
    result = [0] * positions
    helper(result, extra_spaces, 0)


# Example usage
extra_spaces = 4
positions = 6
combinations = distribute_dots(extra_spaces, positions)



