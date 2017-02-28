import os
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prefix", required=True, help="prefix for the files")
ap.add_argument("-f", "--folder", required=True, help="path to directory with files to be renamed")
args = vars(ap.parse_args())

folder = args["folder"]
prefix = args["prefix"]
directory = os.getcwd() + "/" + folder
files = os.listdir(directory)
index = 1

for file in files:
    numberstring = str(index)
    if len(numberstring) == 1:
        numberstring = "000" + numberstring
    elif len(numberstring) == 2:
        numberstring = "00" + numberstring
    elif len(numberstring) == 3:
        numberstring = "0" + numberstring
    os.rename(os.path.join(directory, file), os.path.join(directory, prefix+numberstring+'.jpg'))
    index = index + 1

