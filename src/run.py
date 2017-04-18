import os
import opencvSupport

#Identify which object/project you want to work on, and adjust any path variables to follow suit
directory = os.getcwd() + "/objects/"
staple_folders = [".DS_Store"]
object_folders = []
for dir in os.listdir(directory):
    if dir not in staple_folders:
        object_folders.append(dir)
        print(dir)
object_folder = input("Which object would you like to work on: ")
while object_folder not in object_folders:
    object_folder = input("ERROR: Please select a valid folder: ")
directory = directory + object_folder + "/"
images = directory + "images/"
vec_file = directory + "vec_files/vec.vec"
info = directory + "info.txt"
non_images = os.path.dirname(os.path.dirname(os.path.dirname(directory))) + "/non_images/"
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
        os.system("opencv_annotation --images=images/  --annotations=" + info)
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
    opencvSupport.create_bg(directory, os.getcwd())
    if use_annotations == "y":
        if images_annotated:
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
