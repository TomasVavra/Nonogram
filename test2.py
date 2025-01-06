from multiprocessing import Pool, cpu_count
import numpy as np


def f(x):
    return x+10

worker

if __name__ == '__main__':
    a = np.array([1, 2, 3, 4])
    b = np.array([1, 2, 3, 4])
    c = np.array([[1, 2], [3, 4], [5, 6]])




    with Pool(processes=num_cores) as pool:
        resultc = pool.starmap(worker, tasks)

    resultb = []
    for item in b:
        resultb.append(f(item))


    print("a ", a)
    print("resulta", resulta)
    print("b ", b)
    print("resultb", resultb)