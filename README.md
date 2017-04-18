# ImageProcessing
It's me, learning OpenCV, watch me do it, for free

# What does it do?
It creates new folders for every object you want to train a cascade classifier for. It does NOT supply the sample images (that to come later)

# What do I have to do to use this?
Clone the repo. There are a few shell commands you can run to do things
*If you want to create a new object (and in essence train a new classifier), just run "new.sh". It'll create a subfolder for you automatically with this structure
*If you want to finally train the classifier, just run "run.sh". It'll ask you a bunch of questions in this order
  1. If you want to rename your images.
    *A lot of the time when you download images from somewhere, it's a garbage file name. This will make them all uniform, and can handle up to 10000 (0 to 9999) images in your "images" folder.
  2. If you need to annotate your images
    *This is only necessary if you have more than one positive image sample.
    *_(future)_ Automatically checks whether this is true or not
  3. If you don't want to annotate your images, it asks whether you already have done it.
  4. If you want to use annotated images for analysis, or if you want OpenCV to create samples for you (typically only if you have one positive sample)
  5. If you want to train the classifier. If you already have a trained classifier, this hefty computational portion of the code can be skipped.
  6. If you already have a trained classifier if you don't want to train the classifier, which leads to
  7. If you want to use the classifier on a set of images.
