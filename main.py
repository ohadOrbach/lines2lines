from Set import *
from calc import *


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

    Set1.closest_points_set(Set2)
    dist = Set1.distance(Set2)
    Set1.plot3d(Set2, title="sum of distances " + str(dist) + "\nwithout rotation")

    axis = [1, 2, 1]
    theta = math.radians(5)
    R = rotation_matrix(axis, theta)
    t = np.array([5, -4, 2], dtype=np.float64)

    Set2.R_t_Set(R, t)
    Set2.noise()

    for i in range(5):
        Set1.closest_points_set(Set2)
        dist = Set1.distance(Set2)
        Set1.plot3d(Set2, title="sum of distances " + str(dist))
        _, R, t = Set2.best_fit_transform(Set1)
        R = np.around(R, decimals=2)
        t = np.around(t, decimals=2)
        Set2.R_t_Set(R, t)


if __name__ == '__main__':
    main()
