#!/usr/bin/env python

import asyncio
import base64
import binascii
import io
import numpy
from PIL import Image, UnidentifiedImageError
import websockets
import contextvars

import DFGenerator
import json 

#new imports for dummy server
import pandas as pd
import os
import sys
import numpy as np

folder = contextvars.ContextVar('folder', default="")
face_sq_itr = contextvars.ContextVar('face_sq_itr', default=0)
iris_sq_itr = contextvars.ContextVar('iris_sq_itr', default=0)
iris_itr = contextvars.ContextVar('iris_itr', default=0)
face_itr = contextvars.ContextVar('face_itr', default=0)

DATA_PATH = os.path.join(sys.argv[1])
ACTION_NAME = sys.argv[2] 
SEQUENCE_LENGTH = int(sys.argv[3])
NO_SEQUENCES = int(sys.argv[4])

FACE = "FACE"
IRIS = "IRIS"

for sequence in range(NO_SEQUENCES):
    try: 
        os.makedirs(os.path.join(DATA_PATH, IRIS, ACTION_NAME, str(sequence)))
        os.makedirs(os.path.join(DATA_PATH, FACE, ACTION_NAME, str(sequence)))
    except:
        pass
print('folders Created')



# Error Strings
invalid_state_exception = "ERROR: Invalid State Exception"
no_face_detected_exception = "ERROR: No Face Detected"
multi_face_detected_exception = "ERROR: Multiple Faces Detected"
invalid_model_type = "ERROR: Invalid Model Type"

df_generator_exception = "ERROR: DF Generator Failed"
state_generator_exception = "ERROR: State Generator Failed"
answer_generator_exception = "ERROR: Answer Generator Failed"


def get_landmarks(image_data):
    if (image_data[0] == FACE):

        try: 
            df = DFGenerator.FacialDFGenerator.generate_df(image_data[1])
        
        except DFGenerator.NoFaceDetectedException:
            return no_face_detected_exception
        
        except DFGenerator.MultiFaceDetectedException:
            return multi_face_detected_exception

        except Exception:
            return df_generator_exception


    elif (image_data[0] == IRIS):
        
        try:
            df = DFGenerator.IrisDFGenerator.generate_df(image_data[1])

        except DFGenerator.NoFaceDetectedException:
            return no_face_detected_exception
        
        except DFGenerator.MultiFaceDetectedException:
            return multi_face_detected_exception

        except Exception:
            return df_generator_exception

    else:
        print("how did this even happen?")
        raise Exception


    return df

#function to convert an image that is already in a Pillow image format (jpg) to cv2
#https://stackoverflow.com/questions/14134892/convert-image-from-pil-to-opencv-format
def convert_image(im):
    open_cv_image = numpy.array(im)
    open_cv_image = open_cv_image[:,:,::-1].copy()
    return open_cv_image

#async function to recieve an image or images through a websocket
#https://stackoverflow.com/questions/26070547/decoding-base64-from-post-to-use-in-pil
#takes in the message from the websocket and then strips out all the unneeded header information so we just have the base64 encoded data
#this data can then be converted into a PIL image and then dealt with as needed
async def recv_image(websocket):

    async for message in websocket:
        #take in message as a json and then get the data from it according to its tags
        try:
            as_json = json.loads(message)
        except json.JSONDecodeError as ex:
            print("There was an error with the JSON data from the frontend")
            pass
        
        msg_mode = as_json["mode"]
        if (msg_mode == "face"):
            mode = FACE
        elif (msg_mode == "eye"):
            mode = IRIS
        #safe default if there is a problem with the mode type
        else:
            print("Something is wrong with the recieved mode type, defaulting to face tracking.")
            mode = FACE

        img_data = as_json["image"]

        temp = img_data.split(",")
        for i in temp:
            if(i != "data:image/jpeg;base64"):
                try:
                    ima = Image.open(io.BytesIO(base64.b64decode(i)))

                    #convert the image to cv2 for use in the state generators
                    converted = convert_image(ima)
                    try:
                        lm = get_landmarks((mode, converted))
                    except:
                        print("exception occured.")
                        continue
                    
                    if(lm.empty==False):
                        print(mode)
                        if(mode == FACE):
                            print(face_sq_itr.get())
                            if (face_sq_itr.get() >= NO_SEQUENCES):
                                print('Sequences Finished')
                                quit()
                            else:
                                # print('Adding frame')
                                face_itr.set(face_itr.get()+1)
                                if (face_itr.get() == SEQUENCE_LENGTH):
                                    face_sq_itr.set(face_sq_itr.get()+1)
                                    face_itr.set(0)
                                keypoints = np.array(lm)[0]
                                npy_path = os.path.join(DATA_PATH, FACE, ACTION_NAME, str(face_sq_itr.get()), str(face_itr.get()))
                                np.save(npy_path, keypoints)
                        elif(mode == IRIS):
                            print(iris_sq_itr.get())
                            if (iris_sq_itr.get() >= NO_SEQUENCES):
                                print('Sequences Finished')
                                quit()
                            else:
                                iris_itr.set(iris_itr.get()+1)
                                #go to the next folder
                                if (iris_itr.get() == SEQUENCE_LENGTH):
                                    iris_sq_itr.set(iris_sq_itr.get()+1)
                                    iris_itr.set(0)
                                keypoints = np.array(lm)[0]
                                npy_path = os.path.join(DATA_PATH, IRIS, ACTION_NAME, str(iris_sq_itr.get()), str(iris_itr.get()))
                                np.save(npy_path, keypoints)

                    ##############################################################

                #except the exceptions that Pillow will typically throw if something is wrong with the image when opening it
                except (UnidentifiedImageError, ValueError, TypeError) as ex:
                    print("There was an error with that image and it could not be decoded and opened as an image")
                    print(ex)
                    #at this point we could call for the program to quit or return an error here, depends whats appropriate
                
                #except the error from decoding the base64 data
                except (binascii.Error) as decod:
                    print("There was an error decoding the image data in base64")
                    print(decod)



async def start_websocket():
    async with websockets.serve(recv_image, "localhost", 8765):
        await asyncio.Future()  # run forever

def main():
    folder.set(sys.argv[1])
    asyncio.run(start_websocket())

if __name__ == "__main__":
    main()

