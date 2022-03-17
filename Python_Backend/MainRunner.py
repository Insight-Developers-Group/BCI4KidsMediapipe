#!/usr/bin/env python

import asyncio
import base64
import binascii
import io
import numpy
from PIL import Image, UnidentifiedImageError
import websockets
import contextvars
import traceback

import numpy as np

import AnswerGenerator
import DFGenerator
from StateGenerator import StateGenerator
import json 
from ActionBasedStateGenerator import ActionBasedStateGenerator


# Initiate State Generator with the appropriate models
MAX_SIZE_IRIS_DATA_QUEUE = 48
facial_state_generator = StateGenerator("../Machine_Learning_Model/facial_model.pkl", "FACE")
iris_state_generator = ActionBasedStateGenerator("../Machine_Learning_Model/Action_template/3_state_test.h5", MAX_SIZE_IRIS_DATA_QUEUE)

#Initiate actionList to send to 

# Two types of Generators
facial_answer_generator = AnswerGenerator.FacialAnswerGenerator()
iris_answer_generator = AnswerGenerator.IrisAnswerGenerator()

FACE = "FACE"
IRIS = "IRIS"

# Error Strings
invalid_state_exception = "ERROR: Invalid State Exception"
no_face_detected_exception = "ERROR: No Face Detected"
multi_face_detected_exception = "ERROR: Multiple Faces Detected"
invalid_model_type = "ERROR: Invalid Model Type"

df_generator_exception = "ERROR: DF Generator Failed"
state_generator_exception = "ERROR: State Generator Failed"
answer_generator_exception = "ERROR: Answer Generator Failed"

# Member Variables
current_answer = contextvars.ContextVar('current_answer', default=AnswerGenerator.Answer.UNDEFINED)
iris_data_queue = contextvars.ContextVar('iris_data_queue', default=[])

def compareIrisLandmarks(irisLandmarks, eyeLandmarks, eyeAnchors):
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

def process_image(image_data):

    answer = AnswerGenerator.Answer.UNDEFINED

    if (image_data[0] == FACE):

        try: 
            df = DFGenerator.FacialDFGenerator.generate_df(image_data[1])
        
        except DFGenerator.NoFaceDetectedException:
            return no_face_detected_exception
        
        except DFGenerator.MultiFaceDetectedException:
            return multi_face_detected_exception

        except Exception:
            return df_generator_exception

        try:
            state = facial_state_generator.get_state(df)

        except ValueError:
            return invalid_model_type

        except Exception:
            return state_generator_exception

        try:
            facial_answer_generator.add_frame_to_queue(state)
            answer = facial_answer_generator.determine_answer()

        except AnswerGenerator.InvalidStateException:
            return invalid_state_exception

        except Exception as e: 
            traceback.print_exc()
            return  state_generator_exception


    elif (image_data[0] == IRIS):
        
        try:
            df = DFGenerator.IrisDFGenerator.generate_df(image_data[1])
            res = np.array(df)[0]
            keypoints = compareIrisLandmarks(res[15:30], res[81:108], res[132:138]) + compareIrisLandmarks(res[0:15], res[30:57], res[138:])
            print(len(keypoints))

            if (len(iris_data_queue.get()) < MAX_SIZE_IRIS_DATA_QUEUE):

                iris_data_queue.get().append(keypoints)
                return answer
            
            else:
                iris_data_queue.get().pop(0)
                iris_data_queue.get().append(keypoints)


        except DFGenerator.NoFaceDetectedException:
            return no_face_detected_exception
        
        except DFGenerator.MultiFaceDetectedException:
            return multi_face_detected_exception

        except Exception as e:
            print("dataframeError:")
            traceback.print_exc()
            # print(e.with_traceback)
            return df_generator_exception

        try:
            state = iris_state_generator.get_state(np.array(iris_data_queue.get()))
            print(state)

        except ValueError:
            traceback.print_exc()
            return invalid_model_type

        except Exception:
            print("ERROR FROM ACTION STATE GENERATOR")
            traceback.print_exc()
            return state_generator_exception

        try:
            iris_answer_generator.add_frame_to_queue(state)
            answer = iris_answer_generator.determine_answer()
            print(answer)
        
        except AnswerGenerator.InvalidStateException:
            return invalid_state_exception 

        except Exception:
            traceback.print_exc()
            return  state_generator_exception


    return answer



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
                        answer = process_image((mode, converted))
                    except:
                        print("exception occured.")
                        pass

                    if (answer != current_answer.get()):
                        current_answer.set(answer)

                        if (answer == AnswerGenerator.Answer.UNDEFINED):
                            answer = "NO"
                        if (answer == AnswerGenerator.Answer.YES):
                            answer = "YES"

                        if (answer != AnswerGenerator.Answer.UNDEFINED):
                            print("Generated Answer: {}".format(answer))
                            #Put the answer in a json to send
                            returnInformation = {}
                            returnInformation['Answer'] = answer
                            json_returnInfo = json.dumps(returnInformation, indent = 4)
                            await websocket.send(json_returnInfo)

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
    asyncio.run(start_websocket())

if __name__ == "__main__":
    main()
