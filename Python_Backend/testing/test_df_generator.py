import unittest
import sys
sys.path.insert(0, '../')

from DFGenerator import FacialDFGenerator
from DFGenerator import IrisDFGenerator

class TestAnswerGenerator(unittest.TestCase):

    #There are two tests each which test the shape of each DF to make sure they are sized properly 
    def test_facial_df_shape(self):

        df = FacialDFGenerator.generate_df("test_resources/smile_1.jpg")

        self.assertEqual(len(df.columns), 1404)

    def test_iris_df_shape(self):

        df = IrisDFGenerator.generate_df("test_resources/smile_1.jpg")

        self.assertEqual(len(df.columns), 568)

    