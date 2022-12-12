import numpy as np
from matplotlib import pyplot as plt
from scipy.spatial.transform import Rotation

''' 
    Helper functions for homogenous coordinates conversion
'''


def to_homogenous(points):
    return np.hstack((points, np.ones((len(points), 1))))


def from_homogenous(points):
    points /= points[:, -1:]
    return points[:, :-1]


'''
    Transforms 2d points on image plane to 3d points in world coordinates
    by applying inverse camera transformations.
'''


def to_3d(points_2d, K_inv, T_inv):
    points = to_homogenous(points_2d)
    if K_inv is not None:
        points = np.dot(K_inv, points.T).T
        points = to_homogenous(points)
    points = np.dot(T_inv, points.T).T
    points = from_homogenous(points)
    return points


'''
    Transforms a center + set of points into a set of lines
    defined by unit direction vectors from the center.
'''


def get_direction_vectors(center, points):
    direction = points - center
    return direction / np.linalg.norm(direction, axis=-1)[:, np.newaxis]


'''
    Converts 2d points on image into 3D lines.
    Takes set of points, inverse intrinsic camera matrix K_inv 
    and inverse extrinsic matrix T_inv.
    Returns origin point of the lines, and a list of points on 
    the image plane but the in world coordinate system.
'''


def get_3d_lines(points, K_inv, T_inv):
    points = to_3d(points, K_inv, T_inv)
    origin = to_3d(np.zeros((1, 3)), None, T_inv)[0]
    return origin, points


''' 
    Generates calibration matrix given center point coordinates cx, cy
    and focal distances fx, fy
'''


def generate_intrinsics(fx=1, fy=1, cx=0, cy=0):
    return np.asarray([[fx, 0, cx],
                       [0, fy, cy],
                       [0, 0, 1]])


''' 
    Generates a rotation-translation matrix given 6 degrees of freedom
    cx, cy, cz - translation
    ax, ay, az - rotation (Euler angles)
'''


def generate_extrinsics(cx, cy, cz, rx, ry, rz):
    rotation = Rotation.from_euler("xyz", (rx, ry, rz)).as_matrix()
    translation = np.asarray([cx, cy, cz])
    T = np.eye(4)
    T[:3, :3] = rotation
    T[:3, -1] = translation
    return T


''' 
    Generates a circle of cameras.
    Cameras are placed around origin in a circle of a given radius,
    Each pair of cameras are distanced by an arc of a given angle.
    The circle is in the plane XY, the Z coordinate is always 0.
    Returns the inverse extrinsics matrix.
'''


def generate_circle_of_cameras(R, count, arc_angle):
    Ts_inv = []
    for i in range(count):
        alpha = arc_angle * i
        T_inv = generate_extrinsics(
            R * np.cos(alpha), R * np.sin(alpha), 0,  # center
            -np.pi / 2, 0, alpha + np.pi / 2)  # rotation
        Ts_inv.append(T_inv)
    return Ts_inv


'''
    Visualization of single image and a corresponding set of lines.
'''


# helper visualization function - just to keep aspect ratio
def _set_axes_equal(ax: plt.Axes):
    limits = np.array([
        ax.get_xlim3d(),
        ax.get_ylim3d(),
        ax.get_zlim3d(),
    ])
    origin = np.mean(limits, axis=1)
    radius = 0.5 * np.max(np.abs(limits[:, 1] - limits[:, 0]))
    _set_axes_radius(ax, origin, radius)


# helper visualization function - just to keep aspect ratio
def _set_axes_radius(ax, origin, radius):
    x, y, z = origin
    ax.set_xlim3d([x - radius, x + radius])
    ax.set_ylim3d([y - radius, y + radius])
    ax.set_zlim3d([z - radius, z + radius])


# shows image with fixed aspect ratio
def plt_show_fixed_aspect(ax):
    ax.set_box_aspect([1, 1, 1])
    _set_axes_equal(ax)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.show()


# main visualization function
def visualize(ax, center, points, title="Visualization"):
    ax.set_title(title)
    ax.scatter(points[:, 0], points[:, 1], points[:, 2], s=4)
    for i in range(len(points)):
        ax.plot(*zip(center, points[i]), color="b", linewidth=1)
