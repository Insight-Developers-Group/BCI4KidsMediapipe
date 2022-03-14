#!/usr/bin/env python

import asyncio
import base64
import binascii
import io
import numpy
from PIL import Image, UnidentifiedImageError
import websockets
import contextvars

import AnswerGenerator
import DFGenerator
from StateGenerator import StateGenerator
import json 
from ActionBasedStateGenerator import ActionBasedStateGenerator


# Initiate State Generator with the appropriate models
facial_state_generator = StateGenerator("../Machine_Learning_Model/smile_neutral_rf.pkl", "FACE")
iris_state_generator = ActionBasedStateGenerator("../Machine_Learning_Model/iris.pkl", 48)

#Initiate actionList to send to 

# Two types of Generators
facial_answer_generator = AnswerGenerator.FacialAnswerGenerator()
iris_answer_generator = None  # TODO MAKE THIS THE ACTUAL DATA TYPE

FACE = "FACE"
IRIS = "IRIS"

MAX_SIZE_IRIS_DATA_QUEUE = 98

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
            facial_answer_generator.add_state_to_queue(state)
            answer = facial_answer_generator.determine_answer()

        except AnswerGenerator.InvalidStateException:
            return invalid_state_exception

        except Exception:
            return  state_generator_exception


    elif (image_data[0] == IRIS):
        
        try:
            df = DFGenerator.IrisDFGenerator.generate_df(image_data[1])

            if (len(iris_data_queue) < MAX_SIZE_IRIS_DATA_QUEUE):
                iris_data_queue.append(df)
                return answer
            
            else:
                iris_data_queue.pop(0)
                iris_data_queue.append(df)


        except DFGenerator.NoFaceDetectedException:
            return no_face_detected_exception
        
        except DFGenerator.MultiFaceDetectedException:
            return multi_face_detected_exception

        except Exception:
            return df_generator_exception

        try:
            state = iris_state_generator.get_state(iris_data_queue)

        except ValueError:
            return invalid_model_type

        except Exception:
            return state_generator_exception

        try:
            iris_answer_generator.add_state_to_queue(state)
            answer = iris_answer_generator.determine_answer()
        
        except AnswerGenerator.InvalidStateException:
            return invalid_state_exception 

        except Exception:
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

