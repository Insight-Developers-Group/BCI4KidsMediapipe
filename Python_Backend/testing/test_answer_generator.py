import unittest
import sys

sys.path.insert(0, '../')

import AnswerGenerator
from AnswerGenerator import Answer

class TestAnswerGenerator(unittest.TestCase):

    # Unit tests for FacialAnswerGenerator

    def test_facial_add_smile_to_queue(self):

        ag = AnswerGenerator.FacialAnswerGenerator()        
        ag.add_frame_to_queue("SMILE")

        self.assertEqual(ag._FacialAnswerGenerator__past_frames[ag.QUEUE_SIZE - 1], "SMILE")

    def test_facial_add_frown_to_queue(self):

        ag = AnswerGenerator.FacialAnswerGenerator()        
        ag.add_frame_to_queue("FROWN")

        self.assertEqual(ag._FacialAnswerGenerator__past_frames[ag.QUEUE_SIZE - 1], "FROWN")

    def test_facial_overfill_queue(self):
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

    def test_facial_yes_series_all_smiles(self):
        ag = AnswerGenerator.FacialAnswerGenerator()

        for x in range(len(ag._FacialAnswerGenerator__past_frames)):
            ag.add_frame_to_queue("SMILE")

        self.assertEqual(ag.determine_answer(), Answer.YES)

    def test_facial_yes_series_one_frown(self):
        ag = AnswerGenerator.FacialAnswerGenerator()

        for x in range(len(ag._FacialAnswerGenerator__past_frames)):
            ag.add_frame_to_queue("SMILE")        

        ag.add_frame_to_queue("FROWN")
  
        self.assertEqual(ag.determine_answer(), Answer.YES)
    
    def test_facial_no_series_all_frowns(self):
        ag = AnswerGenerator.FacialAnswerGenerator()        
        
        for x in range(len(ag._FacialAnswerGenerator__past_frames)):
            ag.add_frame_to_queue("FROWN")

        self.assertEqual(ag.determine_answer(), Answer.NO)
    
    def test_facial_no_series_one_smile(self):
        ag = AnswerGenerator.FacialAnswerGenerator()        
        
        for x in range(len(ag._FacialAnswerGenerator__past_frames)):
            ag.add_frame_to_queue("FROWN")

        ag.add_frame_to_queue("SMILE")

        self.assertEqual(ag.determine_answer(), Answer.NO)
    
    def test_facial_undefined_series_mixed(self):
        ag = AnswerGenerator.FacialAnswerGenerator()        

        for x in range(ag.QUEUE_SIZE):

            if x % 3 == 0:
                ag.add_frame_to_queue("SMILE")
            elif x % 2 == 0:
                ag.add_frame_to_queue("FROWN")
            else:
                ag.add_frame_to_queue("NEUTRAL")

        self.assertEqual(ag.determine_answer(), Answer.UNDEFINED)
    
    def test_facial_undefined_series_init(self):
        ag = AnswerGenerator.FacialAnswerGenerator()        

        self.assertEqual(ag.determine_answer(), Answer.UNDEFINED)
    
    def test_facial_undefined_series_clear(self):
        ag = AnswerGenerator.FacialAnswerGenerator()

        for x in range(len(ag._FacialAnswerGenerator__past_frames)):
            ag.add_frame_to_queue("SMILE")

        ag.clear_queue()

        self.assertEqual(ag.determine_answer(), Answer.UNDEFINED)
    
    def test_facial_undefined_series_neutral(self):
        ag = AnswerGenerator.FacialAnswerGenerator()        

        for x in range(len(ag._FacialAnswerGenerator__past_frames)):
            ag.add_frame_to_queue("NEUTRAL")

        self.assertEqual(ag.determine_answer(), Answer.UNDEFINED)

    def test_facial_add_invalid_frame(self):
        with self.assertRaises(Exception) as context:
            ag = AnswerGenerator.FacialAnswerGenerator()        
            ag.add_frame_to_queue("San Pellegrino")
            
        self.assertTrue("FacialAnswerGenerator: Invalid frame cannot be added to queue" in str(context.exception))

   # Unit tests for IrisAnswerGenerator 

    def test_iris_add_yes_to_queue(self):

        ag = AnswerGenerator.IrisAnswerGenerator()       
        ag.add_frame_to_queue("YES")

        self.assertEqual(ag._IrisAnswerGenerator__past_states[ag.QUEUE_SIZE - 1], "YES")

    def test_iris_add_frown_to_queue(self):

        ag = AnswerGenerator.IrisAnswerGenerator()
        ag.add_frame_to_queue("NO")

        self.assertEqual(ag._IrisAnswerGenerator__past_states[ag.QUEUE_SIZE - 1], "NO")

    def test_iris_overfill_queue(self):
        ag = AnswerGenerator.IrisAnswerGenerator()

        for x in range(ag.QUEUE_SIZE * 2):

            if x % 2 == 0:
                ag.add_frame_to_queue("YES")
            else:
                ag.add_frame_to_queue("NO")

        for x in range(ag.QUEUE_SIZE):
            
            if x % 2 == 0:
                self.assertEqual(ag._IrisAnswerGenerator__past_states[x], "YES")
            else:
                self.assertEqual(ag._IrisAnswerGenerator__past_states[x], "NO")

    def test_iris_clear_queue(self):

        ag = AnswerGenerator.IrisAnswerGenerator()      
        ag.add_frame_to_queue("YES")
        ag.clear_queue()

        for frame in ag._IrisAnswerGenerator__past_states:
            self.assertEqual(frame, "INIT")

    def test_iris_clear_full_queue(self):
        ag = AnswerGenerator.IrisAnswerGenerator()       
        
        for x in range(ag.QUEUE_SIZE):

            if x % 2 == 0:
                ag.add_frame_to_queue("YES")
            else:
                ag.add_frame_to_queue("NO")

        ag.clear_queue()

        for frame in ag._IrisAnswerGenerator__past_states:
            self.assertEqual(frame, "INIT")

    def test_iris_clear_empty_queue(self):

        ag = AnswerGenerator.IrisAnswerGenerator()        
        ag.clear_queue()

        for frame in ag._IrisAnswerGenerator__past_states:
            self.assertEqual(frame, "INIT")

    def test_iris_yes_series_all_yeses(self):
        ag = AnswerGenerator.IrisAnswerGenerator()

        for x in range(len(ag._IrisAnswerGenerator__past_states)):
            ag.add_frame_to_queue("YES")

        self.assertEqual(ag.determine_answer(), Answer.YES)

    def test_iris_yes_series_one_no(self):
        ag = AnswerGenerator.IrisAnswerGenerator()

        for x in range(len(ag._IrisAnswerGenerator__past_states)):
            ag.add_frame_to_queue("YES")        

        ag.add_frame_to_queue("NO")
  
        self.assertEqual(ag.determine_answer(), Answer.YES)
    
    def test_iris_no_series_all_nos(self):
        ag = AnswerGenerator.IrisAnswerGenerator()      
        
        for x in range(len(ag._IrisAnswerGenerator__past_states)):
            ag.add_frame_to_queue("NO")

        self.assertEqual(ag.determine_answer(), Answer.NO)
    
    def test_iris_no_series_one_yes(self):
        ag = AnswerGenerator.IrisAnswerGenerator()        
        
        for x in range(len(ag._IrisAnswerGenerator__past_states)):
            ag.add_frame_to_queue("NO")

        ag.add_frame_to_queue("YES")

        self.assertEqual(ag.determine_answer(), Answer.NO)
    
    def test_iris_undefined_series_mixed(self):
        ag = AnswerGenerator.IrisAnswerGenerator()        

        for x in range(ag.QUEUE_SIZE):

            if x % 3 == 0:
                ag.add_frame_to_queue("YES")
            elif x % 2 == 0:
                ag.add_frame_to_queue("NO")
            else:
                ag.add_frame_to_queue("NEUTRAL")

        self.assertEqual(ag.determine_answer(), Answer.UNDEFINED)
    
    def test_iris_undefined_series_init(self):
        ag = AnswerGenerator.IrisAnswerGenerator()        

        self.assertEqual(ag.determine_answer(), Answer.UNDEFINED)
    
    def test_iris_undefined_series_clear(self):
        ag = AnswerGenerator.IrisAnswerGenerator()

        for x in range(len(ag._IrisAnswerGenerator__past_states)):
            ag.add_frame_to_queue("YES")

        ag.clear_queue()

        self.assertEqual(ag.determine_answer(), Answer.UNDEFINED)
    
    def test_iris_undefined_series_neutral(self):
        ag = AnswerGenerator.IrisAnswerGenerator()        

        for x in range(len(ag._IrisAnswerGenerator__past_states)):
            ag.add_frame_to_queue("NEUTRAL")

        self.assertEqual(ag.determine_answer(), Answer.UNDEFINED)

    def test_iris_add_invalid_frame(self):
        with self.assertRaises(Exception) as context:
            ag = AnswerGenerator.IrisAnswerGenerator()        
            ag.add_frame_to_queue("San Pellegrino")
            
        self.assertTrue("IrisAnswerGenerator: Invalid state cannot be added to queue" in str(context.exception))