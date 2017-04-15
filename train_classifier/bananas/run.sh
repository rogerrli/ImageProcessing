#!/usr/bin/env bash
rm bg.txt
rm -rf vec_files
rm -rf classifier

mkdir vec_files
mkdir classifier
touch bg.txt

python ./src/run.py
