#!/usr/bin/env bash

read -p 'What is the object you are looking to detect: ' varObject

mkdir $varObject
cd $varObject
mkdir images
mkdir non_images
mkdir classifier
mkdir vec_files
touch bg.txt
touch info.txt