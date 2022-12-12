from os import path

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

'''
    For each image, returns a list of keypoints and descriptors
'''


def get_descriptors(images):
    def get_sift(sift, image):
        kp = sift.detect(image, None)
        kp, des = sift.compute(image, kp)
        return kp, des

    result = []
    sift = cv.SIFT_create()
    for image in images:
        kp, des = get_sift(sift, image)
        result.append((kp, des))
    return result


'''
    For each image, returns an array of keypoints.
    If only_complete_matches is True:
        Keypoints are ordered, such that keypoints of same indices
        in each array are matched with keypoints of same indices 
        in each other array.
    Else:
        All keypoints from all images are returned
'''


def get_matches(images, only_complete_matches=True, visualize=False):
    ''' Gets a dictionary {from -> to} of keypoint indices for each pair 
        of images '''

    def get_match_dictionaries(descriptors):
        dictionaries = []
        bf = cv.BFMatcher()
        for i in range(len(descriptors) - 1):
            img1, img2 = images[i:i + 2]
            ((kp1, des1), (kp2, des2)) = descriptors[i:i + 2]
            matches = bf.knnMatch(des1, des2, k=2)
            # Apply ratio test
            good = []
            for m, n in matches:
                if m.distance < 0.75 * n.distance:
                    good.append([m])
            match_dictionary = dict([(x[0].queryIdx, x[0].trainIdx) for x in good])
            dictionaries.append(match_dictionary)
            if visualize:
                plt.figure()
                plt.title("Matching images {} and {}".format(i, i + 1))
                img3 = cv.drawMatchesKnn(img1, kp1, img2, kp2, good, flags=2, outImg=None)
                plt.imshow(img3)
                plt.show()
        return dictionaries

    ''' Gets a list of complete match paths, containing keypoints from 
        all images. Only such complete matches are returned by get_matches '''

    def get_complete_matches(match_dictionaries):
        def get_path(query):
            path = [query]
            for dictionary in match_dictionaries:
                if query in dictionary:
                    query = dictionary[query]
                    path.append(query)
                else:
                    break
            return path

        complete_matches = []
        for item in match_dictionaries[0].keys():
            path = get_path(item)
            if len(path) == len(match_dictionaries) + 1:
                complete_matches.append(path)
        return complete_matches

    # using helper functions to get descriptors and complete matches
    descriptors = get_descriptors(images)
    if only_complete_matches:
        # save only keypoints matched across all images
        match_dictionaries = get_match_dictionaries(descriptors)
        complete_matches = get_complete_matches(match_dictionaries)
        # composing list of lists of matched keypoints in each image
        points_2d = [np.zeros((len(complete_matches), 2)) for i in range(len(images))]
        for img_idx in range(len(images)):
            for keypoint_idx in range(len(complete_matches)):
                idx_in_descriptors = complete_matches[keypoint_idx][img_idx]
                kp, des = descriptors[img_idx]
                keypoint = kp[idx_in_descriptors].pt
                points_2d[img_idx][keypoint_idx] = keypoint
    else:
        # save all keypoints
        points_2d = []
        for img_idx in range(len(images)):
            kp, des = descriptors[img_idx]
            points_2d.append(np.asarray([keypoint.pt for keypoint in kp]))
    if visualize:
        for i in range(len(points_2d)):
            plt.figure();
            plt.title("Matched eypoints: image {}".format(i))
            plt.imshow(images[i], cmap='gray')
            plt.scatter(points_2d[i][:, 0], points_2d[i][:, 1]);
            plt.gca().set_aspect('equal')
    return points_2d


if __name__ == "__main__":
    IMGS_PATH = "images_bottle/"
    images = [cv.imread(path.join(IMGS_PATH, '{:03d}.png'.format(n)), 0)
              for n in [10, 11, 12]]
    points_2d = get_matches(images, visualize=True)
