#!/usr/bin/env bash

read -p 'What is the object you are looking to detect: ' varObject

cd objects
mkdir $varObject
cd $varObject
mkdir images
mkdir negative_images
mkdir classifier
mkdir vec_files
touch bg.txt
touch info.txt