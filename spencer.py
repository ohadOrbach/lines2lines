import cv2
import os

def get_video_path():
    # Check if the "video" directory exists
    if os.path.exists("video"):
        # Check if the "video" directory is not empty
        if len(os.listdir("video")) > 0:
            # Get the list of files in the "video" directory
            files = os.listdir("video")
            # Check if the "video" directory contains only one file
            if len(files) == 1:
                # Return the path of the video file
                return os.path.join("video", files[0])
    # If the "video" directory does not exist, is empty, or contains more than one file, return None
    return None


def cut_video_to_images(video_path, start_time, end_time):
    # Create a new folder called "new_images"
    images_folder = "new_images"
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)
    else:
        # If the folder already exists, delete all images in it
        for file in os.listdir(images_folder):
            file_path = os.path.join(images_folder, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)

    # Open the video using cv2
    video = cv2.VideoCapture(video_path)
    frame_count = 0
    success = True
    # Set the video to start at the specified time
    video.set(cv2.CAP_PROP_POS_MSEC, start_time * 1000)
    while success:
        # Read the next frame of the video
        success, frame = video.read()
        # If the frame was successfully read and the current time is within the specified range, save it to the "new_images" folder
        current_time = video.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
        if success and current_time >= start_time and current_time < end_time:
            cv2.imwrite(os.path.join(images_folder, "{:03d}.jpg".format(frame_count+1)), frame)
            frame_count += 1
        # Skip the next frame to get 2 frames per second
        success, _ = video.read()
    # Release the video capture object
    video.release()


video_path = get_video_path()
if video_path is not None:
    cut_video_to_images(video_path, 5, 30)
change_background('new_images')