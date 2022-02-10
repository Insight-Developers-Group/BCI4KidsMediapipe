import unittest
import sys
sys.path.insert(0, '../')

from PIL import Image
import cv2 as cv
import numpy

from MainRunner import convert_image
from MainRunner import process_image

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

    def test_process_image_smile_face(self):
        im = Image.open("test_resources/smile_1.jpg")
        open_cv_image = numpy.array(im)
        open_cv_image = open_cv_image[:,:,::-1].copy()
        print(process_image(("FACE",open_cv_image)))

