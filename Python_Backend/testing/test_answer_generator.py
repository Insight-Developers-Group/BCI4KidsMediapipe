import unittest
import sys
sys.path.insert(0, '../')

import AnswerGenerator
from AnswerGenerator import Answer

class TestAnswerGenerator(unittest.TestCase):

    def test_add_smile_to_queue(self):

        ag = AnswerGenerator.FacialAnswerGenerator()        
        ag.add_frame_to_queue("SMILE")

        self.assertEqual(ag._FacialAnswerGenerator__past_frames[ag.QUEUE_SIZE - 1], "SMILE")

    def test_add_frown_to_queue(self):

        ag = AnswerGenerator.FacialAnswerGenerator()        
        ag.add_frame_to_queue("FROWN")

        self.assertEqual(ag._FacialAnswerGenerator__past_frames[ag.QUEUE_SIZE - 1], "FROWN")

    def test_overfill_queue(self):
        ag = AnswerGenerator.FacialAnswerGenerator()

        for x in range(ag.QUEUE_SIZE * 2):

            if x % 2 == 0:
                ag.add_frame_to_queue("SMILE")
            else:
                ag.add_frame_to_queue("FROWN")

        for x in range(ag.QUEUE_SIZE):
            
            if x % 2 == 0:
                self.assertEqual(ag._FacialAnswerGenerator__past_frames[x], "SMILE")
            else:
                self.assertEqual(ag._FacialAnswerGenerator__past_frames[x], "FROWN")

    def test_facial_clear_queue(self):

        ag = AnswerGenerator.FacialAnswerGenerator()        
        ag.add_frame_to_queue("SMILE")
        ag.clear_queue()

        for frame in ag._FacialAnswerGenerator__past_frames:
            self.assertEqual(frame, "INIT")

    def test_facial_clear_full_queue(self):
        ag = AnswerGenerator.FacialAnswerGenerator()        
        
        for x in range(ag.QUEUE_SIZE):

            if x % 2 == 0:
                ag.add_frame_to_queue("SMILE")
            else:
                ag.add_frame_to_queue("FROWN")

        ag.clear_queue()

        for frame in ag._FacialAnswerGenerator__past_frames:
            self.assertEqual(frame, "INIT")

    def test_facial_clear_empty_queue(self):

        ag = AnswerGenerator.FacialAnswerGenerator()        
        ag.clear_queue()

        for frame in ag._FacialAnswerGenerator__past_frames:
            self.assertEqual(frame, "INIT")

    def test_yes_frame_all_smiles(self):
        ag = AnswerGenerator.FacialAnswerGenerator()

        for x in range(len(ag._FacialAnswerGenerator__past_frames)):
            ag.add_frame_to_queue("SMILE")

        self.assertEqual(ag.determine_answer(), Answer.YES)

    def test_yes_frame_one_frown(self):
        ag = AnswerGenerator.FacialAnswerGenerator()

        for x in range(len(ag._FacialAnswerGenerator__past_frames)):
            ag.add_frame_to_queue("SMILE")        

        ag.add_frame_to_queue("FROWN")
  
        self.assertEqual(ag.determine_answer(), Answer.YES)
    
    def test_no_frame_all_frowns(self):
        ag = AnswerGenerator.FacialAnswerGenerator()        
        
        for x in range(len(ag._FacialAnswerGenerator__past_frames)):
            ag.add_frame_to_queue("FROWN")

        self.assertEqual(ag.determine_answer(), Answer.NO)
    
    def test_no_frame_one_smile(self):
        ag = AnswerGenerator.FacialAnswerGenerator()        
        
        for x in range(len(ag._FacialAnswerGenerator__past_frames)):
            ag.add_frame_to_queue("FROWN")

        ag.add_frame_to_queue("SMILE")

        self.assertEqual(ag.determine_answer(), Answer.NO)
    
    def test_undefined_frame_mixed(self):
        ag = AnswerGenerator.FacialAnswerGenerator()        

        for x in range(ag.QUEUE_SIZE):

            if x % 3 == 0:
                ag.add_frame_to_queue("SMILE")
            elif x % 2 == 0:
                ag.add_frame_to_queue("FROWN")
            else:
                ag.add_frame_to_queue("NEUTRAL")

        self.assertEqual(ag.determine_answer(), Answer.UNDEFINED)
    
    def test_undefined_frame_init(self):
        ag = AnswerGenerator.FacialAnswerGenerator()        

        self.assertEqual(ag.determine_answer(), Answer.UNDEFINED)
    
    def test_undefined_frame_clear(self):
        ag = AnswerGenerator.FacialAnswerGenerator()

        for x in range(len(ag._FacialAnswerGenerator__past_frames)):
            ag.add_frame_to_queue("SMILE")

        ag.clear_queue()

        self.assertEqual(ag.determine_answer(), Answer.UNDEFINED)
    
    def test_undefined_frame_neutral(self):
        ag = AnswerGenerator.FacialAnswerGenerator()        

        for x in range(len(ag._FacialAnswerGenerator__past_frames)):
            ag.add_frame_to_queue("NEUTRAL")

        self.assertEqual(ag.determine_answer(), Answer.UNDEFINED)

    def test_add_invalid_frame(self):
        with self.assertRaises(Exception) as context:
            ag = AnswerGenerator.FacialAnswerGenerator()        
            ag.add_frame_to_queue("San Pellegrino")
            
        self.assertTrue("FacialAnswerGenerator: Invalid frame cannot be added to queue" in str(context.exception))

