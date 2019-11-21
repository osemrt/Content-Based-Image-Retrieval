from common import *
from functions import *


class DatasetImage:
    def __init__(self, path):
        self.image = cv.imread(path)
        self.name = path.split(os.path.sep)[-1]

    def show_image(self):
        cv.imshow(self.name, self.image)

    def create_rgb_histogram(self):
        self.rgb_histogram = rgb_histogram(self.image)

    def create_lbp_image(self):
        self.lbp_image = get_lbp_image(self.image)

    def create_lbp_histogram(self):
        self.lbp_histogram = grayscale_histogram(self.lbp_image)
