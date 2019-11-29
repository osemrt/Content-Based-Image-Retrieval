from common import *


# A function to get all image paths
# in a specific  folder
def get_image_paths(root_path):
    files = []
    supported_extensions = ".bmp" ".pbm" ".pgm" ".ppm" ".jpeg" ".jpg" ".jpe" ".png" ".tiff" ".tif"
    # r=root, d=directories, f = files
    for r, d, f in os.walk(root_path):
        for file in f:
            extension = file.format().split('.')[-1]
            if extension in supported_extensions:
                files.append(os.path.join(r, file))
    return files


# Gets dataset and query image path
# from the user using an argument parser
def get_inputs_from_user():
    program = '''
              IMPORT: You have to pass the required parameters to start the program.
              Try 'main.py --help' for more information.\n              
              '''

    usage = "Extracts query image's a feature and retrieves similar image from the image database."

    parser = ArgumentParser(prog=textwrap.dedent(program),
                            usage=usage,
                            formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("-d", "--dataset",
                        dest="dataset_path",
                        help="the path of image database",
                        metavar="DATASET",
                        required=True, type=str, nargs=1)

    parser.add_argument("-c", "--count", dest="count",
                        help="the number of the max similar images",
                        metavar="COUNT",
                        required=True, type=int, nargs=1)
    args = parser.parse_args()

    dataset_path = "".join(args.dataset_path)
    count = int(''.join(str(i) for i in args.count))

    return dataset_path, count


# Gets query image path
def get_query_image_path_from_user():
    dataset_path = raw_input("\nquery image path: ")
    return dataset_path


# A function to normalize a histogram
def normalize_histogram(hist, total_pixel_count):
    for i in range(0, hist.size, 1):
        hist[i] = hist[i] / total_pixel_count
    return hist


# A function calculates the histogram of the given image
# returns its 3-channel histogram array
def rgb_histogram(image):
    red_channel_histogram = np.zeros(256, dtype=float)
    green_channel_histogram = np.zeros(256, dtype=float)
    blue_channel_histogram = np.zeros(256, dtype=float)

    for i in range(0, image.shape[0], 1):
        for j in range(0, image.shape[1], 1):
            pixel = image[i][j]
            blue_channel_histogram[pixel[0]] += 1
            green_channel_histogram[pixel[1]] += 1
            red_channel_histogram[pixel[2]] += 1

    hist = np.array([red_channel_histogram, green_channel_histogram, blue_channel_histogram])
    return hist


# A function returns LBP histogram of the given grayscale image
def lbp_histogram(grayscale):
    hist = np.zeros(256, dtype=float)
    for i in range(0, grayscale.shape[0], 1):
        for j in range(0, grayscale.shape[1], 1):
            hist[grayscale[i][j]] += 1

    return hist


# A function to convert a RGB image to grayscale
def rgb_to_grayscale(rgb_image):
    grayscale_image = np.zeros_like(rgb_image)
    grayscale_image.astype(np.uint8)
    for i in range(0, rgb_image.shape[0], 1):
        for j in range(0, rgb_image.shape[1], 1):
            pixel = rgb_image[i][j]
            b = pixel[0]
            g = pixel[1]
            r = pixel[2]

            grayscale_image[i][j] = int(r * 0.30 + b * 0.11 + g * 0.59)

    return grayscale_image


# A function to get LBP image of the given image
def get_lbp_image(image):
    height, width, channel = image.shape
    if channel > 1:
        image = rgb_to_grayscale(image)

    lbp_image = np.zeros_like(image)
    neighbor = 3
    factor = [[1, 2, 4],
              [128, 0, 8],
              [64, 32, 16]]

    for i in range(0, height - neighbor, 1):
        for j in range(0, width - neighbor, 1):
            img = image[i:i + neighbor, j:j + neighbor]
            center = img[1][1]

            img = (img >= center) * 1
            img = img * factor
            total = np.sum(img)
            lbp_image[i + 1][j + 1] = total

    return lbp_image


# A function to print image filenames
# after finding similar images
def print_filenames(dataset, indexes, count):
    i = 1
    while i <= indexes.size and i <= count:
        print(dataset[indexes[-i]].get_filename())
        i += 1


def finding_similarity_percentage(dataset, query_image_filename, indexes, max):
    count = 0.0
    i = 1
    while i <= indexes.size and i <= max:
        filename = dataset[indexes[-i]].get_filename()
        if query_image_filename[0] == filename[0] and query_image_filename[1] == filename[1]:
            count += 1.0
        i += 1

    if indexes.size > max:
        percentage = (count / max) * 100
    else:
        percentage = (count / indexes.size) * 100

    return percentage


# A function to find the most similar images to the given image
# according to RGB values by using Manhattan City Block (L1 norm) method
def find_similar_rgb_images(dataset, size, query_image):
    index = []
    min_distance = sys.maxsize

    query_rgb_hist = query_image.get_rgb_histogram()

    for i in range(0, size, 1):
        rgb_hist = dataset[i].get_rgb_histogram()

        red_distance = hist_difference(rgb_hist[0], query_rgb_hist[0])
        blue_distance = hist_difference(rgb_hist[1], query_rgb_hist[1])
        green_distance = hist_difference(rgb_hist[2], query_rgb_hist[2])

        total_rgb_distance = red_distance + blue_distance + green_distance
        if total_rgb_distance < min_distance:
            min_distance = total_rgb_distance
            index.append(i)

    index = np.array(index)
    return index


# A function to find the most similar images to the given image
# according to LBP values by using Manhattan City Block (L1 norm) method
def find_similar_lbp_images(dataset, size, query_image):
    index = []
    min_distance = sys.maxsize

    query_lbp_hist = query_image.get_lbp_histogram()

    for i in range(0, size, 1):
        lbp_hist = dataset[i].get_lbp_histogram()
        lbp_distance = hist_difference(lbp_hist, query_lbp_hist)

        if lbp_distance < min_distance:
            min_distance = lbp_distance
            index.append(i)

    index = np.array(index)
    return index


# A function to find the most similar images to the given image
# according to the summation of LBP and RGB distances
def find_similar_images(dataset, size, query_image):
    index = []
    min_distance = sys.maxsize

    query_lbp_hist = query_image.get_lbp_histogram()
    query_rgb_hist = query_image.get_rgb_histogram()

    for i in range(0, size, 1):
        lbp_hist = dataset[i].get_lbp_histogram()
        rgb_hist = dataset[i].get_rgb_histogram()

        lbp_distance = hist_difference(lbp_hist, query_lbp_hist)
        r_distance = hist_difference(rgb_hist[0], query_rgb_hist[0])
        g_distance = hist_difference(rgb_hist[1], query_rgb_hist[1])
        b_distance = hist_difference(rgb_hist[2], query_rgb_hist[2])

        total_distance = lbp_distance + r_distance + g_distance + b_distance

        if total_distance < min_distance:
            min_distance = total_distance
            index.append(i)

    index = np.array(index)
    return index


# A function to calculate the distance of two given histogram arrays
def hist_difference(hist1, hist2):
    total = 0
    if hist1.size != hist2.size:
        print("An error has occurred while calculating the histogram difference...")
    else:
        for i in range(0, hist1.size, 1):
            total += abs(hist1[i] - hist2[i])

    return total
