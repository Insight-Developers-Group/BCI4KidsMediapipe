# FacialDFGenerator uses modified code from: https://techtutorialsx.com/2021/05/19/mediapipe-face-landmarks-estimation/
# IrisDFGenerator uses modified code from: https://github.com/Rassibassi/mediapipeDemos

import abc
import argparse
import cv2
import mediapipe as mp
import numpy as np
import pandas as pd

from custom.iris_lm_depth import from_landmarks_to_depth


def add_landmark_to_df(landmark, landmark_idx, df_headers, df_values):
    """Function that adds a landmark to the dataframe"""

    df_headers.append("x{}".format(landmark_idx))
    df_headers.append("y{}".format(landmark_idx))
    df_headers.append("z{}".format(landmark_idx))

    df_values.append(landmark[0])
    df_values.append(landmark[1])
    df_values.append(landmark[2])


def multiple_faces_detected(image):
    """Returns true if multiple faces are in frame, false otherwise"""

    with mp.solutions.face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:

    # Convert the BGR image to RGB and process it with MediaPipe Face Detection.
        results = face_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        # check if there is more then 1 face in frame
        if len(results.detections) > 1:
      
            return True
        
        return False


class DFGeneratorInterface(metaclass=abc.ABCMeta):
    
    @staticmethod
    @abc.abstractmethod
    def generate_df(image):
        """Return a pandas dataframe"""
        raise NotImplementedError




class IrisDFGenerator(DFGeneratorInterface):
    """Facial landmark dataframe generator"""

    MP_FACE_MESH = mp.solutions.face_mesh

    LEFT_EYE_LANDMARKS_ID = np.array([33, 133])
    RIGHT_EYE_LANDMARKS_ID = np.array([362, 263])

    YELLOW = (0, 255, 255)
    GREEN = (0, 255, 0)
    BLUE = (255, 0, 0)
    RED = (0, 0, 255)
    SMALL_CIRCLE_SIZE = 1
    LARGE_CIRCLE_SIZE = 2

    POINTS_IDX = [33, 133, 362, 263, 61, 291, 199]
    POINTS_IDX = list(set(POINTS_IDX))
    POINTS_IDX.sort()



    @staticmethod
    def generate_df(image):
        """Overrides DFGeneratorInterface.generate_df()"""

        return IrisDFGenerator.__get_iris_landmarks(image)



    @staticmethod
    def __get_iris_landmarks(image):
        """Get landmarks for iris and formats dataframe appropriately"""

        landmarks = None
        smooth_left_depth = -1
        smooth_right_depth = -1
        smooth_factor = 0.1

        with IrisDFGenerator.MP_FACE_MESH.FaceMesh(
            static_image_mode=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        ) as face_mesh:
            
            frame_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(frame_rgb)

            image_width, image_height, image_channels = image.shape

            image_size = (image_height, image_width)
            focal_length = image_height
    
            multi_face_landmarks = results.multi_face_landmarks

            # check that only one face is in frame, otherwise throw an exception
            if not multi_face_landmarks:

                raise Exception("IrisDFGenerator: No face detected")

            elif multiple_faces_detected(image):

                raise Exception("IrisDFGenerator: Multiple faces detected")

            face_landmarks = multi_face_landmarks[0]
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
                landmarks[:, IrisDFGenerator.LEFT_EYE_LANDMARKS_ID],
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
                landmarks[:, IrisDFGenerator.RIGHT_EYE_LANDMARKS_ID],
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

            if landmarks is not None:

                landmark_idx = 0
                df_headers = []
                df_values = []

                # add subset of facemesh to dataframe
                for ii in IrisDFGenerator.POINTS_IDX:

                    landmark = (landmarks[0, ii], landmarks[1, ii], landmarks[2, ii])
                    add_landmark_to_df(landmark, landmark_idx, df_headers, df_values)

                    landmark_idx += 1

                # add eye contours to dataframe
                eye_landmarks = np.concatenate(
                    [
                        right_eye_contours,
                        left_eye_contours,
                    ]
                )
                for landmark in eye_landmarks:
                    
                    add_landmark_to_df(landmark, landmark_idx, df_headers, df_values)

                    landmark_idx += 1

                # add iris landmarks to dataframe
                iris_landmarks = np.concatenate(
                    [
                        right_iris_landmarks,
                        left_iris_landmarks,
                    ]
                )
                for landmark in iris_landmarks:

                    add_landmark_to_df(landmark, landmark_idx, df_headers, df_values)

                    landmark_idx += 1

                # create dataframe
                df = pd.DataFrame([df_values], columns = df_headers)

                #IrisDFGenerator.__display_debug_image(landmarks, eye_landmarks, iris_landmarks, image, image_size)

                return df
                



    @staticmethod
    def __display_debug_image(face_landmarks, eye_landmarks, iris_landmarks, image, image_size):
        """Displays image with iris landmarks"""

        if face_landmarks is not None:

            # draw subset of facemesh
            for ii in IrisDFGenerator.POINTS_IDX:
                pos = (np.array(image_size) * face_landmarks[:2, ii]).astype(np.int32)
                image = cv2.circle(image, tuple(pos), IrisDFGenerator.LARGE_CIRCLE_SIZE, IrisDFGenerator.GREEN, -1)

            # draw eye contours
            for landmark in eye_landmarks:
                pos = (np.array(image_size) * landmark[:2]).astype(np.int32)
                image = cv2.circle(image, tuple(pos), IrisDFGenerator.SMALL_CIRCLE_SIZE, IrisDFGenerator.RED, -1)

            # draw iris landmarks
            for landmark in iris_landmarks:
                pos = (np.array(image_size) * landmark[:2]).astype(np.int32)
                image = cv2.circle(image, tuple(pos), IrisDFGenerator.SMALL_CIRCLE_SIZE, IrisDFGenerator.YELLOW, -1)

        cv2.imshow('Debug Image', image)

        cv2.waitKey(0)
        cv2.destroyAllWindows()




class FacialDFGenerator(DFGeneratorInterface):
    """Facial landmark dataframe generator"""

    __faceModule = mp.solutions.face_mesh
    __drawingModule = mp.solutions.drawing_utils

    __circleDrawingSpec = __drawingModule.DrawingSpec(thickness=1, circle_radius=1, color=(0, 255, 0))
    __lineDrawingSpec = __drawingModule.DrawingSpec(thickness=1, color=(0, 255, 0))



    @staticmethod
    def generate_df(image):
        """Overrides DFGeneratorInterface.generate_df()"""
        return FacialDFGenerator.__get_face_Landmarks(image)
        
    

    @staticmethod
    def __get_face_Landmarks(image):
        """Get landmarks for face and format dataframe appropriately"""

        with FacialDFGenerator.__faceModule.FaceMesh(static_image_mode=True) as face:
            
            results = face.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

            # check that only one face is in frame, otherwise throw an exception
            if not results.multi_face_landmarks:

                raise Exception("FacialDFGenerator: No face detected")

            elif multiple_faces_detected(image):

                raise Exception("FacialDFGenerator: Multiple faces detected")

            # add landmarks to dataframe
            for facial_landmarks in results.multi_face_landmarks:
                df_headers = []
                df_values = []

                for i in range(0, 468):
                    
                    landmarks = facial_landmarks.landmark[i]
                    landmark = (landmarks.x, landmarks.y, landmarks.z)
                    add_landmark_to_df(landmark, i, df_headers, df_values)

                # create dataframe
                df = pd.DataFrame([df_values], columns = df_headers)
    
                #FacialDFGenerator.__display_debug_image(results.multi_face_landmarks, image)

                return df



    @staticmethod
    def __display_debug_image(landmarks, image):
        """Displays image with facial landmarks"""
        
        if landmarks != None:
            for faceLandmarks in landmarks:
                FacialDFGenerator.__drawingModule.draw_landmarks(image, faceLandmarks, FacialDFGenerator.__faceModule.FACEMESH_CONTOURS, 
                                            FacialDFGenerator.__circleDrawingSpec, FacialDFGenerator.__lineDrawingSpec)
        cv2.imshow('Debug Image', image)

        cv2.waitKey(0)
        cv2.destroyAllWindows()
