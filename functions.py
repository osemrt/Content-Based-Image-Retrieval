import numpy as np
import cv2 as cv
import os


# A function to get all image paths
# from a specific root folder
def get_image_paths(root_path):
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(root_path):
        for file in f:
            # if ".jpg" or ".bmp" or "pgm" or "png" in file:
            files.append(os.path.join(r, file))
    return files


# Gets dataset folder path
# from the user
def get_dataset_path_from_user():
    dataset_path = input("Dataset folder path: ")
    return dataset_path


# Takes an image and
# returns its normalized image
def normalize_image(image):
    resized_image = cv.resize(image, (800, 800))
    normalized_image = cv.normalize(resized_image, None, 0, 255, cv.NORM_MINMAX)
    return normalized_image


# A function calculates the histogram of the given image
# returns its 3-channel histogram array
def rgb_histogram(image):
    red_channel_histogram = np.zeros(256, dtype=int)
    green_channel_histogram = np.zeros(256, dtype=int)
    blue_channel_histogram = np.zeros(256, dtype=int)

    for i in range(0, image.shape[0], 1):
        for j in range(0, image.shape[1], 1):
            pixel = image[i][j]
            blue_channel_histogram[pixel[0]] += 1
            green_channel_histogram[pixel[1]] += 1
            red_channel_histogram[pixel[2]] += 1

    hist = np.array([red_channel_histogram, green_channel_histogram, blue_channel_histogram])
    return hist


# A function returns the histogram of the given grayscale image
def grayscale_histogram(grayscale):
    hist = np.zeros(256, dtype=int)
    for i in range(0, grayscale.shape[0], 1):
        for j in range(0, grayscale.shape[1], 1):
            hist[grayscale[i][j]] += 1

    return hist

