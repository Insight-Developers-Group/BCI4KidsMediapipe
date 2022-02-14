import unittest
from unittest.mock import Mock
import sys
sys.path.insert(0, '../')

from PIL import Image
import cv2 as cv
import numpy

import MainRunner
from MainRunner import convert_image
from MainRunner import process_image
from AnswerGenerator import Answer

class TestMainRunner(unittest.TestCase):

    def test_image_conversion_1(self):
        im = Image.open("test_resources/test_img1.jpg")
        open_cv_image = numpy.array(im)
        open_cv_image = open_cv_image[:,:,::-1].copy()
        compare = numpy.array_equal(open_cv_image, convert_image(im))

        self.assertEqual(compare,True)

    def test_image_conversion_2(self):
        im = Image.open("test_resources/test_img2.jpg")
        open_cv_image = numpy.array(im)
        open_cv_image = open_cv_image[:,:,::-1].copy()
        compare = numpy.array_equal(open_cv_image, convert_image(im))

        self.assertEqual(compare,True)
    
    def test_image_conversion_3(self):
        im = Image.open("test_resources/bci4kids.jpg")
        open_cv_image = numpy.array(im)
        open_cv_image = open_cv_image[:,:,::-1].copy()
        compare = numpy.array_equal(open_cv_image, convert_image(im))

        self.assertEqual(compare,True)

    def test_process_image_bad_face(self):
        mock = Mock()
        mock.side_effect = Exception("FacialDFGenerator: No face detected")
        MainRunner.DFGenerator.FacialDFGenerator.generate_df = mock
        im = Image.open("test_resources/test_img2.jpg")
        open_cv_image = numpy.array(im)
        open_cv_image = open_cv_image[:,:,::-1].copy()
        testval = 0
        try:
            value = process_image(("FACE",open_cv_image))
        except Exception as e:
            if (str(e)=="FacialDFGenerator: No face detected"):
                testval = 1
            else:
                raise e
        
        self.assertEqual(testval,1)

    def test_process_image_bad_iris(self):
        mock = Mock()
        mock.side_effect = Exception("IrisDFGenerator: No face detected")
        MainRunner.DFGenerator.FacialDFGenerator.generate_df = mock
        im = Image.open("test_resources/test_img2.jpg")
        open_cv_image = numpy.array(im)
        open_cv_image = open_cv_image[:,:,::-1].copy()
        testval = 0
        try:
            value = process_image(("IRIS",open_cv_image))
        except Exception as e:
            if (str(e)=="IrisDFGenerator: No face detected"):
                testval = 1
            else:
                raise e
        
        self.assertEqual(testval,1)

    def test_process_image_yes_face(self):
        mock = Mock()
        mock2 = Mock()
        mock3 = Mock()
        MainRunner.facial_state_generator = mock
        MainRunner.facial_answer_generator = mock2
        MainRunner.facial_answer_generator.determine_answer().return_value = Answer.YES
        MainRunner.DFGenerator = mock3
        im = Image.open("test_resources/test_img1.jpg")
        open_cv_image = numpy.array(im)
        open_cv_image = open_cv_image[:,:,::-1].copy()
        test = process_image(("FACE",open_cv_image))
        
        self.assertEqual(test(),Answer.YES)

    def test_process_image_yes_iris(self):
        mock = Mock()
        mock2 = Mock()
        mock3 = Mock()
        MainRunner.iris_state_generator = mock
        MainRunner.iris_answer_generator = mock2
        MainRunner.iris_answer_generator.determine_answer().return_value = Answer.YES
        MainRunner.DFGenerator = mock3
        im = Image.open("test_resources/test_img1.jpg")
        open_cv_image = numpy.array(im)
        open_cv_image = open_cv_image[:,:,::-1].copy()
        test = process_image(("IRIS",open_cv_image))
        
        self.assertEqual(test(),Answer.YES)

    def test_process_image_no_face(self):
        mock = Mock()
        mock2 = Mock()
        mock3 = Mock()
        MainRunner.facial_state_generator = mock
        MainRunner.facial_answer_generator = mock2
        MainRunner.facial_answer_generator.determine_answer().return_value = Answer.NO
        MainRunner.DFGenerator = mock3
        im = Image.open("test_resources/test_img1.jpg")
        open_cv_image = numpy.array(im)
        open_cv_image = open_cv_image[:,:,::-1].copy()
        test = process_image(("FACE",open_cv_image))
        
        self.assertEqual(test(),Answer.NO)

    def test_process_image_no_iris(self):
        mock = Mock()
        mock2 = Mock()
        mock3 = Mock()
        MainRunner.iris_state_generator = mock
        MainRunner.iris_answer_generator = mock2
        MainRunner.iris_answer_generator.determine_answer().return_value = Answer.NO
        MainRunner.DFGenerator = mock3
        im = Image.open("test_resources/test_img1.jpg")
        open_cv_image = numpy.array(im)
        open_cv_image = open_cv_image[:,:,::-1].copy()
        test = process_image(("IRIS",open_cv_image))
        
        self.assertEqual(test(),Answer.NO)

    def test_process_image_undefined_face(self):
        mock = Mock()
        mock2 = Mock()
        mock3 = Mock()
        MainRunner.facial_state_generator = mock
        MainRunner.facial_answer_generator = mock2
        MainRunner.facial_answer_generator.determine_answer().return_value = Answer.UNDEFINED
        MainRunner.DFGenerator = mock3
        im = Image.open("test_resources/test_img1.jpg")
        open_cv_image = numpy.array(im)
        open_cv_image = open_cv_image[:,:,::-1].copy()
        test = process_image(("FACE",open_cv_image))
        
        self.assertEqual(test(),Answer.UNDEFINED)

    def test_process_image_undefined_iris(self):
        mock = Mock()
        mock2 = Mock()
        mock3 = Mock()
        MainRunner.iris_state_generator = mock
        MainRunner.iris_answer_generator = mock2
        MainRunner.iris_answer_generator.determine_answer().return_value = Answer.UNDEFINED
        MainRunner.DFGenerator = mock3
        im = Image.open("test_resources/test_img1.jpg")
        open_cv_image = numpy.array(im)
        open_cv_image = open_cv_image[:,:,::-1].copy()
        test = process_image(("IRIS",open_cv_image))
        
        self.assertEqual(test(),Answer.UNDEFINED)
