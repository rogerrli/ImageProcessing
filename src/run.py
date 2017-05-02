import os
import opencvSupport
import json


resource = os.getcwd() + "/resource.json"
directory = os.getcwd() + "/objects/"


with open('config.json', 'r') as f:
    config = json.load(f)

for object in config['objects'].keys():
    print(object)
object = input("Which object would you like to work on: ")
while object not in config['objects'].keys():
    object = input("ERROR: Please select a valid object: ")

directory = directory + object + "/"
if not os.path.exists(object):
    if "image_path" not in config['objects'][object].keys():
        os.makedirs(directory + "images")
        images = directory + "images/"
        info = directory + "info.txt"
    else:
        images = config['objects'][object]['image_path']
        if images[-1] is not "/":
            images += "/"
        img_dir = images.split("/")
        par_dir = "/".join(img_dir[:-2]) + "/"
        info = par_dir + "info.txt"
    if "negative_images" not in config['objects'][object].keys():
        os.makedirs(directory + "negative_images")
        negative_images = directory + "negative_images/"
    else:
        negative_images = config['objects'][object]['negative_images']
    if not os.path.exists(directory + "/classifier"):
        os.makedirs(directory + "classifier")
    if not os.path.exists(directory + "/vec_files"):
        os.makedirs(directory + "vec_files")


vec_file = directory + "vec_files/vec.vec"
classifier = directory + "classifier/"
rename = input("Do you need to rename image files (Y/N): ").lower()
validInput = False
num_images = opencvSupport.num_images(images)
while not validInput:
    if rename == "y":
        prefix = input("What is the prefix for your files: ")
        opencvSupport.rename(prefix, images)
        validInput = True
        print("Files renamed")
    elif rename == "n":
        validInput = True
    else:
        rename = input("ERROR: Please use Y/N to indicate whether to rename the images: ")

annotate = input("Do you need to annotate your images (Y/N): ").lower()
images_annotated = False
validInput = False
while not validInput:
    if annotate == "y":
        os.chdir(directory)
        opencvSupport.annotate_images(images, info)
        os.chdir(os.path.dirname(os.path.dirname(directory)))
        validInput = True
        images_annotated = True
        print("Images annotated")
    elif annotate == "n":
        validInput = True
        have_annotate = input("Do you have annotated imaged (Y/N): ").lower()
        nested_validInput = False
        while not nested_validInput:
            if have_annotate == "y":
                images_annotated = True
                nested_validInput = True
            elif have_annotate == "n":
                nested_validInput = True
            else:
                have_annotate = input("ERROR: Please use Y/N to indicate whether you have annotated images: ")
    else:
        annotate = input("ERROR: Please use Y/N to indicate whether to annotate the images: ")

use_annotations = input("Do you want to use annotated images for analysis (Y/N): ").lower()
validInput = False
while not validInput:
    opencvSupport.create_bg(directory, negative_images)
    if use_annotations == "y":
        if images_annotated:
            os.chdir(images)
            os.system("opencv_createsamples -info " + info + " -vec " + vec_file)
            use_annotations = True
        else:
            print("ERROR: You do not have any annotated image files")
            use_annotations = "n"
        validInput = True
    elif use_annotations == "n":
        image_multiplier = input("How many instances of the image do you want to overlay: ")
        opencvSupport.create_vec(images, directory, image_multiplier)
        use_annotations = False
        validInput = True
    else:
        use_annotations = input("ERROR: Please use Y/N to indicate whether to use annotated images: ")

train_classifier = input("Do you want to train the classifier (Y/N): ").lower()
validInput = False
classifier_trained = False
if not use_annotations:
    num_images = str(int(image_multiplier) * num_images)
else:
    num_images = str(num_images)
while not validInput:
    if train_classifier == "y":
        os.system("opencv_traincascade -data " + classifier + " -vec " + vec_file + " -bg " + directory + "bg.txt -numStages 12 -minHitRate 0.999 -maxFalseAlarmRate 0.5 -numNeg 3380 -numPos " + num_images)
        validInput = True
        classifier_trained = True
    elif train_classifier == "n":
        validInput = True
        have_classifier_trained = input("Do you have a trained classifier (Y/N): ")
        nested_validInput = False
        while not nested_validInput:
            if have_classifier_trained == "y":
                nested_validInput = True
                classifier_trained = True
            elif have_classifier_trained == "n":
                nested_validInput = True
            else:
                have_classifier_trained = input("ERROR: Please use Y/N to indicate whether you have a trained ..."
                                                "classifier: ")
    else:
        train_classifier = input("ERROR: Please use Y/N to indicate whether to train the classifier: ")

if classifier_trained:
        image_folder = input("Location of images to detect (e.g. images/): ")
        opencvSupport.detect_object(images, classifier + "cascade.xml")
