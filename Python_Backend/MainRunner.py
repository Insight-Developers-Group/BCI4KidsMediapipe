#!/usr/bin/env python

import asyncio
from enum import Enum
import websockets
from PIL import Image
import cv2 as cv
import numpy
import io
import base64
from concurrent.futures import ProcessPoolExecutor
import AnswerGenerator
import StateGenerator
import DFGenerator

# Initiate State Generator with the appropriate models
stateGenerator = StateGenerator.StateGenerator("../Machine_Learning_Model/smile_neutral_rf.pkl", "FACE")

# Two types of Generators
facialAnswerGenerator = AnswerGenerator.FacialAnswerGenerator()
irisAnswerGenerator = None  # TODO MAKE THIS THE ACTUAL DATA TYPE

FACE = "FACE"
IRIS = "IRIS"

current_tracking_mode = FACE
current_answer = AnswerGenerator.Answer.UNDEFINED


def process_image(image_data):

    answer = AnswerGenerator.Answer.UNDEFINED

    # Use the generator based on the imageType
    df = None
    if (image_data[0] == FACE):
        df = DFGenerator.FacialDFGenerator.generate_df(image_data[1])

    elif (image_data[0] == IRIS):
        df = DFGenerator.IrisDFGenerator.generate_df(image_data[1])

    else:
        return answer

    if current_tracking_mode != image_data[0]:

        if image_data[0] == FACE:
            stateGenerator = StateGenerator.StateGenerator("../Machine_Learning_Model/smile_neutral_rf.pkl", "FACE")
            
        elif image_data[0] == IRIS:
            stateGenerator = StateGenerator.StateGenerator("../Machine_Learning_Model/iris_rf.pkl", "IRIS")

    # Run Machine learning algorithm based on type
    state = stateGenerator.get_state(df)

    print("yui")
    print(state)

    # Run the Answer Generator
    if (image_data[0] == FACE):
        facialAnswerGenerator.add_state_to_queue(state)
        answer = facialAnswerGenerator.determine_answer()

    #elif (image_data[0] == IRIS):
        #irisAnswerGenerator.add_state_to_queue(state)
        #answer = irisAnswerGenerator.determine_answer()

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
        temp = message.split(",")
        for i in temp:
            if(i != "data:image/jpeg;base64"):
                try:
                    ima = Image.open(io.BytesIO(base64.b64decode(i)))
                    print("hello")
                    #convert the image to cv2 for use in the state generators
                    converted = convert_image(ima)

                    answer = process_image((FACE, converted))

                    if (answer != current_answer) and (answer != AnswerGenerator.Answer.UNDEFINED):
                        current_answer = answer
                        print(answer)
                        await websocket.send(answer)

                except:
                    print("there was an error with that image and it could not be decoded")
                    #at this point we could call for the program to quit or return an error here, depends whats appropriate



async def start_websocket():
    async with websockets.serve(recv_image, "localhost", 8765):
        await asyncio.Future()  # run forever



asyncio.run(start_websocket())

