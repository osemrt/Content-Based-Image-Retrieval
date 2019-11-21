from functions import *

if __name__ == '__main__':
    # Getting dataset and query path
    dataset_path, count = get_inputs_from_user()

    # Image paths in the dataset
    files = get_image_paths(dataset_path)
    files = np.array(files)

    # Creating dataset
    dataset = []
    # TODO: Change the upper limit to files.size
    for i in range(0, files.size, 1):
        dataset_image = DatasetImage(files[i])
        print("{}: {} is added to dataset...".format(i, dataset_image.get_name()))
        dataset.append(dataset_image)
        # dataset[i].show_image()
        # dataset[i].show_lbp_image()

    while 1:
        query_image_path = get_query_image_path_from_user()

        if os.path.exists(query_image_path) and os.path.isfile(query_image_path):

            print(query_image_path)
            # Creating dataset-image instance for query image
            query = DatasetImage(query_image_path)
            query.show_image()

            # Finding the most similar image
            index = find_similar_image(dataset, files.size, query)

            i = 1
            while i < index.size and i <= count:
                image = dataset[index[-i]]
                image.show_image()
                # image.show_lbp_image()
                i += 1

            cv.waitKey(0)
            cv.destroyAllWindows()
        else:
            print("invalid file path!")
