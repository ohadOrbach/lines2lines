import numpy as np

class LineR3:
    def __init__(self, origin, point, line=None):
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

    def normalize(self):
        self.direction = self.direction / np.linalg.norm(self.direction)

    def add_noise(self, up_lim=0.05):
        noise = np.random.normal(0, up_lim, self.direction.shape)
        self.direction = self.direction + noise
        self.direction = self.direction / np.linalg.norm(self.direction)

    def closest_point(self, other):
        '''
        Triangulation: finding closest points to two lines.
        P1 = point on first line
        d1 = first line's direction vector
        p2 = point on the second line
        d1 = second line's direction vector
        '''

        if np.isclose(np.abs(np.dot(self.direction, other.direction)), 1):
            # parallel lines, returning any middle point inbetween
            return self.origin, other.origin
        else:
            # intersecting or skew lines, returning the point with minimal distance
            n = np.cross(self.direction, other.direction)
            t1 = np.dot((np.cross(other.direction, n)), (other.origin - self.origin)) / (np.dot(n, n))
            t2 = np.dot((np.cross(self.direction, n)), (other.origin - self.origin)) / (np.dot(n, n))
            p1 = self.origin + (t1 * self.direction)
            p2 = other.origin + (t2 * other.direction)
            return p1, p2

    def R_T_On_Line(self, R, t):
        new_origin = np.dot(R, self.origin) + t
        new_point = np.dot(R, self.point) + t
        self.update_line(new_origin, new_point)

    def __str__(self):
        return "\n(x,y,z) + t(u,v,w) = ", str(self.origin), " + t", str(self.direction)
