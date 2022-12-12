from os import path

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

from geometry import (generate_intrinsics, generate_circle_of_cameras,
                      get_3d_lines, visualize, plt_show_fixed_aspect,
                      get_direction_vectors)
from matching import get_matches

if __name__ == "__main__":
    R = 5  # radius of the circle of cameras
    ARC_ANGLE = np.pi / 36  # 5 degrees increment, as in the sample images
    IMGS_PATH = "images_bottle/"
    ONLY_COMPLETE_MATCHES = True  # keep only matched keypoints
    images = [cv.imread(path.join(IMGS_PATH, '{:03d}.png'.format(n)), 0)
              for n in range(10, 17)]
    points_2d = get_matches(images, ONLY_COMPLETE_MATCHES)

    h, w = images[0].shape
    f = h + w  # focal length, estimate
    cx, cy = w / 2.0, h / 2.0  # central point, estimate
    K = generate_intrinsics(f, f, cx, cy)
    Ts_inv = generate_circle_of_cameras(R, len(images), ARC_ANGLE)
    K_inv = np.linalg.inv(K)
    centers = []
    points = []
    fig = plt.figure(dpi=200);
    ax = fig.add_subplot(projection="3d");
    for idx, T_inv in enumerate(Ts_inv):  # for each camera
        # note that points 3d are just 2d image points in
        # world coordinate system. They are not a 3d model.
        center_3d, points_3d = get_3d_lines(
            points_2d[idx], K_inv, T_inv)
        centers.append(center_3d)
        points.append(points_3d)
        visualize(ax, center_3d, points_3d)
    plt_show_fixed_aspect(ax)
    # if the direction vectors are needed - they are calculated below.
    line_directions = get_direction_vectors(center_3d, points_3d)
