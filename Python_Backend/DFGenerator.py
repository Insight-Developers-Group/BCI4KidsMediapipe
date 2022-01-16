# FacialDFGenerator uses modified code from: https://techtutorialsx.com/2021/05/19/mediapipe-face-landmarks-estimation/
# IrisDFGenerator uses modified code from: https://github.com/Rassibassi/mediapipeDemos

import abc
import argparse
import cv2
import mediapipe as mp
import numpy as np
import pandas as pd

from custom.iris_lm_depth import from_landmarks_to_depth

class DFGeneratorInterface(metaclass=abc.ABCMeta):
    
    @staticmethod
    @abc.abstractmethod
    def generateDF(image):
        """Return a pandas dataframe"""
        raise NotImplementedError


class IrisDFGenerator(DFGeneratorInterface):
    """Facial Landmark Dataframe Generator"""

    __mp_face_mesh = mp.solutions.face_mesh

    __points_idx = [33, 133, 362, 263, 61, 291, 199]

    __left_eye_landmarks_id = np.array([33, 133])
    __right_eye_landmarks_id = np.array([362, 263])

    __dist_coeff = np.zeros((4, 1))


    @staticmethod
    def generateDF(image):
        """Overrides DFGeneratorInterface.generateDF()"""

        IrisDFGenerator.__points_idx = list(set(IrisDFGenerator.__points_idx))
        IrisDFGenerator.__points_idx.sort()

        return IrisDFGenerator.__get_iris_Landmarks(image)


    @staticmethod
    def __get_iris_Landmarks(image):
        """Get landmarks for iris and format dataframe appropriately"""

        landmarks = None
        smooth_left_depth = -1
        smooth_right_depth = -1
        smooth_factor = 0.1

        with IrisDFGenerator.__mp_face_mesh.FaceMesh(
            static_image_mode=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        ) as face_mesh:

            frame = cv2.imread("images/tim.jpg")
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(frame_rgb)

            frame_w, frame_h, frame_c = frame.shape

            image_size = (frame_h, frame_w)
            focal_length = frame_h
    
            multi_face_landmarks = results.multi_face_landmarks

            if multi_face_landmarks:
                face_landmarks = results.multi_face_landmarks[0]
                landmarks = np.array(
                    [(lm.x, lm.y, lm.z) for lm in face_landmarks.landmark]
                )
                landmarks = landmarks.T

                (
                    left_depth,
                    left_iris_size,
                    left_iris_landmarks,
                    left_eye_contours,
                ) = from_landmarks_to_depth(
                    frame_rgb,
                    landmarks[:, IrisDFGenerator.__left_eye_landmarks_id],
                    image_size,
                    is_right_eye=False,
                    focal_length=focal_length,
                )

                (
                    right_depth,
                    right_iris_size,
                    right_iris_landmarks,
                    right_eye_contours,
                ) = from_landmarks_to_depth(
                    frame_rgb,
                    landmarks[:, IrisDFGenerator.__right_eye_landmarks_id],
                    image_size,
                    is_right_eye=True,
                    focal_length=focal_length,
                )

                if smooth_right_depth < 0:
                    smooth_right_depth = right_depth
                else:
                    smooth_right_depth = (
                        smooth_right_depth * (1 - smooth_factor)
                        + right_depth * smooth_factor
                    )

                if smooth_left_depth < 0:
                        smooth_left_depth = left_depth
                else:
                    smooth_left_depth = (
                        smooth_left_depth * (1 - smooth_factor)
                        + left_depth * smooth_factor
                    )

                print(
                    f"depth in cm: {smooth_left_depth / 10:.2f}, {smooth_right_depth / 10:.2f}"
                )
                print(f"size: {left_iris_size:.2f}, {right_iris_size:.2f}")


                if landmarks is not None:

                    landmark_idx = 0
                    point_headers = []
                    point_values = []

                    # add subset of facemesh to dataframe
                    for ii in IrisDFGenerator.__points_idx:

                        landmark = (landmarks[0, ii], landmarks[1, ii], landmarks[2, ii])
                        IrisDFGenerator.__addLandmarkToDataframe(landmark, landmark_idx, point_headers, point_values)

                        landmark_idx += 1

                    # add eye contours to dataframe
                    eye_landmarks = np.concatenate(
                        [
                            right_eye_contours,
                            left_eye_contours,
                        ]
                    )
                    for landmark in eye_landmarks:
                    
                        IrisDFGenerator.__addLandmarkToDataframe(landmark, landmark_idx, point_headers, point_values)

                        landmark_idx += 1

                    # add iris landmarks to dataframe
                    iris_landmarks = np.concatenate(
                        [
                            right_iris_landmarks,
                            left_iris_landmarks,
                        ]
                    )
                    for landmark in iris_landmarks:

                        IrisDFGenerator.__addLandmarkToDataframe(landmark, landmark_idx, point_headers, point_values)

                        landmark_idx += 1

                    # create dataframe
                    df = pd.DataFrame([point_values], columns = point_headers)
                    print(df)
            
                IrisDFGenerator.__displayDebugImage(landmarks, eye_landmarks, iris_landmarks, frame, image_size)



    @staticmethod
    def __displayDebugImage(face_landmarks, eye_landmarks, iris_landmarks, image, image_size):
        """Overrides DFGeneratorInterface.__displayDebugImage()"""
        
        YELLOW = (0, 255, 255)
        GREEN = (0, 255, 0)
        BLUE = (255, 0, 0)
        RED = (0, 0, 255)
        SMALL_CIRCLE_SIZE = 1
        LARGE_CIRCLE_SIZE = 2

        if face_landmarks is not None:

            # draw subset of facemesh
            for ii in IrisDFGenerator.__points_idx:
                pos = (np.array(image_size) * face_landmarks[:2, ii]).astype(np.int32)
                image = cv2.circle(image, tuple(pos), LARGE_CIRCLE_SIZE, GREEN, -1)

            # draw eye contours
            for landmark in eye_landmarks:
                pos = (np.array(image_size) * landmark[:2]).astype(np.int32)
                image = cv2.circle(image, tuple(pos), SMALL_CIRCLE_SIZE, RED, -1)

            # draw iris landmarks
            for landmark in iris_landmarks:
                pos = (np.array(image_size) * landmark[:2]).astype(np.int32)
                image = cv2.circle(image, tuple(pos), SMALL_CIRCLE_SIZE, YELLOW, -1)

        cv2.imshow('Debug Image', image)

        cv2.waitKey(0)
        cv2.destroyAllWindows()



    @staticmethod
    def __addLandmarkToDataframe(landmark, landmark_idx, point_headers, point_values):
        point_headers.append("x{}".format(landmark_idx))
        point_headers.append("y{}".format(landmark_idx))
        point_headers.append("z{}".format(landmark_idx))

        point_values.append(landmark[0])
        point_values.append(landmark[1])
        point_values.append(landmark[2])



class FacialDFGenerator(DFGeneratorInterface):
    """Facial Landmark Dataframe Generator"""

    __faceModule = mp.solutions.face_mesh
    __drawingModule = mp.solutions.drawing_utils

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
            
            # todo: take in proper image format and convert cv2 retval
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
        cv2.imshow('Debug Image', image)

        cv2.waitKey(0)
        cv2.destroyAllWindows()


IrisDFGenerator.generateDF(2)
