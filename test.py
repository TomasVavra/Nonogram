import numpy as np
from multiprocessing import Pool
from typing import List

def create_all_possibilities_for_line(line: np.ndarray, instruction: List[int]) -> np.ndarray:
    # Placeholder for your existing line processing function
    return np.array([])

def worker_task(l_matrix: np.ndarray, instruction_line: List[int], line_index: int, is_row: bool) -> np.ndarray:
    if is_row:
        result = create_all_possibilities_for_line(l_matrix[line_index, :], instruction_line)
        print("row ", line_index)
    else:
        result = create_all_possibilities_for_line(l_matrix[:, line_index], instruction_line)
        print("col ", line_index)
    return result

def create_all_possibilities_for_all_lines(l_matrix: np.ndarray, l_rows_or_cols_instruction: List[List[int]], is_row: bool) -> List[np.ndarray]:
    num_cores = multiprocessing.cpu_count()
    with Pool(processes=num_cores) as pool:
        tasks = [(l_matrix, instruction_line, line_index, is_row) for line_index, instruction_line in enumerate(l_rows_or_cols_instruction)]
        result = pool.starmap(worker_task, tasks)
    return result

# Example usage
l_matrix = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
l_rows_or_cols_instruction = [[1], [1], [1]]
is_row = True

result = create_all_possibilities_for_all_lines(l_matrix, l_rows_or_cols_instruction, is_row)
print(result)
