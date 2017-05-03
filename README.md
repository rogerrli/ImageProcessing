# ImageProcessing
It's me, learning OpenCV. Maybe I'm making it better (I think I am). 

Progress:
* Utilizes a configuration file that YOU will specify where your images are located at, your negatives images, and where you want the classifier to drop into
* Some scripts that query that user for what they want to do with regards to training/using classifiers, instead of the user needing to call the OpenCV commands themself with arguments that are a little finnicky. 
* Rebuilt the opencv_annotation tool to be more flexible in creating the info.txt file, as well as allowing for metrics of the annotation to be obtained.

# What does it do?
It simplifies the process of creating a haar cascade classifier into simple (yes/no) questions, granted you filled in your configuration file correctly. 
> Here is the folder structure where the code lives is expecting to look like

    ├──src
    │   ├──run.py
    │   └──opencvsupport.py
    ├──config.json
    ├──new.sh
    ├──run.sh
    └──README.md
    
> Here is what the config.json is expecting
```json
    {
        "subjects": {
            "faces": {
                "classifier_location": "where you want your classifier folder to drop into",
                "image_path": "where your positive images are locally",
                "negative_images": "where your negative images are locally",
            },
            "another_subject_you_want_to_detect": {
                ...
            }
        }           
    }
```
> This is the "ideal" setup to keep all things where they belong

    .
    ├──subjects
    │   ├──"subject you want to identify"
    │   │   ├──images
    │   │   │   ├──subject0000.jpg
    │   │   │   ├──...
    │   │   │   └──subject9999.jpg
    │   ├──"another subject you want to identify"
    │   │   ├──images
    │   │   │   ├──another_subject0000.jpg
    │   │   │   ├──...
    │   │   │   └──another_subject9999.jpg   
    │   └──"finally another object you want to identify"

> This is the what it will look like after you run through the program

    .
    ├──subjects
    │   ├──"subject you want to identify"
    │   │   ├──images
    │   │   │   ├──object0000.jpg
    │   │   │   ├──...
    │   │   │   └──object9999.jpg
    │   │   ├──vec_files
    │   │   │   ├──vec1.vec (only if you don't use annotations will numbered vec files populate)
    │   │   │   ├──...
    │   │   │   ├──vec9999.vec
    │   │   │   └──vec.vec
    │   │   ├──classifier
    │   │   │   ├──param.xml
    │   │   │   ├──stage0.xml (the number of stages is dependant on how early the program completes, there may be more or fewer)
    │   │   │   ├──...
    │   │   │   ├──stage20.xml
    │   │   │   └──cascade.xml (this is the golden ticket; the file that contains instructions on how to identify objects in images)
    │   │   ├──bg.txt (only if you have non_images this file will populate)
    |   |   ├──anno_complete.p (only if you have not completed annotating all your images)
    │   │   └──info.txt (only if you annotate your images this file will populate)
    │   ├──"another object you want to identify"
    │   └──"finally another object you want to identify"
  

# What do I have to do to use this?
Clone the repo. 
You will also need to have OpenCV installed. Check out this great tutorial on how to get it set up [here](http://www.pyimagesearch.com/2016/12/05/macos-install-opencv-3-and-python-3-5/)
There is one main command for doing all this stuff I made
* If you want to finally train the classifier, just run "./run.sh". It'll ask you a bunch of questions in this order
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
    * ~~As a result, will need to change the annotation tool. May have to build it again so that there is an option to delete a photo during the annotation phase that way we can remove any bad images~~ DONE!
    * The annotation tool should also display the width/height of the annotated area.
    * The annotation tool could also do post processing to identify which annotated areas are the most similar in size, thereby creating a more uniform classifier. Separate the images into separate folders for each "grouping", then run the training multiple times. As far as I know, there is no way to "re-train" a classifier. 
  * Create a central database for all the cascade.xml files. This should be used so that a community of individuals can use the cascade trainers, with additional informaiton such as success rate and parameters that should be used for identification.
