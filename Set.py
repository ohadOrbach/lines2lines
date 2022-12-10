import numpy as np
import matplotlib.pyplot as plt

class SetOfLines():
    def __init__(self, lines=[]):
        self.size = len(lines);
        self.lines = lines

    def polt3d(self, set_of_lines_2, A, B, scalar=10):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        for i in range(self.size):
            ax.quiver(self.lines[i].origin[0],
                      self.lines[i].origin[1],
                      self.lines[i].origin[2],
                      scalar * self.lines[i].direction[0],
                      scalar * self.lines[i].direction[1],
                      scalar * self.lines[i].direction[2],
                      length=5)
            ax.quiver(set_of_lines_2.lines[i].origin[0],
                      set_of_lines_2.lines[i].origin[1],
                      set_of_lines_2.lines[i].origin[2],
                      scalar * set_of_lines_2.lines[i].direction[0],
                      scalar * set_of_lines_2.lines[i].direction[1],
                      scalar * set_of_lines_2.lines[i].direction[2],
                      length=5)

        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.set_xlim([-20, 20])
        ax.set_ylim([-20, 20])
        ax.set_zlim([-20, 20])
        if(A is not None and B is not None):
            for i in range(len(A)):
                ax.scatter(A[i][0], A[i][1], A[i][2], marker='o', s=100)
                ax.scatter(B[i][0], B[i][1], B[i][2], marker='>', s=100)

        plt.show()

    def __str__(self):
        ret = tuple()
        for i in self.lines:
            x = i.__str__()
            ret = ret + x
        return ''.join(ret)
