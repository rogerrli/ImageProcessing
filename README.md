# ImageProcessing
It's me, learning OpenCV, watch me do it, for free

# What does it do?
It creates new folders for every object you want to train a cascade classifier for. It does NOT supply the sample images (that to come later)
> Here is the folder structure it must follow

    .
    ├──objects
    │   ├──"object you want to identify"
    │   │   ├──images
    │   │   │   ├──object0000.jpg
    │   │   │   ├──...
    │   │   │   └──object9999.jpg
    │   │   ├──vec_files
    │   │   ├──classifier
    │   │   ├──bg.txt
    │   │   └──info.txt
    │   ├──"another object you want to identify"
    │   └──"finally another object you want to identify"
    ├──src
    │   ├──run.py
    │   └──opencvsupport.py
    ├──non_images
    │   ├──non_image0000.jpg
    │   ├──non_image0001.jpg
    │   ├──...
    │   └──non_image9999.jpg
    ├──new.sh
    ├──run.sh
    └──README.md
    
> Once you run "run.sh" your object folders should populate like so

    .
    ├──objects
    │   ├──"object you want to identify"
    │   │   ├──images
    │   │   │   ├──object0000.jpg
    │   │   │   ├──...
    │   │   │   └──object9999.jpg
    │   │   ├──vec_files
    │   │   │   ├──vec1.vec _(only if you don't use annotations will numbered vec files populate)_
    │   │   │   ├──...
    │   │   │   ├──vec9999.vec
    │   │   │   └──vec.vec
    │   │   ├──classifier
    │   │   │   ├──param.xml
    │   │   │   ├──stage0.xml _(the number of stages is dependant on how early the program completes, there may be more or fewer)_
    │   │   │   ├──...
    │   │   │   ├──stage20.xml
    │   │   │   └──cascade.xml _(this is the golden ticket; the file that contains instructions on how to identify objects in images)_
    │   │   ├──bg.txt _(only if you have non_images this file will populate)_
    │   │   └──info.txt _(only if you annotate your images this file will populate)_
    │   ├──"another object you want to identify"
    │   └──"finally another object you want to identify"
    ├──src
    │   ├──run.py
    │   └──opencvsupport.py
    ├──non_images
    │   ├──non_image0000.jpg
    │   ├──non_image0001.jpg
    │   ├──...
    │   └──non_image9999.jpg
    ├──new.sh
    ├──run.sh
    └──README.md
  

# What do I have to do to use this?
Clone the repo. 
You will also need to have OpenCV installed. Check out this great tutorial on how to get it set up [here](http://www.pyimagesearch.com/2016/12/05/macos-install-opencv-3-and-python-3-5/)
There are a few shell commands you can run to do things
* If you want to create a new object (and in essence train a new classifier), just run "new.sh". It'll create a subfolder for you automatically with this structure
* If you want to finally train the classifier, just run "run.sh". It'll ask you a bunch of questions in this order
  1. If you want to rename your images.
    * A lot of the time when you download images from somewhere, it's a garbage file name. This will make them all uniform, and can handle up to 10000 (0 to 9999) images in your "images" folder.
  2. If you need to annotate your images
    * This is only necessary if you have more than one positive image sample.
    * _(future)_ Automatically checks whether this is true or not
  3. If you don't want to annotate your images, it asks whether you already have done it.
  4. If you want to use annotated images for analysis, or if you want OpenCV to create samples for you (typically only if you have one positive sample)
  5. If you want to train the classifier. If you already have a trained classifier, this hefty computational portion of the code can be skipped.
  6. If you already have a trained classifier if you don't want to train the classifier, which leads to
  7. If you want to use the classifier on a set of images.
  
# Future Plans
  * Add a webscraping utility that can grab images for you
    * As a result, will need to change the annotation tool. May have to build it again so that there is an option to delete a photo during the annotation phase that way we can remove any bad images
    * The annotation tool should also display the width/height of the annotated area.
    * The annotation tool could also do post processing to identify which annotated areas are the most similar in size, thereby creating a more uniform classifier. Separate the images into separate folders for each "grouping", then run the training multiple times. As far as I know, there is no way to "re-train" a classifier. 
  * Create a central database for all the cascade.xml files. This should be used so that a community of individuals can use the cascade trainers, with additional informaiton such as success rate and parameters that should be used for identification.
