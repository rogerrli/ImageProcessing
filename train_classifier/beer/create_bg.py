import os
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", required=True, help="negative image files directory")
args = vars(ap.parse_args())

image_directory = args["images"]
fo = open("bg.txt", "a")
for positive_image in os.listdir(image_directory):
    if positive_image.endswith(".jpg"):
        fo.write(image_directory +  positive_image + "\n")
fo.close()
