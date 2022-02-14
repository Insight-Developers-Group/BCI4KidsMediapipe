#!/usr/bin/env python

import asyncio
import binascii
from enum import Enum
import websockets
import contextvars
from PIL import Image
from PIL import UnidentifiedImageError
import cv2 as cv
import numpy
import io
import base64
from concurrent.futures import ProcessPoolExecutor
import AnswerGenerator
from StateGenerator import StateGenerator
import DFGenerator
import json
import time
import random

# Initiate State Generator with the appropriate models
facial_state_generator = StateGenerator("../Machine_Learning_Model/smile_neutral_rf.pkl", "FACE")
iris_state_generator = StateGenerator("../Machine_Learning_Model/iris.pkl", "IRIS")

# Two types of Generators
facial_answer_generator = AnswerGenerator.FacialAnswerGenerator()
iris_answer_generator = None  # TODO MAKE THIS THE ACTUAL DATA TYPE

FACE = "FACE"
IRIS = "IRIS"

frame_counter = contextvars.ContextVar('frame_counter', default=0)

current_answer = AnswerGenerator.Answer.UNDEFINED


def process_image(image_data):

    answer = AnswerGenerator.Answer.UNDEFINED

    if (image_data[0] == FACE):

        df = DFGenerator.FacialDFGenerator.generate_df(image_data[1])

        state = facial_state_generator.get_state(df)

        facial_answer_generator.add_state_to_queue(state)
        answer = facial_answer_generator.determine_answer()

    elif (image_data[0] == IRIS):

        df = DFGenerator.IrisDFGenerator.generate_df(image_data[1])

        state = iris_state_generator.get_state(df)

        iris_answer_generator.add_state_to_queue(state)
        answer = iris_answer_generator.determine_answer()

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

        frame_counter.set(frame_counter.get() + 1)

        if frame_counter.get() >= 5:

            frame_counter.set(0)

            temp = message.split(",")
            for i in temp:
                if(i != "data:image/jpeg;base64"):
                    try:
                        ima = Image.open(io.BytesIO(base64.b64decode(i)))

                        #convert the image to cv2 for use in the state generators

                        # number = random.randint(0,10)

                        # if ( number  <5 ):

                        #     answer = "YES"
                        # else:
                        #     answer = "NO"
                        # 

                        converted = convert_image(ima)
                        try:
                            answer = process_image((FACE, converted))
                        except:
                            print("exception occured")
                            return None
                        # TEMPORARY REMOVAL
                        if (answer == AnswerGenerator.Answer.UNDEFINED):
                            answer = "NO"
                        if (answer == AnswerGenerator.Answer.YES):
                            answer = "YES"

                        print(answer)

                        # print("Generated Answer: {}".format(answer))
                        #Put the answer in a json to send
                        returnInformation = {}
                        returnInformation['Answer'] = answer
                        json_returnInfo = json.dumps(returnInformation, indent = 4)
                        await websocket.send(json_returnInfo)
                        

                    #except the exceptions that Pillow will typically throw if something is wrong with the image when opening it
                    except (UnidentifiedImageError, ValueError, TypeError) as ex:
                        print("there was an error with that image and it could not be decoded and opened as an image")
                        print(ex)
                        #at this point we could call for the program to quit or return an error here, depends whats appropriate
                
                    #except the error from decoding the base64 data
                    except (binascii.Error) as decod:
                        print("There was an error decoding the image data in base64")
                        print(decod)



async def start_websocket():

    asyncState = type('', (), {})()
    asyncState.counter = 0

    async with websockets.serve(recv_image, "localhost", 8765):
        await asyncio.Future()  # run forever



asyncio.run(start_websocket())
