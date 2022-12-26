import cv2
import numpy as np


def checkCoutOutput(values):
    for value in values:
        value = value.strip()
        if value == '':
            return 0, 0, 0, 0
    return values[0], values[1], values[2], values[3].strip()


def readMotionVectorsAsNumpy(file_name, video_path=None, result_video_path=None):
    frames = []
    with open(file_name, "r") as file:
        for line in file.readlines():
            if "frame" in line:
                frames.append([])
            else:
                values = line.split(',')
                if len(values) == 4:
                    src_x, src_y, dst_x, dst_y = checkCoutOutput(values)
                    frames[-1].append(np.array([float(src_x), float(src_y), float(dst_x), float(dst_y)]))
    frames = np.array(frames)
    if video_path is not None:
        cap = cv2.VideoCapture(video_path)
        writer = None
        if result_video_path is not None:
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            writer = cv2.VideoWriter(result_video_path, fourcc, int(cap.get(cv2.CAP_PROP_FPS)),
                                     (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
        for frame in frames:
            ret, img = cap.read()
            for mv in frame:
                img = cv2.arrowedLine(img, (int(mv[0]), int(mv[1])), (int(mv[2]), int(mv[3])), (0, 255, 0), 1)
            if writer is not None:
                writer.write(img)
            cv2.imshow("motion vector frame", img)
            cv2.waitKey(1)
        cap.release()
        if writer is not None:
            writer.release()
    return frames


if __name__ == "__main__":
    readMotionVectorsAsNumpy("./IMG_0330_motion_vectors.txt", "./video/IMG_0330.MOV",
                             "./IMG_0330_result.avi")
