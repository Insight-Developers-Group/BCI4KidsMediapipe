import unittest
import sys
import cv2
sys.path.insert(0, '../')

from DFGenerator import FacialDFGenerator
from DFGenerator import IrisDFGenerator

class TestDFGenerator(unittest.TestCase):

    #There are two tests each which test the shape of each DF to make sure they are sized properly 
    def test_facial_df_shape(self):
        image = cv2.imread('test_resources/smile_1.jpg')
        df = FacialDFGenerator.generate_df(image)

        self.assertEqual(len(df.columns), 1404)

    def test_iris_df_shape(self):
        image = cv2.imread('test_resources/smile_1.jpg')
        df = IrisDFGenerator.generate_df(image)

        self.assertEqual(len(df.columns), 477)

    