import cv2
import mediapipe
import numpy as np
import csv
import argparse

# Tutorial from: https://techtutorialsx.com/2021/05/19/mediapipe-face-landmarks-estimation/
def generate(outputfile, image):
    if (outputfile is None):
        raise TypeError("No output file specified.")
    if (image is None):
        raise TypeError("No input file specified.")    
    drawingModule = mediapipe.solutions.drawing_utils
    faceModule = mediapipe.solutions.face_mesh

    circleDrawingSpec = drawingModule.DrawingSpec(thickness=1, circle_radius=1, color=(0, 255, 0))
    lineDrawingSpec = drawingModule.DrawingSpec(thickness=1, color=(0, 255, 0))

    with faceModule.FaceMesh(static_image_mode=True) as face:
        image = cv2.imread(image)

        results = face.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))


        for facial_landmarks in results.multi_face_landmarks:
            point_headers = []
            point_values = []

            for i in range(0, 468):
                pt1 = facial_landmarks.landmark[i]
                point_headers.append("x{}".format(i))
                point_headers.append("y{}".format(i))
                point_headers.append("z{}".format(i))

                point_values.append(pt1.x)
                point_values.append(pt1.y)
                point_values.append(pt1.z)
            # persist to CSV
            with open(outputfile, 'w') as f:

                # using csv.writer method from CSV package
                write = csv.writer(f)
                write.writerow(point_headers)
                write.writerows([point_values])

        if results.multi_face_landmarks != None:
            for faceLandmarks in results.multi_face_landmarks:
                drawingModule.draw_landmarks(image, faceLandmarks, faceModule.FACEMESH_CONTOURS, circleDrawingSpec,
                                            lineDrawingSpec)

        cv2.imshow('Test image', image)

        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Choose output file and input file "
    )

    parser.add_argument(
        "-o", metavar="path-to-file", type=str, help="Path to output file"
    )
    parser.add_argument(
        "-i", metavar="path-to-image", type=str, help="Path to input image"
    )
    args = parser.parse_args()
    print(args)
    generate(args.o, args.i)