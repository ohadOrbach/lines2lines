import pygame
import numpy as np
from math import *

#---------------------------------------- COLORS RGB ----------------------------------------
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (135, 206, 235)
GREEN = (193, 255, 193)
LAVANDER = (171, 130, 255)
PINK = (255, 192, 203)
AZURE1 = (240, 255, 255)
AZURE2 = (224, 238, 238)
AZURE3 = (193, 205, 205)
AZURE4 = (131, 139, 139)
POWDEBLUE = (176, 224, 230)

#-------------------------------------- DISPLAY CONTROL ----------------------------------------
WIDTH, HEIGHT = 800, 600                          # Width and Height of the display window.
pygame.display.set_caption("3D Box projection")   # Caption of the display window
screen = pygame.display.set_mode((WIDTH, HEIGHT))

scale = 100                                       # How big is the object view.

circle_pos = [WIDTH/2, HEIGHT/2]                  # (x, y). Object's place in the window.

#-------------------------------- ROTATION ANGLES DEFINITIONS ----------------------------------
# (10,0,0) = 360 rotation on Y + 10 deg angle on the object.
angle_x = 10
angle_y = 0
angle_z = 0
#-------------------------------- ALL THE VERTICES OF THE BOX----------------------------------------------------------------
points = []
points.append(np.matrix([-1, -1, 1]))
points.append(np.matrix([1, -1, 1]))
points.append(np.matrix([1,  1, 1]))
points.append(np.matrix([-1, 1, 1]))
points.append(np.matrix([-1, -1, -1]))
points.append(np.matrix([1, -1, -1]))
points.append(np.matrix([1, 1, -1]))
points.append(np.matrix([-1, 1, -1]))

#----------- PROJECTION MATRIX ---------------
projection_matrix = np.matrix([[1, 0, 0],
                               [0, 1, 0]])

projected_points = [[n, n] for n in range(len(points))]

# Function to draw lines between given vertices.
def connect_points( i, j, points):
    pygame.draw.line(screen, LAVANDER, (points[i][0], points[i][1]), (points[j][0], points[j][1]))

# Set time for display.
clock = pygame.time.Clock()

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

    # Rotation matrices definitions.
    rotation_z = np.matrix([
        [cos(angle_z), -sin(angle_z), 0],
        [sin(angle_z), cos(angle_z), 0],
        [0, 0, 1],
    ])

    rotation_y = np.matrix([
        [cos(angle_y), 0, sin(angle_y)],
        [0, 1, 0],
        [-sin(angle_y), 0, cos(angle_y)],
    ])

    rotation_x = np.matrix([
        [1, 0, 0],
        [0, cos(angle_x), -sin(angle_x)],
        [0, sin(angle_x), cos(angle_x)],
    ])

    # Rotation Matrix.
    ROTATION = rotation_x @ rotation_y @ rotation_z
    # Speed of the rotation.
    angle_y += 0.01

    # Fill the background with wanted color.
    screen.fill(BLACK)

    i = 0   # counter
    # Printing points loop.
    for point in points:
        rotated2d = np.dot(ROTATION, point.reshape((3, 1)))
        projected2d = np.dot(projection_matrix, rotated2d)

        x = int(projected2d[0][0] * scale) + circle_pos[0]
        y = int(projected2d[1][0] * scale) + circle_pos[1]

        projected_points[i] = [x, y]
        pygame.draw.circle(screen, BLUE, (x, y), 5)
        i += 1

    # Polygon(surface, color, points, width=0) -> Rect
    pygame.draw.polygon(screen, AZURE1, projected_points[0:4])
    pygame.draw.polygon(screen, AZURE2, projected_points[4:8])
    pygame.draw.polygon(screen, AZURE3, np.array(projected_points)[[0, 1, 5, 4]])
    pygame.draw.polygon(screen, AZURE4, np.array(projected_points)[[1, 2, 6, 5]])
    pygame.draw.polygon(screen, POWDEBLUE, np.array(projected_points)[[2, 3, 7, 6]])
    pygame.draw.polygon(screen, WHITE, np.array(projected_points)[[3, 0, 4, 7]])

    # Lines drawing loop.
    for p in range(4):
        connect_points(p, (p+1) % 4, projected_points)
        connect_points(p+4, ((p+1) % 4) + 4, projected_points)
        connect_points(p, (p+4), projected_points)


    pygame.display.update()