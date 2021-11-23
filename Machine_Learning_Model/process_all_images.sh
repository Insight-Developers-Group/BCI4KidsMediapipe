#!/bin/bash

for filename in "$1"/*; do
	echo $filename
    python3 pic_to_facemesh.py -i $filename -o csvs/neutral.csv
done 

# target=$1
# let count=0
# for f in "$target"/*
# do
#     echo $(basename $f)
#     let count=count+1
# done
# echo ""
# echo "Count: $count"