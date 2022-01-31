#!/usr/bin/env python

import asyncio
import websockets
from PIL import Image
import cv2 as cv
import numpy
import io
import base64

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
async def recv_img(websocket):
    async for message in websocket:
        temp = message.split(",")
        for i in temp:
            if(i != "data:image/jpeg;base64"):
                try:
                    ima = Image.open(io.BytesIO(base64.b64decode(i)))
                    
                    #convert the image to cv2 for use in the state generators
                    converted = convert_image(ima)
                except:
                    print("there was an error with that image and it could not be decoded")
                    #at this point we could call for the program to quit or return an error here, depends whats appropriate


async def main():
    async with websockets.serve(recv_img, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())