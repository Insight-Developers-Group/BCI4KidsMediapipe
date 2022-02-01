import cv2
import mediapipe
import numpy as np
import csv
import argparse
# Tutorial from: https://techtutorialsx.com/2021/05/19/mediapipe-face-landmarks-estimation/

drawingModule = mediapipe.solutions.drawing_utils
faceModule = mediapipe.solutions.face_mesh

circleDrawingSpec = drawingModule.DrawingSpec(thickness=1, circle_radius=1, color=(0, 255, 0))
lineDrawingSpec = drawingModule.DrawingSpec(thickness=1, color=(0, 255, 0))

def collect(outputfile):
    if (outputfile is None):
        raise TypeError("No output file specified.")
    FIRST_TIME = True
    cap = cv2.VideoCapture(0)
    with faceModule.FaceMesh() as face:
        while cap.isOpened():
            ret, frame = cap.read()
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            results = face.process(image)

            try:
                overall_face = results.multi_face_landmarks

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
                    with open(outputfile, mode='a', newline='') as f:
                        csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        if (FIRST_TIME):
                            csv_writer.writerow(point_headers)
                            FIRST_TIME = False
                        csv_writer.writerow(point_values) 

                    f.close()
            except:
                pass

            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.multi_face_landmarks != None:
                for faceLandmarks in results.multi_face_landmarks:
                    drawingModule.draw_landmarks(image, faceLandmarks, faceModule.FACEMESH_CONTOURS, circleDrawingSpec,
                                                lineDrawingSpec)

            cv2.imshow('Raw Webcam Feed', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break


        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Choose output file"
    )

    parser.add_argument(
        "-o", metavar="path-to-file", type=str, help="Path to output file"
    )

    args = parser.parse_args()
    print(args)
    collect(args.o)