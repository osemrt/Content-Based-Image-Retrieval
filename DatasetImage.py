from functions import *



class DatasetImage:
    def __init__(self, path):
        # assignment image name as its filename
        self.name = path.split(os.path.sep)[-1]

        # reading image from the given path
        self.image = cv.imread(path)
        print("{} is read...".format(self.name))

        # getting image attributes
        self.height, self.width, self.channel = self.image.shape
        self.total_pixel_count = self.height * self.width

        # creating lbp image
        self.lbp_image = get_lbp_image(self.image)
        print("a lbp image is created for {}...".format(self.name))

        # getting image histogram arrays
        self.rgb_histogram = rgb_histogram(self.image)
        print("rgb histogram array is created for {}...".format(self.name))
        self.lbp_histogram = lbp_histogram(self.lbp_image)
        print("lbp histogram array is created for {}...".format(self.name))

        # normalizing histogram arrays after creation them
        # # normalization of R histogram
        self.rgb_histogram[0] = normalize_histogram(self.rgb_histogram[0], self.total_pixel_count)
        # # normalization of G histogram
        self.rgb_histogram[1] = normalize_histogram(self.rgb_histogram[1], self.total_pixel_count)
        # # normalization of B histogram
        self.rgb_histogram[2] = normalize_histogram(self.rgb_histogram[2], self.total_pixel_count)
        # # normalization of lbp histogram
        self.lbp_histogram = normalize_histogram(self.lbp_histogram, self.total_pixel_count)
        print("rgb and lbp histograms of {} are normalized...".format(self.name))

    def get_filename(self):
        return self.name

    def show_image(self):
        cv.imshow(self.name, self.image)

    def show_lbp_image(self):
        cv.imshow("[LBP image of  " + self.name + " ]", self.lbp_image)

    def get_rgb_histogram(self):
        return self.rgb_histogram

    def get_lbp_image(self):
        return self.lbp_image

    def get_lbp_histogram(self):
        return self.lbp_histogram

    def get_name(self):
        return self.name
