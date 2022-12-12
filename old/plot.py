import matplotlib.pyplot as plt


def plot3d(P1, P2, A, B):
    '''
    :param P1: Set of vectors
    each vector (X,Y,Z)+t(U,V,W)
    size Nx2x3
    :param P2: Set of vectors (matches to P1)
    :param A: Set of points from P1
    each point (X,Y,Z)
    size Nx3
    :param B: Set of points from P2 (matches to A)
    :return: plot in 3d
    Ohad Orbach
    '''
    scalar = 10
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    for i in range(len(P1)):
        ax.quiver(P1[i][0][0],
                  P1[i][0][1],
                  P1[i][0][2],
                  scalar * P1[i][1][0],
                  scalar * P1[i][1][1],
                  scalar * P1[i][1][2],
                  length=5)
        ax.quiver(P2[i][0][0],
                  P2[i][0][1],
                  P2[i][0][2],
                  scalar * P2[i][1][0],
                  scalar * P2[i][1][1],
                  scalar * P2[i][1][2],
                  length=5)

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_xlim([-20, 20])
    ax.set_ylim([-20, 20])
    ax.set_zlim([-20, 20])

    for i in range(len(A)):
        ax.scatter(A[i][0], A[i][1], A[i][2], marker='o', s=100)
        ax.scatter(B[i][0], B[i][1], B[i][2], marker='>', s=100)

    plt.show()
