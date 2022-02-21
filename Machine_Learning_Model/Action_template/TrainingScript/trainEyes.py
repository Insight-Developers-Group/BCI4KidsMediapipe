import argparse
import cv2
import numpy as np
import os
from matplotlib import pyplot as plt
import mediapipe as mp

import sys
sys.path.insert(0, '../')
from videosource import WebcamSource
from custom.iris_lm_depth import from_landmarks_to_depth

def __add_landmark_to_df(landmark, landmark_idx, df_headers, df_values):
    """Helper function that adds a landmark to the dataframe"""

    df_headers.append("x{}".format(landmark_idx))
    df_headers.append("y{}".format(landmark_idx))
    df_headers.append("z{}".format(landmark_idx))

    df_values.append(landmark[0])
    df_values.append(landmark[1])
    df_values.append(landmark[2])

def main(dirname, firstState, secondState, no_sequences, sequence_length):
    no_sequences = int(no_sequences)
    sequence_length = int(sequence_length)
    if (dirname is None):
        raise TypeError("No output dir specified.")
    if firstState is None:
        raise TypeError("First State Not Specified")
    if (secondState is None):
        raise TypeError("Second State Note Specified")
    if (no_sequences is None or no_sequences < 1):
        raise TypeError("Video Number is none or less than 1")
    if (sequence_length is None or sequence_length < 1):
        raise TypeError("Sequence Length is none or less than 1")
    # Path for exported data, numpy arrays
    DATA_PATH = os.path.join(dirname) 

    # Actions that we try to detect
    actions = np.array([firstState, secondState ])

    ## Create the Appropriate Directories
    for action in actions: 
        for sequence in range(no_sequences):
            try: 
                os.makedirs(os.path.join(DATA_PATH, action, str(sequence)))
            except:
                pass
    
    mp_face_mesh = mp.solutions.face_mesh

    left_eye_landmarks_id = np.array([33, 133])
    right_eye_landmarks_id = np.array([362, 263])

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
    FIRST_TIME = True
    frame_height, frame_width = (720, 1280)
    source = WebcamSource(width=frame_width, height=frame_height)
    image_size = (frame_width, frame_height)
    count = 0

    # pseudo camera internals
    focal_length = frame_width

    landmarks = None
    smooth_left_depth = -1
    smooth_right_depth = -1
    smooth_factor = 0.1

    with mp_face_mesh.FaceMesh(
        static_image_mode=False,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    ) as face_mesh:
        for action in actions:
            # Loop through sequences aka videos
            for sequence in range(no_sequences):
                # Loop through video length aka sequence length
                for idx, (frame, frame_rgb) in enumerate(source):
                    # only go sequence_length times
                    count = count + 1
                    print(count)
                    if count == sequence_length:
                        count = 0
                        break
#                     for idx, (frame, frame_rgb) in enumerate(source):
                    results = face_mesh.process(frame_rgb)
                    multi_face_landmarks = results.multi_face_landmarks

                    if multi_face_landmarks:
                        face_landmarks = results.multi_face_landmarks[0]
                        landmarks = np.array(
                            [(lm.x, lm.y, lm.z)
                             for lm in face_landmarks.landmark]
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

                        # add iris landmarks to dataframe
                        iris_landmarks = np.concatenate(
                            [
                                right_iris_landmarks,
                                left_iris_landmarks,
                            ]
                        )
                        for landmark in iris_landmarks:

                            __add_landmark_to_df(
                                landmark, landmark_idx, df_headers, df_values)

                            landmark_idx += 1

                        for landmark in eye_landmarks:

                            __add_landmark_to_df(
                                landmark, landmark_idx, df_headers, df_values)

                            landmark_idx += 1

                        # add subset of facemesh to dataframe
                        for ii in POINTS_IDX:

                            landmark = (landmarks[0, ii],
                                        landmarks[1, ii], landmarks[2, ii])
                            __add_landmark_to_df(
                                landmark, landmark_idx, df_headers, df_values)

                            landmark_idx += 1

                        # draw subset of facemesh
                        for ii in POINTS_IDX:
                            pos = (np.array(image_size) *
                                   landmarks[:2, ii]).astype(np.int32)
                            frame = cv2.circle(frame, tuple(
                                pos), LARGE_CIRCLE_SIZE, GREEN, -1)

                        # draw eye contours
                        eye_landmarks = np.concatenate(
                            [
                                right_eye_contours[0:17],
                                left_eye_contours[0:17],
                            ]
                        )
                        for landmark in eye_landmarks:
                            pos = (np.array(image_size) *
                                   landmark[:2]).astype(np.int32)
                            frame = cv2.circle(frame, tuple(
                                pos), SMALL_CIRCLE_SIZE, RED, -1)

                        # draw iris landmarks
                        iris_landmarks = np.concatenate(
                            [
                                right_iris_landmarks[0:3],
                                left_iris_landmarks[0:5],
                            ]
                        )
                        for landmark in iris_landmarks:
                            pos = (np.array(image_size) *
                                   landmark[:2]).astype(np.int32)
                            frame = cv2.circle(frame, tuple(
                                pos), SMALL_CIRCLE_SIZE, YELLOW, -1)

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

                     # NEW Apply wait logic
                        if count == 1:
                            cv2.putText(frame, 'STARTING COLLECTION: Get in position', (120, 200),
                                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 4, cv2.LINE_AA)
                            cv2.putText(frame, 'Collecting frames for {} Video Number {}'.format(action, sequence), (15, 12),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
                            # Show to screen
                            source.show(frame)
                            cv2.waitKey(2000)
                        else:
                            cv2.putText(frame, 'Collecting frames for {} Video Number {}'.format(action, sequence), (15, 12),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
                            source.show(frame)

                            keypoints = np.array(df_values)
                            print(keypoints)
                            npy_path = os.path.join(DATA_PATH, action, str(sequence), str(count))
                            np.save(npy_path, keypoints)

    


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Choose video file otherwise webcam is used."
    )
    parser.add_argument(
        "-o", metavar="FolderName", type=str, help="Path to output file"
    )
    parser.add_argument(
        "-s1", metavar="state1", type=str, help="state1name"
    )
    parser.add_argument(
        "-s2", metavar="state2", type=str, help="state2name"
    )
    parser.add_argument(
        "-seqNo", metavar="sequenceNum", type=str, help="Number of sequences of action to capture"

    )
    parser.add_argument(
        "-seqLen", metavar="state2", type=str, help="How long each sequence action is in frames"

    )


    args = parser.parse_args()
    print(args)
    main( args.o, args.s1, args.s2, args.seqNo, args.seqLen)
