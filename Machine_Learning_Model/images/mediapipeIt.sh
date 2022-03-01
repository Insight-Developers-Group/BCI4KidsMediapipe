mkdir $1/mediapipe
cd $1
for FILE in *;
    do python ../Generate_Landmarks.py -i $FILE -o mediapipe/$FILE.mediapipe;
done