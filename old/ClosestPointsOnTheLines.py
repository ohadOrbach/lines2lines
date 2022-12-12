from calc import *
from plot import *


def main():
    Q1 = np.array([[0, 0, 0], [1, 2, 1]], dtype=np.float64)
    Q2 = np.array([[0, 0, 0], [3, 4, 5]], dtype=np.float64)
    Q3 = np.array([[0, 0, 0], [0, 3, 3]], dtype=np.float64)

    axis = [1, 2, 1]
    theta = math.radians(5)
    R = rotation_matrix(axis, theta)
    t = np.array([5, -4, 2], dtype=np.float64)
    new_origin = np.array([10, 0, 5], dtype=np.float64)
    origin = np.array([new_origin, new_origin, new_origin])
    sec_point = np.array([Q1[1] * 2, Q2[1] * 2, Q3[1] * 2])
    L1, L2, L3 = add_noise(R_T_On_Lines(R, t, origin, sec_point))
    Q1 = normline(Q1)
    Q2 = normline(Q2)
    Q3 = normline(Q3)

    L1 = normline(L1)
    L2 = normline(L2)
    L3 = normline(L3)
    A = np.zeros([3, 3])
    B = np.zeros([3, 3])
    for i in range(10):
        A[0], B[0] = closest_point(Q1[0], Q1[1], L1[0], L1[1])
        A[1], B[1] = closest_point(Q2[0], Q2[1], L2[0], L2[1])
        A[2], B[2] = closest_point(Q3[0], Q3[1], L3[0], L3[1])
        dist = sum(math.dist(A[i], B[i]) for i in range(len(A)))
        plot3d(np.array([Q1, Q2, Q3]), np.array([L1, L2, L3]), A, B)
        T2, R2, t2 = best_fit_transform(B, A)
        R2 = np.around(R2, decimals=2)
        t2 = np.around(t2, decimals=2)
        print("\nsum of distances is :\n", dist)

        L = R_T_On_Lines(R2, t2, np.array([L1[0], L2[0], L3[0]]), B)
        L1, L2, L3 = L
        L1 = normline(L1)
        L2 = normline(L2)
        L3 = normline(L3)


if __name__ == '__main__':
    main()
