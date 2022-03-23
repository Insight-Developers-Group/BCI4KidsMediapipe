
from pandas import array
from ActionBasedStateGenerator import ActionBasedStateGenerator
from tensorflow.keras.models import Sequential
import numpy as np
import unittest
import sys
import __main__
from unittest.mock import MagicMock
from ActionBasedStateGenerator import ActionBasedStateGenerator

class TestActionBasedStateGenerator(unittest.TestCase):

    def test_path_f(self):

        sg = ActionBasedStateGenerator("SAMPLEPATH", 33)

        self.assertEqual(sg.get_model_path(), "SAMPLEPATH")

    def test_add_invalid_ModelType(self):
        with self.assertRaises(ValueError) as context:
            sg = ActionBasedStateGenerator("SAMPLEPATH", -1)

        self.assertTrue("Sequence Length Cannot be Less than 0" in str(context.exception))

    def test_Neutral(self):
        mocked = Sequential
        mocked.predict = MagicMock(return_value= [np.array([0,1,0])])
        mocked.load_weights = MagicMock()

        sg = ActionBasedStateGenerator("SAMPLEPATH", 1)
        state = sg.get_state([])
        self.assertTrue(state == "NEUTRAL")
        del(mocked)

    def test_Yes(self):
        mocked = Sequential
        mocked.predict = MagicMock(return_value= [np.array([1,0.5,0])])
        mocked.load_weights = MagicMock()

        sg = ActionBasedStateGenerator("SAMPLEPATH", 1)
        state = sg.get_state([])
        self.assertTrue(state == "YES")
        del(mocked)

    def test_No(self):
        mocked = Sequential
        mocked.predict = MagicMock(return_value= [np.array([0.2,0.3,0.9])])
        mocked.load_weights = MagicMock()

        sg = ActionBasedStateGenerator("SAMPLEPATH", 1)
        state = sg.get_state([])
        self.assertTrue(state == "NO")
        del(mocked)
	


        

