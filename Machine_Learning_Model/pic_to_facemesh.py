import cv2
import mediapipe
import numpy as np
import csv

import sys
import getopt

def pic_to_mesh(imagepath):

    faceModule = mediapipe.solutions.face_mesh
    with faceModule.FaceMesh(static_image_mode=True) as face:
        image = cv2.imread(imagepath)
        results = face.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        point_values = []
        for facial_landmarks in results.multi_face_landmarks:
            point_values = []

            for i in range(0, 468):
                pt1 = facial_landmarks.landmark[i]
                point_values.append(pt1.x)
                point_values.append(pt1.y)
                point_values.append(pt1.z)
        return point_values


def persist_row_to_csv(point_values, output_file):
    # persist to CSV
    with open(output_file, 'a') as f:
        # using csv.writer method from CSV package
        write = csv.writer(f, lineterminator='\r\n')
        write.writerow(point_values)



def main(argv):
    inputfile = ''
    outputfile = 'image_mesh.csv'
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('pic_to_facemesh.py -i <inputimagepath> -o <outputcsvpath>')
            sys.exit()
        elif opt in ("-i", "--inputimage"):
            inputfile = arg
        elif opt in ("-o", "--outputcsv"):
            outputfile = arg

    if inputfile == '':
        raise ValueError('Input Image must be provided.')

    persist_row_to_csv(pic_to_mesh(inputfile), outputfile)
    print("Image Facemesh of {} has been persisted to file: {}!".format(inputfile, outputfile))


if __name__ == "__main__":
    main(sys.argv[1:])
