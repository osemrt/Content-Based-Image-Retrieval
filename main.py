from functions import *
from DatasetImage import *

if __name__ == '__main__':
    # Getting dataset and query path
    dataset_path, count = get_inputs_from_user()

    # Image paths in the dataset
    files = get_image_paths(dataset_path)
    files = np.array(files)

    # Creating dataset
    dataset = []
    for i in range(0, files.size, 1):
        print("{}...".format(i+1))
        dataset_image = DatasetImage(files[i])
        dataset.append(dataset_image)
        print("{} is added to dataset...\n".format(dataset_image.get_name()))

    while 1:

        # Getting query image path from the user
        query_image_path = get_query_image_path_from_user()

        # checking whether the given path is valid or not
        if os.path.exists(query_image_path) and os.path.isfile(query_image_path):

            # Creating dataset-image instance for query image
            query_image = DatasetImage(query_image_path)

            # Finding the most similar images
            similar_rgb_indexes = find_similar_rgb_images(dataset, files.size, query_image)
            similar_lbp_indexes = find_similar_lbp_images(dataset, files.size, query_image)
            similar_indexes = find_similar_images(dataset, files.size, query_image)

            print("\n-------------------------------------------")
            print("\nThe closest images to \"{}\" according to only RGB distances (The closest image printed first).".format(query_image.get_filename()))
            print_filenames(dataset, similar_rgb_indexes, count)
            similarity_percentage_rgb = finding_similarity_percentage(dataset, query_image.get_filename(), similar_rgb_indexes, count)
            print("The similarity percentage is %{:0.3f}".format(similarity_percentage_rgb))

            print("\nThe closest images to \"{}\" according to only LBP distances (The closest image printed first).".format(query_image.get_filename()))
            print_filenames(dataset, similar_lbp_indexes, count)
            similarity_percentage_lbp = finding_similarity_percentage(dataset, query_image.get_filename(),similar_lbp_indexes, count)
            print("The similarity percentage is %{:0.3f}".format(similarity_percentage_lbp))

            print("\nThe closest images to \"{}\" according to both LBP and RGB (The closest image printed first).".format(query_image.get_filename()))
            print_filenames(dataset, similar_indexes, count)
            similarity_percentage_both = finding_similarity_percentage(dataset, query_image.get_filename(),similar_indexes, count)
            print("The similarity percentage is %{:0.3f}".format(similarity_percentage_both))

            dataset[similar_indexes[-1]].show_image()
            query_image.show_image()

            cv.waitKey(0)
            cv.destroyWindow(dataset[similar_indexes[-1]].get_filename())
            cv.destroyWindow(query_image.get_filename())

        else:
            print("invalid file path!")
