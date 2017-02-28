import argparse
import os
import os.path
from subprocess import call

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", required=True, help="positive image files directory")
ap.add_argument("-n", "--negative", required=True, help="negative image files directory file")
args = vars(ap.parse_args())

vec_num = 1
image_directory = args["images"]
bg_file = args["negative"]
for positive_image in os.listdir(image_directory):
    if positive_image.endswith(".jpg"):
        vec_name = "vec_files/vec" + str(vec_num) + ".vec"
        full_path = image_directory + positive_image
        full_command = "opencv_createsamples -img " + full_path + " -vec " + vec_name + " -bg " + bg_file + " -num 50"
        os.system(full_command)
        vec_num = vec_num + 1