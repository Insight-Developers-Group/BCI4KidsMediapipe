import unittest
import sys
sys.path.insert(0, '../')

import AnswerGenerator
from AnswerGenerator import Answer

class TestAnswerGenerator(unittest.TestCase):

    INIT_QUEUE = ["INIT", "INIT", "INIT", "INIT", "INIT"]

    def test_add_smile_to_queue(self):

        ag = AnswerGenerator.FacialAnswerGenerator()        
        ag.add_state_to_queue("SMILE")

        self.assertEqual(ag._FacialAnswerGenerator__past_states, ["INIT", "INIT", "INIT", "INIT", "SMILE"])

    def test_add_frown_to_queue(self):

        ag = AnswerGenerator.FacialAnswerGenerator()        
        ag.add_state_to_queue("FROWN")

        self.assertEqual(ag._FacialAnswerGenerator__past_states, ["INIT", "INIT", "INIT", "INIT", "FROWN"])

    def test_overfill_queue(self):
        ag = AnswerGenerator.FacialAnswerGenerator()        
        ag.add_state_to_queue("NEUTRAL")
        ag.add_state_to_queue("FROWN")
        ag.add_state_to_queue("SMILE")
        ag.add_state_to_queue("FROWN")
        ag.add_state_to_queue("FROWN")
        ag.add_state_to_queue("SMILE")
        ag.add_state_to_queue("FROWN")
        ag.add_state_to_queue("NEUTRAL")

        self.assertEqual(ag._FacialAnswerGenerator__past_states, ["FROWN", "FROWN", "SMILE", "FROWN", "NEUTRAL"])

    def test_facial_clear_queue(self):

        ag = AnswerGenerator.FacialAnswerGenerator()        
        ag.add_state_to_queue("SMILE")
        ag.clear_queue()

        self.assertEqual(ag._FacialAnswerGenerator__past_states, self.INIT_QUEUE)

    def test_facial_clear_full_queue(self):
        ag = AnswerGenerator.FacialAnswerGenerator()        
        ag.add_state_to_queue("SMILE")
        ag.add_state_to_queue("FROWN")
        ag.add_state_to_queue("SMILE")
        ag.add_state_to_queue("FROWN")
        ag.add_state_to_queue("SMILE")
        ag.clear_queue()

        self.assertEqual(ag._FacialAnswerGenerator__past_states, self.INIT_QUEUE)

    def test_facial_clear_empty_queue(self):

        ag = AnswerGenerator.FacialAnswerGenerator()        
        ag.clear_queue()

        self.assertEqual(ag._FacialAnswerGenerator__past_states, self.INIT_QUEUE)

    def test_yes_state_all_smiles(self):
        ag = AnswerGenerator.FacialAnswerGenerator()        
        ag.add_state_to_queue("SMILE")
        ag.add_state_to_queue("SMILE")
        ag.add_state_to_queue("SMILE")
        ag.add_state_to_queue("SMILE")
        ag.add_state_to_queue("SMILE")

        self.assertEqual(ag.determine_answer(), Answer.YES)

    def test_yes_state_one_frown(self):
        ag = AnswerGenerator.FacialAnswerGenerator()        
        ag.add_state_to_queue("SMILE")
        ag.add_state_to_queue("SMILE")
        ag.add_state_to_queue("FROWN")
        ag.add_state_to_queue("SMILE")
        ag.add_state_to_queue("SMILE")

        self.assertEqual(ag.determine_answer(), Answer.YES)
    
    def test_no_state_all_frowns(self):
        ag = AnswerGenerator.FacialAnswerGenerator()        
        ag.add_state_to_queue("FROWN")
        ag.add_state_to_queue("FROWN")
        ag.add_state_to_queue("FROWN")
        ag.add_state_to_queue("FROWN")
        ag.add_state_to_queue("FROWN")

        self.assertEqual(ag.determine_answer(), Answer.NO)
    
    def test_no_state_one_smile(self):
        ag = AnswerGenerator.FacialAnswerGenerator()        
        ag.add_state_to_queue("FROWN")
        ag.add_state_to_queue("FROWN")
        ag.add_state_to_queue("FROWN")
        ag.add_state_to_queue("FROWN")
        ag.add_state_to_queue("SMILE")

        self.assertEqual(ag.determine_answer(), Answer.NO)
    
    def test_undefined_state_mixed(self):
        ag = AnswerGenerator.FacialAnswerGenerator()        
        ag.add_state_to_queue("SMILE")
        ag.add_state_to_queue("NEUTRAL")
        ag.add_state_to_queue("FROWN")
        ag.add_state_to_queue("SMILE")
        ag.add_state_to_queue("SMILE")

        self.assertEqual(ag.determine_answer(), Answer.UNDEFINED)
    
    def test_undefined_state_init(self):
        ag = AnswerGenerator.FacialAnswerGenerator()        

        self.assertEqual(ag.determine_answer(), Answer.UNDEFINED)
    
    def test_undefined_state_clear(self):
        ag = AnswerGenerator.FacialAnswerGenerator()        
        ag.add_state_to_queue("SMILE")
        ag.add_state_to_queue("SMILE")
        ag.add_state_to_queue("SMILE")
        ag.add_state_to_queue("SMILE")
        ag.add_state_to_queue("SMILE")
        ag.clear_queue()

        self.assertEqual(ag.determine_answer(), Answer.UNDEFINED)
    
    def test_undefined_state_neutral(self):
        ag = AnswerGenerator.FacialAnswerGenerator()        
        ag.add_state_to_queue("NEUTRAL")
        ag.add_state_to_queue("NEUTRAL")
        ag.add_state_to_queue("NEUTRAL")
        ag.add_state_to_queue("NEUTRAL")
        ag.add_state_to_queue("NEUTRAL")

        self.assertEqual(ag.determine_answer(), Answer.UNDEFINED)

    def test_add_invalid_state(self):
        with self.assertRaises(Exception) as context:
            ag = AnswerGenerator.FacialAnswerGenerator()        
            ag.add_state_to_queue("San Pellegrino")

        self.assertTrue("FacialAnswerGenerator: Invalid state cannot be added to queue" in str(context.exception))