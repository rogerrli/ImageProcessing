#!/usr/bin/env bash

read -p 'What is the object you are looking to detect: ' varObject

mkdir $varObject
cp -r ./BASE/ ./$varObject/