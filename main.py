from helpers import *

if __name__ == "__main__":
    # not optimized for large input, as "instruction4.txt"
    input_file = "instruction2.txt"

    dimension = find_dimensions(input_file)
    number_of_rows = dimension[0]
    number_of_cols = dimension[1]

    rows_instruction = find_instructions_row(input_file, number_of_rows)
    cols_instruction = find_instructions_col(input_file, number_of_cols)

    is_instruction_valid(rows_instruction, cols_instruction)

    matrix = np.array([[col for col in range(number_of_cols)] for row in range(number_of_rows)], dtype=object)
    previous_matrix = np.array([[0 for col in range(number_of_cols)] for row in range(number_of_rows)], dtype=object)

    paint_overlap(matrix, rows_instruction, cols_instruction)

    print()
    print_matrix_debug(matrix)
    print()

    #create possibilities
    rows_possibilities = create_all_possibilities_for_all_lines(matrix,rows_instruction, is_row = True)
    cols_possibilities = create_all_possibilities_for_all_lines(matrix,cols_instruction, is_row = False)

    #update possibilities and matrix till matrix is changing
    while not np.array_equal(previous_matrix, matrix):
        previous_matrix = np.copy(matrix)
        possibilities_overlap(matrix, rows_possibilities, cols_possibilities)
        rows_possibilities = delete_obsolete_possibilities_for_all_lines(matrix, rows_possibilities, is_row = True)
        cols_possibilities = delete_obsolete_possibilities_for_all_lines(matrix, cols_possibilities, is_row = False)

    print()
    print_matrix_debug(matrix)
    print()

    print()
    print_picture(matrix)
    print()
    is_solution_valid(matrix, rows_instruction, cols_instruction)
