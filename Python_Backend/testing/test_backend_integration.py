import cv2 
import unittest
import sys
sys.path.insert(0, '../')

import MainRunner

FACE = "FACE"
IRIS = "IRIS"

class TestBackendIntegration(unittest.TestCase):

    def test_facial_yes_response(self):

        image = cv2.imread("test_resources/smile_1.jpg")

        for x in range(30):
            answer = MainRunner.process_image((FACE, image))

        self.assertEqual(answer, 1)

