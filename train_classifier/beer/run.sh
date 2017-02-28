rm bg.txt
rm vec.vec
rm -rf vec_files
rm -rf classifier

mkdir vec_files
mkdir classifier
touch bg.txt

python create_bg.py -i non_images/
say "background file created"

python create_vec_files.py -i images/ -n bg.txt
say "vector files created"

python mergevec.py -v vec_files/ -o vec.vec
say "vector files merged"

opencv_traincascade -data classifier/ -vec vec.vec -bg bg.txt -numStages 12 -minHitRate 0.999 -maxFalseAlarmRate 0.5 -mode ALL -numNeg 3380 -numPos 25000
say "classifier trained"