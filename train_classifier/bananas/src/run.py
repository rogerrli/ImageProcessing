import os
import opencvSupport


rename = input("Do you need to rename image files (Y/N): ").lower()
validInput = False
while not validInput:
    if rename == "y":
        prefix = input("What is the prefix for your files: ")
        opencvSupport.rename(prefix, "images/")
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
        info = input("Where do you want your txt file to save to (e.g. 'info.txt'): ")
        os.system("opencv_annotation --images=images/ --annotations=" + info)
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
    if use_annotations == "y":
        if images_annotated:
            info = input("Where is your annotations located? (e.g. 'info.txt'): ")
            os.system("opencv_createsamples -info " + info + " -vec vec_files/vec.vec")
        else:
            print("ERROR: You do not have any annotated image files")
            use_annotations = "n"
        validInput = True
    elif use_annotations == "n":
        opencvSupport.create_vec("images/")
        validInput = True
    else:
        use_annotations = input("ERROR: Please use Y/N to indicate whether to use annotated images: ")

train_classifier = input("Do you want to train the classifier (Y/N): ").lower()
validInput = False
classifer_trained = False
while not validInput:
    if train_classifier == "y":
        os.system("opencv_traincascade -data classifier/ -vec ./vec_files/vec.vec -bg bg.txt -numStages 12 -minHitRate 0.999 -maxFalseAlarmRate 0.5 -numNeg 3380 -numPos 1500")
        validInput = True
        classifer_trained = True
    elif train_classifier == "n":
        validInput = True
        have_classifier_trained = input("Do you have a trained classifier (Y/N): ")
        nested_validInput = False
        while not nested_validInput:
            if have_classifier_trained == "y":
                nested_validInput = True
                classifer_trained = True
            elif have_classifier_trained == "n":
                nested_validInput = True
            else:
                have_classifier_trained = input("ERROR: Please use Y/N to indicate whether you have a trained classifier: ")
    else:
        rename = input("ERROR: Please use Y/N to indicate whether to rename the images: ")

#if classifer_trained:
