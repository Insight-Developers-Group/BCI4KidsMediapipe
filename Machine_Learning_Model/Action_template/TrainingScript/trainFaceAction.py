import argparse
import cv2
import numpy as np
import os
from matplotlib import pyplot as plt
import mediapipe as mp


drawingModule = mp.solutions.drawing_utils
faceModule = mp.solutions.face_mesh

circleDrawingSpec = drawingModule.DrawingSpec(thickness=1, circle_radius=1, color=(0, 255, 0))
lineDrawingSpec = drawingModule.DrawingSpec(thickness=1, color=(0, 255, 0))

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

    YELLOW = (0, 255, 255)
    GREEN = (0, 255, 0)
    BLUE = (255, 0, 0)
    RED = (0, 0, 255)
    SMALL_CIRCLE_SIZE = 1
    LARGE_CIRCLE_SIZE = 2
    count=0

    cap = cv2.VideoCapture(0)
    with mp_face_mesh.FaceMesh() as face:
        for action in actions:
            # Loop through sequences aka videos
            for sequence in range(no_sequences):
                while cap.isOpened():
                    count = count + 1
                    print(count)
                    if count == sequence_length:
                        count = 0
                        break
                    ret, frame = cap.read()
                    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                    results = face.process(image)
                    point_values = []
                    print(point_values)
                    try:

                        for facial_landmarks in results.multi_face_landmarks:
                            

                            for i in range(0, 468):
                                
                                pt1 = facial_landmarks.landmark[i]
                                point_values.append(pt1.x)
                                point_values.append(pt1.y)
                                point_values.append(pt1.z)

                           
                    except:
                        print("exception Occured")
                        pass
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                    if results.multi_face_landmarks != None:
                        for faceLandmarks in results.multi_face_landmarks:
                            drawingModule.draw_landmarks(image, faceLandmarks, faceModule.FACEMESH_CONTOURS, circleDrawingSpec,
                                                        lineDrawingSpec)

                    # NEW Apply wait logic
                    if count == 1:
                        cv2.putText(image, 'STARTING COLLECTION: Get in position', (120, 200),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 4, cv2.LINE_AA)
                        cv2.putText(image, 'Get in Position for {} Video Number {}'.format(action, sequence), (15, 12),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
                        # Show to screen
                        cv2.imshow('Raw Webcam Feed', image)
                        cv2.waitKey(2000)
                    else:
                        cv2.putText(image, 'Collecting frames for {} Video Number {}'.format(action, sequence), (15, 12),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
                        print("new image should be here...")
                        cv2.imshow('Raw Webcam Feed', image)
                        if cv2.waitKey(10) & 0xFF == ord('q'):
                            break

                        keypoints = np.array(point_values)
                        print(keypoints)
                        npy_path = os.path.join(DATA_PATH, action, str(sequence), str(count))
                        np.save(npy_path, keypoints)

                    
        print("complete")
        cv2.destroyAllWindows()


    


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
        "-seqLen", metavar="sequenceLength", type=str, help="How long each sequence action is in frames"

    )


    args = parser.parse_args()
    print(args)
    main( args.o, args.s1, args.s2, args.seqNo, args.seqLen)
