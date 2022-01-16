# Tutorial from facial landmarks: https://techtutorialsx.com/2021/05/19/mediapipe-face-landmarks-estimation/

import abc
import cv2
import mediapipe
import numpy as np
import pandas as pd

class DFGeneratorInterface(metaclass=abc.ABCMeta):
    
    @staticmethod
    @abc.abstractmethod
    def generateDF(image):
        """Return a pandas dataframe"""
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def __displayDebugImage(landmarks, image):
        """Displays image with landmarks"""
        raise NotImplementedError

    


class IrisDFGenerator(DFGeneratorInterface):
    """Facial Landmark Dataframe Generator"""


    @staticmethod
    def generateDF(image):
        """Overrides DFGeneratorInterface.generateDF()"""
        IrisDFGenerator.__get_iris_Landmarks(image)
        pass

    @staticmethod
    def __get_iris_Landmarks(image):
        """Get landmarks for iris and format dataframe appropriately"""
        pass

    @staticmethod
    def __displayDebugImage(landmarks, image):
        """Overrides DFGeneratorInterface.__displayDebugImage()"""
        raise NotImplementedError


class FacialDFGenerator(DFGeneratorInterface):
    """Facial Landmark Dataframe Generator"""

    __faceModule = mediapipe.solutions.face_mesh
    __drawingModule = mediapipe.solutions.drawing_utils

    __circleDrawingSpec = __drawingModule.DrawingSpec(thickness=1, circle_radius=1, color=(0, 255, 0))
    __lineDrawingSpec = __drawingModule.DrawingSpec(thickness=1, color=(0, 255, 0))


    @staticmethod
    def generateDF(image):
        """Overrides DFGeneratorInterface.generateDF()"""
        FacialDFGenerator.__get_face_Landmarks(image)
        pass
    
    @staticmethod
    def __get_face_Landmarks(image):
        """Get landmarks for face and format dataframe appropriately"""

        with FacialDFGenerator.__faceModule.FaceMesh(static_image_mode=True) as face:
            image = cv2.imread("images/tim.jpg")

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

                # create dataframe
                df = pd.DataFrame([point_values], columns = point_headers)
                print(df)
    
            FacialDFGenerator.__displayDebugImage(results.multi_face_landmarks, image)

            return df

    @staticmethod
    def __displayDebugImage(landmarks, image):
        """Overrides DFGeneratorInterface.__displayDebugImage()"""
        
        if landmarks != None:
            for faceLandmarks in landmarks:
                FacialDFGenerator.__drawingModule.draw_landmarks(image, faceLandmarks, FacialDFGenerator.__faceModule.FACEMESH_CONTOURS, 
                                            FacialDFGenerator.__circleDrawingSpec, FacialDFGenerator.__lineDrawingSpec)
        cv2.imshow('Debug image', image)

        cv2.waitKey(0)
        cv2.destroyAllWindows()


FacialDFGenerator.generateDF(2)
