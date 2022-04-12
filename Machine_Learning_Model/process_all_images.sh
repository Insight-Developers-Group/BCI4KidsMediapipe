#!/bin/bash

for filename in "$1"/*; do
	echo $filename
    python pic_to_facemesh.py -i $filename -o $2
done 
