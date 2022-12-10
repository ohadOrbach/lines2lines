import numpy as np
from plot import *
from calc import *
from plot import *

def checkLines():
    origin = np.array([1,1,1])
    sec_point = np.array([4, 4, 4])
    vector = np.array([origin, sec_point-origin])

    axis = [1, 0, 0]
    theta = math.radians(90)
    R = rotation_matrix(axis, theta)
    t = np.array([5, -4, 2], dtype=np.float64)
    new_origin = np.dot(R,origin)+t
    new_sec_point = np.dot(R,sec_point)+t
    new_vector = np.array([new_origin, new_sec_point-new_origin])
    plot3d(np.array([vector]), np.array([new_vector]), np.array([origin, sec_point]),np.array([new_origin, new_sec_point]))

def checlRT():
    A = np.random.randint(-5, 5, size = [3,3])
    B = np.zeros_like(A)
    axis = [1, 0, 1]
    theta = math.radians(90)
    R = rotation_matrix(axis, theta)
    t = np.array([10, 3, 1])
    R = np.around(R, decimals=2)
    t = np.around(t, decimals=2)
    print("\nRotation :\n", R, "\nTranslation :\n", t)
    for i in range(len(A)):
        B[i] = np.dot(R, A[i]) + t
    T2, R2, t2 = best_fit_transform(A,B)
    R2 = np.around(R2, decimals=2)
    t2 = np.around(t2, decimals=2)
    print("\nRotation :\n", R2, "\nTranslation :\n", t2)


checkLines()
checlRT()