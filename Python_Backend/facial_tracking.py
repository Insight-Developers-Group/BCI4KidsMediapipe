import cv2
import mediapipe
import numpy as np
import pandas as pd
import csv

# Tutorial from: https://techtutorialsx.com/2021/05/19/mediapipe-face-landmarks-estimation/

__faceModule = mediapipe.solutions.face_mesh
__drawingModule = mediapipe.solutions.drawing_utils

__circleDrawingSpec = __drawingModule.DrawingSpec(thickness=1, circle_radius=1, color=(0, 255, 0))
__lineDrawingSpec = __drawingModule.DrawingSpec(thickness=1, color=(0, 255, 0))


def __displayDebugImage(landmarks, image):
    """Displays image with landmarks"""
        
    if landmarks != None:
        for faceLandmarks in landmarks:
            __drawingModule.draw_landmarks(image, faceLandmarks, __faceModule.FACEMESH_CONTOURS, __circleDrawingSpec,
                                        __lineDrawingSpec)
    cv2.imshow('Test image', image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

with __faceModule.FaceMesh(static_image_mode=True) as face:
    image = cv2.imread("images/tim.jpg")

    results = face.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))


    multi_face_landmarks = results.multi_face_landmarks

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

        # create dataframe
        df = pd.DataFrame([point_values], columns = point_headers)
    

    __displayDebugImage(results.multi_face_landmarks, image)


