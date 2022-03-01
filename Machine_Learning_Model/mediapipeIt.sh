
dir = "mediapipe"
mkdir $dir
for FILE in *;
    do python Generate_Landmarks.py -i $FILE -o $dir/$FILE.mediapipe;
done