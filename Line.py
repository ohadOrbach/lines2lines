import numpy as np


class LineR3:
    def __init__(self, origin, point, line=None, random=False):
        if random:
            self.origin = np.random.randint(-5, 5, size=(3,))
            self.point = np.random.randint(-5, 5, size=(3,))
        else:
            if line is None:
                self.origin = origin
                self.point = point
                self.direction_without_norm = self.point - self.origin
                self.direction = self.direction_without_norm / np.linalg.norm(self.direction_without_norm)
            else:
                self.origin = line.origin
                self.point = line.point
                self.direction_without_norm = line.direction_without_norm
                self.direction = line.direction

    def update_line(self, new_origin, new_point):
        self.origin = new_origin
        self.point = new_point
        self.direction_without_norm = self.point - self.origin
        self.direction = self.direction_without_norm / np.linalg.norm(self.direction_without_norm)

    def add_noise(self, up_lim=0.05):
        """
        :param up_lim: upper limit of noise
        :return: add noise to line
        """
        noise = np.random.normal(0, up_lim, self.direction.shape)
        self.direction = self.direction + noise
        self.direction = self.direction / np.linalg.norm(self.direction)

    def closest_point(self, other):
        """
        :param other: Line that matches this line
        :return: (p1,p2) = points on L1,L2 that are
                           the closest to each other
        """
        if np.isclose(np.abs(np.dot(self.direction, other.direction)), 1):
            return self.origin, other.origin
        else:
            n = np.cross(self.direction, other.direction)
            t1 = np.dot((np.cross(other.direction, n)), (other.origin - self.origin)) / (np.dot(n, n))
            t2 = np.dot((np.cross(self.direction, n)), (other.origin - self.origin)) / (np.dot(n, n))
            p1 = self.origin + (t1 * self.direction)
            p2 = other.origin + (t2 * other.direction)
            return p1, p2

    def R_T_On_Line(self, R, t):
        """
        :param R: Rotation matrix
        :param t: Translation
        :return: update this line
        """
        new_origin = np.dot(R, self.origin) + t
        new_point = np.dot(R, self.point) + t
        self.update_line(new_origin, new_point)

    def __str__(self):
        return "\n(x,y,z) + t(u,v,w) = ", str(self.origin), " + t", str(self.direction)
