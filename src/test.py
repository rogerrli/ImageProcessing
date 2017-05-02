import opencvSupport

images = "/Users/Roger/Desktop/coding/objects/temp/images/"
info = "/Users/Roger/Desktop/coding/objects/temp/info.txt"
open(info, "w+")
opencvSupport.annotate_images(images, info)