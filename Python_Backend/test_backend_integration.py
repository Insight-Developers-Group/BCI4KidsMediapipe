import cv2 
import os
import unittest
import sys
sys.path.insert(0, '../')

from MainRunner import process_image
from AnswerGenerator import Answer

FACE = "FACE"
IRIS = "IRIS"

class TestBackendIntegration(unittest.TestCase):

    def test_facial_yes_response(self):

        image = cv2.imread("testing/test_resources/smile_1.jpg")

        for x in range(30):
            answer = process_image((FACE, image))

        self.assertEqual(answer.value, Answer.YES.value)


    def test_facial_yes_mixed_response(self):

        image_smile = cv2.imread("testing/test_resources/smile_1.jpg")
        image_neutral = cv2.imread("testing/test_resources/neutral_1.jpg")

        for x in range(30):

            if x % 5 == 0:
                process_image((FACE, image_neutral))

            answer = process_image((FACE, image_smile))

        self.assertEqual(answer.value, Answer.YES.value)


    def test_facial_undefined_mixed_response(self):

        image_smile = cv2.imread("testing/test_resources/smile_1.jpg")
        image_neutral = cv2.imread("testing/test_resources/neutral_1.jpg")

        for x in range(30):

            if x % 5 == 0:
                process_image((FACE, image_smile))

            answer = process_image((FACE, image_neutral))

            answer

        self.assertEqual(answer.value, Answer.UNDEFINED.value)
