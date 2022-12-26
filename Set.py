import matplotlib.pyplot as plt

from Line import *


class SetOfLines:
    def __init__(self, lines=None, Set=None):
        if Set is not None:
            self.lines = np.zeros_like(Set.lines)
            for i in range(len(Set.lines)):
                self.lines[i] = LineR3(line=Set.lines[i])
            self.size = len(self.lines)
            self.points = Set.points.copy()
        else:
            self.lines = lines
            self.size = len(self.lines)
            self.points = np.zeros([self.size, 3])

    def closest_points_set(self, other):
        for i in range(self.size):
            self.points[i], other.points[i] = self.lines[i].closest_point(other.lines[i])

    def distance(self, other):
        return np.around(np.sum(np.linalg.norm(self.points[i] - other.points[i]) for i in range(self.size)), decimals=2)

    def best_fit_transform(self, other):
        """
        Calculates the least-squares best-fit transform that maps corresponding points A to B in m spatial dimensions
        Input:
          A: Nxm numpy array of corresponding points
          B: Nxm numpy array of corresponding points
        Returns:
          T: (m+1)x(m+1) homogeneous transformation matrix that maps A on to B
          R: mxm rotation matrix
          t: mx1 translation vector
        """

        # get number of dimensions
        m = self.points.shape[1]

        # translate points to their centroids
        centroid_A = np.mean(self.points, axis=0)
        centroid_B = np.mean(other.points, axis=0)
        AA = self.points - centroid_A
        BB = other.points - centroid_B

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
    
    # This function placing the second point cloud on the unit sphere.!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! NEW FUNC ADDED 26.12.22
    def best_fit_transform_constrained(self, other):
        """
        Using best-fit transform that maps corresponding points A to B in m spatial dimensions
        Input:
          A: Nxm numpy array of corresponding points
          B: Nxm numpy array of corresponding points
        Returns:
          T: (m+1)x(m+1) homogeneous transformation matrix that maps A on to B
          R: mxm rotation matrix
          t: Constrained mx1 translation vector.
        """
        T, R, t =  self.best_fit_transform(other)
        # Normalize translation and calc the diffeance between normlized.
        norm = np.linalg.norm(t)
        # Add the diff to the second set of lines.
        Tnew = t / norm
        return T, R, Tnew

    def R_t_Set(self, R, t):
        for L in self.lines:
            L.R_T_On_Line(R, t)

    def noise(self, up_limit=0.5):
        for L in self.lines:
            L.add_noise(up_limit)

    def plot3d(self, other, points=True, scalar=5, title=None):
        ax_size = 10
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.set_title(title)
        for i in range(self.size):
            ax.quiver(self.lines[i].origin[0],
                      self.lines[i].origin[1],
                      self.lines[i].origin[2],
                      scalar * self.lines[i].direction[0],
                      scalar * self.lines[i].direction[1],
                      scalar * self.lines[i].direction[2],
                      length=4)
            ax.quiver(other.lines[i].origin[0],
                      other.lines[i].origin[1],
                      other.lines[i].origin[2],
                      scalar * other.lines[i].direction[0],
                      scalar * other.lines[i].direction[1],
                      scalar * other.lines[i].direction[2],
                      length=4)

        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.set_xlim([-ax_size, ax_size])
        ax.set_ylim([-ax_size, ax_size])
        ax.set_zlim([-ax_size, ax_size])
        if points:
            for i in range(self.size):
                ax.scatter(self.points[i][0], self.points[i][1], self.points[i][2], marker='o', s=100)
                ax.scatter(other.points[i][0], other.points[i][1], other.points[i][2], marker='>', s=100)

        plt.show()

    def set_on_sphere(self):
        print("distance to headline before movement", self.lines[0].distance_to_headline())
        for i in range(self.size):
            self.lines[i].on_sphere()
        print("distance to headline after movement", self.lines[0].distance_to_headline())

    def __str__(self):
        ret = tuple()
        for i in self.lines:
            x = i.__str__()
            ret = ret + x
        return ''.join(ret)
