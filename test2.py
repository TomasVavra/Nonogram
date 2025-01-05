from multiprocessing import Pool, cpu_count
import numpy as np


def f(x):
    return x*x

if __name__ == '__main__':
    a = np.array([1,2,3,4])
    print(a,"\n")

    num_cores = cpu_count()
    with Pool(processes=num_cores) as pool:
        result = pool.map(f, a)
    print(num_cores)
    print(a)
    print(result)
    print()