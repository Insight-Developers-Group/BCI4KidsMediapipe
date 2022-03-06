import argparse

import cv2
import mediapipe as mp
import numpy as np
import csv
import pandas as pd
import pickle


from custom.iris_lm_depth import from_landmarks_to_depth
from videosource import FileSource, WebcamSource

mp_face_mesh = mp.solutions.face_mesh

points_idx = [33, 133, 362, 263]
points_idx = list(set(points_idx))
points_idx.sort()

left_eye_landmarks_id = np.array([33, 133])
right_eye_landmarks_id = np.array([362, 263])

dist_coeff = np.zeros((4, 1))

YELLOW = (0, 255, 255)
GREEN = (0, 255, 0)
BLUE = (255, 0, 0)
RED = (0, 0, 255)
SMALL_CIRCLE_SIZE = 1
LARGE_CIRCLE_SIZE = 2


LEFT_EYE_LANDMARKS_ID = np.array([33, 133])
RIGHT_EYE_LANDMARKS_ID = np.array([362, 263])

POINTS_IDX = [33, 133, 362, 263]
POINTS_IDX = list(set(POINTS_IDX))
POINTS_IDX.sort()

def __compare__iris__landmarks(irisLandmarks, eyeLandmarks, eyeAnchors):
    deltaVals = []
    for i in range(0, len(irisLandmarks), 3):
        x = irisLandmarks[i]
        y = irisLandmarks[i+1]
        z = irisLandmarks[i+2]
        
        #compare to 
        for j in range(0, len(eyeLandmarks), 3):
            x_c = eyeLandmarks[j]
            y_c = eyeLandmarks[j+1]
            z_c = eyeLandmarks[j+2]
            
            deltaVals.append(x - x_c)
            deltaVals.append(y - y_c)
            deltaVals.append(z - z_c)
        
        for j in range(0, len(eyeAnchors), 3):
            x_c = eyeLandmarks[j]
            y_c = eyeLandmarks[j+1]
            z_c = eyeLandmarks[j+2]
            
            deltaVals.append(x - x_c)
            deltaVals.append(y - y_c)
            deltaVals.append(z - z_c)
    return deltaVals


def __add_landmark_to_df(landmark, landmark_idx, df_headers, df_values):
    """Helper function that adds a landmark to the dataframe"""

    df_headers.append("x{}".format(landmark_idx))
    df_headers.append("y{}".format(landmark_idx))
    df_headers.append("z{}".format(landmark_idx))

    df_values.append(landmark[0])
    df_values.append(landmark[1])
    df_values.append(landmark[2])


def __generate_df_headers(num_landmarks, df_headers):
    """Helper function that add headers to df_values"""

    landmark_idx = 0

    while landmark_idx < num_landmarks:
        df_headers.append("x{}".format(landmark_idx))
        df_headers.append("y{}".format(landmark_idx))
        df_headers.append("z{}".format(landmark_idx))

        landmark_idx = landmark_idx + 1


def main(inp):
    FIRST_TIME=True
    if inp is None:
        frame_height, frame_width = (720, 1280)
        source = WebcamSource(width=frame_width, height=frame_height)
    else:
        source = FileSource(inp)
        frame_width, frame_height = (int(i) for i in source.get_image_size())

    image_size = (frame_width, frame_height)

    # pseudo camera internals
    focal_length = frame_width

    landmarks = None
    smooth_left_depth = -1
    smooth_right_depth = -1
    smooth_factor = 0.1
    with open('S:\GitPro\BCI4Kidz\Machine_Learning_Model\Action_template\iris_states_comp_0.pkl', 'rb') as f:
        model = pickle.load(f)
        with mp_face_mesh.FaceMesh(
            static_image_mode=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        ) as face_mesh:

            for idx, (frame, frame_rgb) in enumerate(source):
                results = face_mesh.process(frame_rgb)
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
                        landmarks[:, left_eye_landmarks_id],
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
                        landmarks[:, right_eye_landmarks_id],
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
                    df_headers = []
                    df_values = []

                    # add eye contours to dataframe
                    eye_landmarks = np.concatenate(
                        [
                            right_eye_contours[0:17],
                            left_eye_contours[0:17],
                        ]
                    )
                    for landmark in eye_landmarks:
                    
                        __add_landmark_to_df(landmark, landmark_idx, df_headers, df_values)

                        landmark_idx += 1

                    # add iris landmarks to dataframe
                    iris_landmarks = np.concatenate(
                        [
                            right_iris_landmarks,
                            left_iris_landmarks,
                        ]
                    )
                    for landmark in iris_landmarks:

                        __add_landmark_to_df(landmark, landmark_idx, df_headers, df_values)

                        landmark_idx += 1

                    # add subset of facemesh to dataframe
                    for ii in POINTS_IDX:

                        landmark = (landmarks[0, ii],
                                    landmarks[1, ii], 
                                    landmarks[2, ii])

                        __add_landmark_to_df(landmark, landmark_idx, df_headers, df_values)

                        landmark_idx += 1

                    df_values = __compare__iris__landmarks(df_values[15:30], df_values[81:108], df_values[132:138]) + __compare__iris__landmarks(df_values[0:15], df_values[30:57], df_values[138:])
                    df_headers = []

                    __generate_df_headers(len(df_values) / 3, df_headers)

                    # create dataframe
                    df = pd.DataFrame([df_values], columns = df_headers) 

                    #model prediction
                    body_language_class = model.predict(df)[0]
                    print(body_language_class)

                    # draw subset of facemesh
                    for ii in points_idx:
                        pos = (np.array(image_size) * landmarks[:2, ii]).astype(np.int32)
                        frame = cv2.circle(frame, tuple(pos), LARGE_CIRCLE_SIZE, GREEN, -1)

                    # draw eye contours
                    eye_landmarks = np.concatenate(
                        [
                            right_eye_contours[0:17],
                            left_eye_contours[0:17],
                        ]
                    )
                    for landmark in eye_landmarks:
                        pos = (np.array(image_size) * landmark[:2]).astype(np.int32)
                        frame = cv2.circle(frame, tuple(pos), SMALL_CIRCLE_SIZE, RED, -1)

                    # draw iris landmarks
                    iris_landmarks = np.concatenate(
                        [
                            right_iris_landmarks,
                            left_iris_landmarks,
                        ]
                    )
                    for landmark in iris_landmarks:
                        pos = (np.array(image_size) * landmark[:2]).astype(np.int32)
                        frame = cv2.circle(frame, tuple(pos), SMALL_CIRCLE_SIZE, YELLOW, -1)

                    # write depth values into frame
                    depth_string = "{:.2f}cm, {:.2f}cm".format(
                        smooth_left_depth / 10, smooth_right_depth / 10
                    )
                    frame = cv2.putText(
                        frame,
                        depth_string,
                        (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        GREEN,
                        2,
                        cv2.LINE_AA,
                    )
                    # Display Class
                    cv2.putText(frame, 'CLASS'
                                , (95,12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                    cv2.putText(frame, str(body_language_class)
                                , (90,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                

                source.show(frame)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Choose video file otherwise webcam is used."
    )
    parser.add_argument(
        "-i", metavar="path-to-file", type=str, help="Path to video file"
    )

    args = parser.parse_args()
    main(args.i)
