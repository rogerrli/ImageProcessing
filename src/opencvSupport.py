import os
import sys
import glob
import struct
import argparse
import traceback
import cv2
import shutil
import pickle

drawing = False
first_click = True
ix, iy, fx, fy = -1, -1, -1, -1


def annotate_images(images, info):
    global img, static_img, img_stack, drawing, first_click
    info_f = open(info, "w")
    image_dir = images.split("/")
    remove_dir = "/".join(image_dir[:-2]) + "/images_tbd"
    anno_incomplete = "/".join(image_dir[:-2]) + "/anno_complete.p"
    anno_images = []
    # Check to see if the user wants to pick up on their prior annotation, and remove any documents as necessary
    if os.path.isfile(anno_incomplete):
        continue_anno = input("Do you want to pick up where you last left on your annotations? (Y/N): ").lower()
        valid_input = False
        while not valid_input:
            if continue_anno == "y":
                anno_images = pickle.load(open(anno_incomplete, 'rb'))
                valid_input = True
            elif continue_anno == "n":
                os.remove(anno_incomplete)
                valid_input = True
            else:
                continue_anno = input("ERROR: Please choose either Y or N: ")
    for image in os.listdir(images):
        end_program = False
        if not image.startswith('.') and image not in anno_images:
            full_path = images + image
            print(image)
            img = cv2.imread(full_path)
            static_img = cv2.imread(full_path)
            original = cv2.imread(full_path)
            img_stack = [original]
            coordinate_points = []
            cv2.namedWindow('image')
            cv2.setMouseCallback('image', draw_rect, [img_stack])
            while 1:
                cv2.imshow('image', img)
                k = cv2.waitKey(1) & 0xFF
                if k == ord('n'):
                    print('n')
                    info_f.write("/".join(image_dir[-2:]) + image + " " + str(len(coordinate_points)) + " " +
                                 " ".join(str(item) for innerlist in coordinate_points for item in innerlist) + "\n")
                    anno_images.append(image)
                    break
                elif k == ord('c'):
                    print('c')
                    if img is not img_stack[-1]:
                        img_stack.append(img)
                        cv2.rectangle(img, (ix, iy,), (fx, fy), (0, 255, 0), 1)
                        if [ix, iy, fx, fy] not in coordinate_points:
                            coordinate_points.append([ix, iy, fx, fy])
                    print(coordinate_points)
                    print(len(img_stack))
                elif k == ord('d'):
                    print('d')
                    if len(img_stack) > 1:
                        img_stack.pop()
                    if len(coordinate_points) > 0:
                        coordinate_points.pop()
                    img = img_stack[-1]
                    drawing = False
                    first_click = True
                    print(coordinate_points)
                    print(len(img_stack))
                elif k == ord('r'):
                    print('r')
                    if not os.path.isdir(remove_dir):
                        os.makedirs(remove_dir)
                    shutil.copy(full_path, remove_dir + "/" + image)
                    os.remove(full_path)
                    break
                elif k == ord('q'):
                    print('q')
                    end_program = True
                    break
        if end_program:
            break
    # Cleanup
    if not end_program:
        os.remove(anno_incomplete)
    else:
        pickle.dump(anno_images, open(anno_incomplete, 'wb'))
    info_f.close()
    cv2.destroyAllWindows()
    return end_program


def draw_rect(event, x, y, flags, param):
    global ix, iy, fx, fy, drawing, first_click, img, static_img
    if event == cv2.EVENT_LBUTTONUP:
        drawing = not drawing
    elif drawing:
        if event == cv2.EVENT_MOUSEMOVE:
            cv2.rectangle(static_img, (ix, iy), (x, y), (0, 0, 255), 1)
            img = static_img
            static_img = param[0][-1].copy()
            fx, fy = x, y
    elif event == cv2.EVENT_LBUTTONDOWN:
        ix, iy = x, y


def create_bg(directory, non_images):
    bg_file = directory + "bg.txt"
    fo = open(bg_file, "w")
    i = 0
    for _ in os.listdir(non_images):
        if i < 10:
            zeros = "000"
        elif i < 100:
            zeros = "00"
        elif i < 1000:
            zeros = "0"
        else:
            zeros = ""
        fo.write(non_images + "/negative_image" + zeros + str(i) + ".jpg\n")
        i += 1
    fo.close()


def create_vec(image_directory, vec_directory, image_multiplier):
    vec_num = 0
    bg_file = "bg.txt"
    for positive_image in os.listdir(image_directory):
        if positive_image.endswith(".jpg"):
            vec_num += 1
            vec_name = vec_directory + "vec" + str(vec_num) + ".vec"
            full_path = image_directory + positive_image
            full_command = "opencv_createsamples -img " + full_path + " -vec " + vec_name + " -bg " + bg_file + " -num " + image_multiplier
            os.system(full_command)
    if vec_num > 1:
        merge_vec_files(vec_directory, vec_directory + "vec.vec")
    else:
        os.rename(vec_name, vec_directory + ".vec")


def detect_subject(image_directory, classifier):
    for image_file in os.listdir(image_directory):
        if image_file != ".DS_Store":
            full_path = image_directory + image_file
            image = cv2.imread(full_path)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            detector = cv2.CascadeClassifier(classifier)
            rects = detector.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(75, 75))
            for (i, (x, y, w, h)) in enumerate(rects):
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(image, "#{}".format(i + 1), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2)
            cv2.imshow("Subject", image)
            cv2.waitKey(0)


def num_images(image_directory):
    output = 0
    for image_file in os.listdir(image_directory):
        if image_file != ".DS_Store":
            output += 1
    return output


def rename(prefix, folder):
    index = 0
    for file in os.listdir(folder):
        if file != ".DS_Store":
            numberstring = str(index)
            if len(numberstring) == 1:
                numberstring = "000" + numberstring
            elif len(numberstring) == 2:
                numberstring = "00" + numberstring
            elif len(numberstring) == 3:
                numberstring = "0" + numberstring
            new_name = os.path.join(folder, prefix+numberstring+'.jpg')
            os.rename(os.path.join(folder, file), new_name)
            resize(new_name)
            index += 1


def resize(directory):
    image = cv2.imread(directory)
    print(directory)
    (height, width) = image.shape[:2]
    if height > width:
        r = 750.0 / height
        dim = (int(width * r), 750)
    else:
        r = 750.0 / width
        dim = (750, int(height * r))
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    cv2.imwrite(directory, resized)



###############################################################################
# Copyright (c) 2014, Blake Wulfe
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
###############################################################################

"""
File: mergevec.py
Author: blake.w.wulfe@gmail.com
Date: 6/13/2014
File Description:

    This file contains a function that merges .vec files called "merge_vec_files".
    I made it as a replacement for mergevec.cpp (created by Naotoshi Seo.
    See: http://note.sonots.com/SciSoftware/haartraining/mergevec.cpp.html)
    in order to avoid recompiling openCV with mergevec.cpp.

    To use the function:
    (1) Place all .vec files to be merged in a single directory (vec_directory).
    (2) Navigate to this file in your CLI (terminal or cmd) and type "python mergevec.py -v your_vec_directory -o your_output_filename".

        The first argument (-v) is the name of the directory containing the .vec files
        The second argument (-o) is the name of the output file

    To test the output of the function:
    (1) Install openCV.
    (2) Navigate to the output file in your CLI (terminal or cmd).
    (2) Type "opencv_createsamples -w img_width -h img_height -vec output_filename".
        This should show the .vec files in sequence.

"""


def exception_response(e):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
    for line in lines:
        print(line)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', dest='vec_directory')
    parser.add_argument('-o', dest='output_filename')
    args = parser.parse_args()
    return args.vec_directory, args.output_filename


def merge_vec_files(vec_directory, output_vec_file):
    """
    Iterates throught the .vec files in a directory and combines them.

    (1) Iterates through files getting a count of the total images in the .vec files
    (2) checks that the image sizes in all files are the same

    The format of a .vec file is:

    4 bytes denoting number of total images (int)
    4 bytes denoting size of images (int)
    2 bytes denoting min value (short)
    2 bytes denoting max value (short)

    ex: 	6400 0000 4605 0000 0000 0000

        hex		6400 0000  	4605 0000 		0000 		0000
                # images  	size of h * w		min		max
        dec	    	100     	1350			0 		0

    :type vec_directory: string
    :param vec_directory: Name of the directory containing .vec files to be combined.
                Do not end with slash. Ex: '/Users/username/Documents/vec_files'

    :type output_vec_file: string
    :param output_vec_file: Name of aggregate .vec file for output.
        Ex: '/Users/username/Documents/aggregate_vec_file.vec'

    """
    if vec_directory.endswith('/'):
        vec_directory = vec_directory[:-1]
    files = glob.glob('{0}/*.vec'.format(vec_directory))
    if len(files) <= 0:
        print('Vec files to be merged could not be found from directory: {0}'.format(vec_directory))
        sys.exit(1)
    if len(files) == 1:
        print('Only 1 vec file was found in directory: {0}. Cannot merge a single file.'.format(vec_directory))
        sys.exit(1)
    prev_image_size = 0
    try:
        with open(files[0], 'rb') as vecfile:
            content = b''.join((line) for line in vecfile.readlines())
            val = struct.unpack('<iihh', content[:12])
            prev_image_size = val[1]
    except IOError as e:
        print('An IO error occured while processing the file: {0}'.format(f))
        exception_response(e)
    total_num_images = 0
    for f in files:
        try:
            with open(f, 'rb') as vecfile:
                content = b''.join((line) for line in vecfile.readlines())
                val = struct.unpack('<iihh', content[:12])
                num_images = val[0]
                image_size = val[1]
                if image_size != prev_image_size:
                    err_msg = """The image sizes in the .vec files differ. These values must be the same. \n The image size of file {0}: {1}\n
                        The image size of previous files: {0}""".format(f, image_size, prev_image_size)
                    sys.exit(err_msg)

                total_num_images += num_images
        except IOError as e:
            print('An IO error occured while processing the file: {0}'.format(f))
            exception_response(e)
    header = struct.pack('<iihh', total_num_images, image_size, 0, 0)
    try:
        with open(output_vec_file, 'wb') as outputfile:
            outputfile.write(header)

            for f in files:
                with open(f, 'rb') as vecfile:
                    content = b''.join((line) for line in vecfile.readlines())
                    outputfile.write(bytearray(content[12:]))
    except Exception as e:
        exception_response(e)

