#!/usr/bin/env bash
rm bg.txt
rm vec.vec
rm -rf vec_files
rm -rf classifier
rm info.txt

mkdir vec_files
mkdir classifier
touch bg.txt

python ./src/run.py

say "classifier trained"