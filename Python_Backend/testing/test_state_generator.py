from MockClassifiers import MockIrisClassifier
from MockClassifiers import MockFaceClassifier
import numpy as np
import unittest
import sys
import __main__
sys.path.insert(0, '../')
from StateGenerator import StateGenerator


class TestAnswerGenerator(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        __main__.MockFaceClassifier = MockFaceClassifier
        self.cls = MockFaceClassifier
        self.instance = MockFaceClassifier().__init__()

        __main__.MockIrisClassifier = MockIrisClassifier
        self.cls = MockIrisClassifier
        self.instance = MockIrisClassifier().__init__()
        unittest.TestCase.__init__(self, *args, **kwargs)

    def test_path_f(self):

        sg = StateGenerator("SAMPLEPATH", "FACE")

        self.assertEqual(sg.get_model_path(), "SAMPLEPATH")

    def test_path_i(self):

        sg = StateGenerator("SAMPLEPATH", "IRIS")

        self.assertEqual(sg.get_model_path(), "SAMPLEPATH")

    def test_iris_model_type(self):

        sg = StateGenerator("SAMPLEPATH", "IRIS")

        self.assertEqual(sg.get_model_type(), "IRIS")

    def test_face_model_type(self):

        sg = StateGenerator("SAMPLEPATH", "FACE")

        self.assertEqual(sg.get_model_type(), "FACE")

    def test_add_invalid_ModelType(self):
        with self.assertRaises(ValueError) as context:
            sg = StateGenerator("SAMPLEPATH", "NOTFACEORIRIS")

        self.assertTrue("NOTFACEORIRIS" in str(context.exception))

    def test_Neutral_f(self):

        sg = StateGenerator("test_resources/test_face_classifier.pkl", "FACE")
        self.assertEqual(sg.get_state([[0]]), "NEUTRAL")

    def test_Smile_f(self):

        sg = StateGenerator("test_resources/test_face_classifier.pkl", "FACE")
        self.assertEqual(sg.get_state([[1]]), "SMILE")

    def test_Frown_f(self):

        sg = StateGenerator("test_resources/test_face_classifier.pkl", "FACE")
        self.assertEqual(sg.get_state([[2]]), "FROWN")

    def test_Eyes_Up_i(self):
        sg = StateGenerator("test_resources/test_iris_classifier.pkl", "IRIS")
        self.assertEqual(sg.get_state([[0]]), "EYES_UP")

    def test_Eyes_Down_i(self):
        sg = StateGenerator("test_resources/test_iris_classifier.pkl", "IRIS")
        self.assertEqual(sg.get_state([[1]]), "EYES_DOWN")

    def test_Eyes_Left_i(self):
        sg = StateGenerator("test_resources/test_iris_classifier.pkl", "IRIS")
        self.assertEqual(sg.get_state([[2]]), "EYES_LEFT")

    def test_Eyes_Right_i(self):
        sg = StateGenerator("test_resources/test_iris_classifier.pkl", "IRIS")
        self.assertEqual(sg.get_state([[3]]), "EYES_RIGHT")

    def test_Eyes_Centre_i(self):
        sg = StateGenerator("test_resources/test_iris_classifier.pkl", "IRIS")
        self.assertEqual(sg.get_state([[4]]), "EYES_CENTRE")
