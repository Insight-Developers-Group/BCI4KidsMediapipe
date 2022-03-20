import cv2 
import unittest
import sys
sys.path.insert(0, '../')

import MainRunner
from AnswerGenerator import Answer

FACE = "FACE"
IRIS = "IRIS"

class TestBackendIntegration(unittest.TestCase):

    def test_facial_yes_response(self):

        image = cv2.imread("testing/test_resources/smile_1.jpg")

        for x in range(30):
            answer = MainRunner.process_image((FACE, image))

        self.assertEqual(answer, "YES")


    def test_facial_yes_mixed_response(self):

        image_smile = cv2.imread("testing/test_resources/smile_1.jpg")
        image_neutral = cv2.imread("testing/test_resources/neutral_1.jpg")

        for x in range(30):

            if x % 5 == 0:
                MainRunner.process_image((FACE, image_neutral))

            answer = MainRunner.process_image((FACE, image_smile))

        self.assertEqual(answer, "YES")


    def test_facial_undefined_mixed_response(self):

        image_smile = cv2.imread("testing/test_resources/smile_1.jpg")
        image_neutral = cv2.imread("testing/test_resources/neutral_1.jpg")

        for x in range(30):

            if x % 5 == 0:
                MainRunner.process_image((FACE, image_smile))

            answer = MainRunner.process_image((FACE, image_neutral))

        self.assertEqual(answer, "NO")

    def test_facial_no_face_detected_exception(self):

        image = cv2.imread("testing/test_resources/panda.png")
        answer = MainRunner.process_image((FACE, image))

        self.assertEqual(answer, MainRunner.no_face_detected_exception)

    def test_facial_multi_face_detected_0_exception(self):

        image = cv2.imread("testing/test_resources/two_faces_1.png")
        answer = MainRunner.process_image((FACE, image))

        self.assertEqual(answer, MainRunner.multi_face_detected_exception)

    def test_facial_multi_face_detected_1_exception(self):

        image = cv2.imread("testing/test_resources/three_faces_1.png")
        answer = MainRunner.process_image((FACE, image))

        self.assertEqual(answer, MainRunner.multi_face_detected_exception)
    
    def test_facial_invalid_path_exception(self):

        image = cv2.imread("invalid/path/pic.png")
        answer = MainRunner.process_image((FACE, image))

        self.assertEqual(answer, MainRunner.df_generator_exception)
