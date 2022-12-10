import numpy as np
from plot import *
from calc import *
from Line import *
from Set import *

def main():
    Q1 = LineR3(np.array([0, 0, 0], dtype=np.float64), np.array([1, 2, 1], dtype=np.float64))
    Q2 = LineR3(np.array([0, 0, 0], dtype=np.float64), np.array([3, 4, 5], dtype=np.float64))
    Q3 = LineR3(np.array([0, 0, 0], dtype=np.float64), np.array([0, 3, 3], dtype=np.float64))
    Set1 = SetOfLines(np.array([Q1, Q2, Q3]))
    print(Set1)
    L1 = LineR3(np.array([10, 0, 5], dtype=np.float64), np.array([2, 4, 2], dtype=np.float64))
    L2 = LineR3(np.array([10, 0, 5], dtype=np.float64), np.array([6, 8, 10], dtype=np.float64))
    L3 = LineR3(np.array([10, 0, 5], dtype=np.float64), np.array([0, 6, 6], dtype=np.float64))
    Set2 = SetOfLines(np.array([L1, L2, L3]))
    print(Set2)
    axis = [1, 2, 1]
    theta = math.radians(5)
    R = rotation_matrix(axis, theta)
    t = np.array([5, -4, 2], dtype=np.float64)

    L1.R_T_On_Line(R, t)
    L2.R_T_On_Line(R, t)
    L3.R_T_On_Line(R, t)

    L1.add_noise()
    L2.add_noise()
    L3.add_noise()

    A = np.zeros([3, 3])
    B = np.zeros([3, 3])

    for i in range(5):
        A[0], B[0] = Q1.closest_point(L1)
        A[1], B[1] = Q2.closest_point(L2)
        A[2], B[2] = Q3.closest_point(L3)
        dist = sum(math.dist(A[i], B[i]) for i in range(len(A)))
        Set1.polt3d(Set2,A,B)
        T2, R2, t2 = best_fit_transform(B, A)
        R2 = np.around(R2, decimals=2)
        t2 = np.around(t2, decimals=2)
        print("\nsum of distances is :\n", dist)

        L1.R_T_On_Line(R2, t2)
        L2.R_T_On_Line(R2, t2)
        L3.R_T_On_Line(R2, t2)

if __name__ == '__main__':
    main()

