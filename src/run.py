import os
import opencvSupport
import json


def setup_from_config():
    """
    Sets up variables from the configuration file.
    Prompts the user as for which subject to work on, and extracts three pieces from the configuration file
        1.) The directory under which to create temporary and permant files, most importantly the classifier
        2.) The directory under which the images to train the classifier can be found
        3.) The directory under which the images to use as the negative base to train the classifier can be found
    It returns the directories for all the locations for the files, both temporary and permanent.
    """
    with open('config.json', 'r') as f:
        config = json.load(f)
    for subject in config['subjects'].keys():
        print(subject)
    subject = input("Which subject would you like to work on: ")
    while subject not in config['subjects'].keys():
        subject = input("ERROR: Please select a valid subject: ")
    directory = config['subjects'][subject]["classifier_location"]
    if not os.path.exists(subject):
        if "image_path" not in config['subjects'][subject].keys():
            os.makedirs(directory + "images")
            images = directory + "images/"
            info = directory + "info.txt"
        else:
            images = config['subjects'][subject]['image_path']
            if images[-1] is not "/":
                images += "/"
            img_dir = images.split("/")
            par_dir = "/".join(img_dir[:-2]) + "/"
            info = par_dir + "info.txt"
        if "negative_images" not in config['subjects'][subject].keys():
            os.makedirs(directory + "negative_images")
            negative_images = directory + "negative_images/"
        else:
            negative_images = config['subjects'][subject]['negative_images']
        if not os.path.exists(directory + "/classifier"):
            os.makedirs(directory + "classifier")
        if not os.path.exists(directory + "/vec_files"):
            os.makedirs(directory + "vec_files")
    vec = directory + "vec_files/"
    classifier = directory + "classifier/"
    opencvSupport.create_bg(directory, negative_images)
    return images, negative_images, info, vec, classifier, directory


def rename_images(images):
    """
    This will rename images as necessary if they have been scraped and have a non-uniform naming standard. This should
    be run the first time in order to create a clean sampling name format
    :param images: The directory from where the images are located
    """
    rename = input("Do you need to rename image files (Y/N): ").lower()
    valid_input = False
    while not valid_input:
        if rename == "y":
            prefix = input("What is the prefix for your files: ")
            opencvSupport.rename(prefix, images)
            valid_input = True
            print("Files renamed")
        elif rename == "n":
            valid_input = True
        else:
            rename = input("ERROR: Please use Y/N to indicate whether to rename the images: ")


def annotate_images(images, info):
    """
    Sets up annotation for images
    :param images: The directory from where the images are located
    :param info: The landing spot for where info.txt
    """
    annotate = input("Do you need to annotate your images (Y/N): ").lower()
    images_annotated = False
    valid_input = False
    while not valid_input:
        if annotate == "y":
            anno_not_complete = opencvSupport.annotate_images(images, info)
            valid_input = True
            images_annotated = True
            if anno_not_complete:
                print("Image annotation paused")
            else:
                print("Images annotated")
        elif annotate == "n":
            valid_input = True
            have_annotate = input("Do you have annotated imaged (Y/N): ").lower()
            nested_valid_input = False
            while not nested_valid_input:
                if have_annotate == "y":
                    images_annotated = True
                    nested_valid_input = True
                elif have_annotate == "n":
                    nested_valid_input = True
                else:
                    have_annotate = input("ERROR: Please use Y/N to indicate whether you have annotated images: ")
        else:
            annotate = input("ERROR: Please use Y/N to indicate whether to annotate the images: ")
    return images_annotated


def create_samples(images, info, images_annotated, vec):
    """
    :param images: The directory from where the images are located
    :param info: The directory from where the info.txt will be located
    :param images_annotated: Boolean if the images have been annotated
    :param vec:
    """
    use_annotations = input("Do you want to use annotated images for analysis (Y/N): ").lower()
    valid_input = False
    image_multiplier = 0
    while not valid_input:
        if use_annotations == "y":
            if images_annotated:
                os.chdir(images)
                os.system("opencv_createsamples -info " + info + " -vec " + vec + "vec.vec")
                use_annotations = True
            else:
                print("ERROR: You do not have any annotated image files")
                use_annotations = "n"
            valid_input = True
        elif use_annotations == "n":
            image_multiplier = input("How many instances of the image do you want to overlay: ")
            opencvSupport.create_vec(images, vec, image_multiplier)
            use_annotations = False
            valid_input = True
        else:
            use_annotations = input("ERROR: Please use Y/N to indicate whether to use annotated images: ")
    return use_annotations, image_multiplier


def create_classifier(images, use_annotations, image_multiplier, directory):
    train_classifier = input("Do you want to train the classifier (Y/N): ").lower()
    valid_input = False
    classifier_trained = False
    num_images = opencvSupport.num_images(images)
    if not use_annotations:
        num_images = str(int(image_multiplier) * num_images)
    else:
        num_images = str(num_images)
    while not valid_input:
        if train_classifier == "y":
            os.system("opencv_traincascade -data " + classifier + " -vec " + vec + "vec.vec -bg " + directory +
                      "bg.txt -numStages 12 -minHitRate 0.999 -maxFalseAlarmRate 0.5 -numNeg 3380 -numPos " +
                      num_images)
            valid_input = True
            classifier_trained = True
        elif train_classifier == "n":
            valid_input = True
            have_classifier_trained = input("Do you have a trained classifier (Y/N): ")
            nested_valid_input = False
            while not nested_valid_input:
                if have_classifier_trained == "y":
                    nested_valid_input = True
                    classifier_trained = True
                elif have_classifier_trained == "n":
                    nested_valid_input = True
                else:
                    have_classifier_trained = input("ERROR: Please use Y/N to indicate whether you have a trained ..."
                                                    "classifier: ")
        else:
            train_classifier = input("ERROR: Please use Y/N to indicate whether to train the classifier: ")
    return classifier_trained


def use_classifier(classifier_trained):
    if classifier_trained:
        print("NEED TO ADD CODE HERE YO")
        opencvSupport.detect_subject(images, classifier + "cascade.xml")

if __name__ == "__main__":
    images, negative_images, info, vec, classifier, directory = setup_from_config()
    rename_images(images)
    images_annotated = annotate_images(images, info)
    use_annotations, image_multiplier = create_samples(images, info, images_annotated, vec)
    classifier_trained = create_classifier(images, use_annotations, image_multiplier, directory)
    use_classifier(classifier_trained)
