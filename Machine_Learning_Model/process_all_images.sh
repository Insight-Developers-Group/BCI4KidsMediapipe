#!/bin/bash
for filename in \\images\\smiling\\*; do
	echo $filename
    python pic_to_facemesh.py -i $filename -o csvs/smile1.csv
done 