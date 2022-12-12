import math

import numpy as np


def add_noise(lines):
    for i in range(len(lines)):
        noise = np.random.normal(0, 3, lines[0][1].shape)
        lines[i][1] = lines[i][1] + noise
    return lines


def R_T_On_Lines(R, t, orig, sec_point):
    new_orig = np.zeros_like(orig)
    new_sec_point = np.zeros_like(sec_point)
    for i in range(len(orig)):
        new_orig[i] = np.dot(R, orig[i]) + t
        new_sec_point[i] = np.dot(R, sec_point[i]) + t
    L1 = np.array([new_orig[0], new_sec_point[0] - new_orig[0]])
    L2 = np.array([new_orig[1], new_sec_point[1] - new_orig[1]])
    L3 = np.array([new_orig[2], new_sec_point[2] - new_orig[2]])
    new_lines = np.array([L1, L2, L3])
    return new_lines


def closest_point(r1, e1, r2, e2):
    ''' Triangulation: finding closest points to two lines. '''
    '''P1 = point on first line
       d1 = first line's direction vector
       p2 = point on the second line
       d1 = second line's direction vector '''

    if np.isclose(np.abs(np.dot(e1, e2)), 1):
        # parallel lines, returning any middle point inbetween
        return r1, r2
    else:
        # intersecting or skew lines, returning the point with minimal distance
        n = np.cross(e1, e2)
        t1 = np.dot((np.cross(e2, n)), (r2 - r1)) / (np.dot(n, n))
        t2 = np.dot((np.cross(e1, n)), (r2 - r1)) / (np.dot(n, n))
        p1 = r1 + (t1 * e1)
        p2 = r2 + (t2 * e2)
        return p1, p2


def normline(l):
    l[1] = l[1] / np.linalg.norm(l[1])
    return l


def rotation_matrix(axis, theta):
    """
    Return the rotation matrix associated with counterclockwise rotation about
    the given axis by theta radians.
    """
    axis = np.asarray(axis)
    axis = axis / math.sqrt(np.dot(axis, axis))
    a = math.cos(theta / 2.0)
    b, c, d = -axis * math.sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d

    return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                     [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                     [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])


def best_fit_transform(A, B):
    '''
    Calculates the least-squares best-fit transform that maps corresponding points A to B in m spatial dimensions
    Input:
      A: Nxm numpy array of corresponding points
      B: Nxm numpy array of corresponding points
    Returns:
      T: (m+1)x(m+1) homogeneous transformation matrix that maps A on to B
      R: mxm rotation matrix
      t: mx1 translation vector
    '''

    assert A.shape == B.shape

    # get number of dimensions
    m = A.shape[1]

    # translate points to their centroids
    centroid_A = np.mean(A, axis=0)
    centroid_B = np.mean(B, axis=0)
    AA = A - centroid_A
    BB = B - centroid_B

    # rotation matrix
    H = np.dot(AA.T, BB)
    U, S, Vt = np.linalg.svd(H)
    R = np.dot(Vt.T, U.T)

    # special reflection case
    if np.linalg.det(R) < 0:
        Vt[m - 1, :] *= -1
        R = np.dot(Vt.T, U.T)

    # translation
    t = centroid_B.T - np.dot(R, centroid_A.T)

    # homogeneous transformation
    T = np.identity(m + 1)
    T[:m, :m] = R
    T[:m, m] = t

    return T, R, t
