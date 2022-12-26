# Import libraries
import numpy as np
import matplotlib.pyplot as plt
import cv2
import glob
import time
start_time = time.time()

def main():
     #--------------------------- CONTROL DEFINITIONS BY USER --------------------------------------
    # Angles of view control.
    elevation_view = 10    # ‘elevation_view’ stores the elevation angle in the z plane.
    azim_angle = 45        # ‘azim_view’ stores the azimuth angle in the x,y plane.

    # Box's parameters.
    box = [15, 19, 28]   # [y, x, z]

    # Axes limits.
    X_lim = 10
    Y_lim = 10
    Z_lim = 10

    # Control Transparency of the BOX. # Between [0, 1], while 0 is transparent.
    alpha = 0.9

    # Define if you want to make frame to each angle - it takes time and useful for making video.
    # NO = 0, YES = 1.
    to_frames = 0

    # Define if you would like to see the plot with axes. NO = 0, YES = 1.
    with_Axes = 1

    # Frames for second - video speed.
    frames_to_sec = 8
    #----------------------------------------------------------------------------------------------

    box_3d_projection(elevation_view, X_lim, Y_lim, Z_lim, alpha, to_frames, azim_angle, with_Axes, box)
    # Uncomment to make a movie.
    #toVideo(elevation_view, frames_to_sec)
    print("--- %s seconds ---" % (time.time() - start_time))

#---------------------------------- SUB FUNCTIONS -------------------------------------------------

def box_3d_projection(elevation_view, X_lim, Y_lim, Z_lim, alpha, to_frames, azim_angle, with_Axes, box):
    # Create axix
    axes = [X_lim, Y_lim, Z_lim]
    # Create Data
    data = np.ones(box, dtype=np.bool)

    # Control colour
    colors = np.empty(box + [4], dtype=np.float)

    colors[:] = [0.1, 0.5, 1, alpha]# blue
    #colors[:] = [0.9, 1, 1, alpha] #white

    # Plot figure
    fig = plt.figure()
    fig.patch.set_facecolor('black')
    ax = fig.add_subplot(111, projection='3d')

    if (with_Axes):
        ax.patch.set_facecolor('black')

        # Create x,y,z axis labels:
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        ax.tick_params(axis='z', colors='white')

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        ax.yaxis.label.set_color('white')
        ax.xaxis.label.set_color('white')
        ax.zaxis.label.set_color('white')

    else:
        ax.xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
        ax.yaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
        ax.zaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))

        # Hide grid lines
        ax.grid(False)
        ax.patch.set_facecolor('black')

    ax.title.set_color('white')
    plt.title('3D Spinning Box')

    # Voxels are used to customizations of the sizes, positions and colors.
    ax.voxels(data, facecolors=colors)

    ax.view_init(elevation_view, azim_angle)
    plt.axis('scaled')

    if(to_frames):
        for angle in range(0, 360):
            plt.title('Current angle is:  ' + str(angle) + '°.\n3D Box (length =  19 cm, width = 15 cm, height = 28 cm)',  x=0.5, y=1)
            plt.plot(axes[0], axes[1], axes[2])
            ax.view_init(elevation_view, angle)
            plt.savefig('frames/' + str(angle) + 'angle.png')

    plt.show()

#--------------------------------------------------------------------------------------
def toVideo(elevation_view, frames_to_sec):
    img_array = []
    for angle in range(0, 360):
        for filename in glob.glob('frames/' + str(angle) + 'angle.png'):
            img = cv2.imread(filename)
            height, width, layers = img.shape
            size = (width, height)
            img_array.append(img)

    out = cv2.VideoWriter('Spinning box elevation view of ' + str(elevation_view) +
                          '(deg).avi', cv2.VideoWriter_fourcc(*'DIVX'), frames_to_sec, size)

    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()

 #--------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()

