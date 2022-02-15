import unittest
import sys

sys.path.insert(0, '../')

import AnswerGenerator
from AnswerGenerator import Answer

class TestAnswerGenerator(unittest.TestCase):

    # Unit tests for FacialAnswerGenerator

    def test_add_smile_to_queue(self):

        ag = AnswerGenerator.FacialAnswerGenerator()        
        ag.add_frame_to_queue("SMILE")

        self.assertEqual(ag._FacialAnswerGenerator__past_frames[ag.QUEUE_SIZE - 1], "SMILE")

    def test_add_frown_to_queue(self):

        ag = AnswerGenerator.FacialAnswerGenerator()        
        ag.add_frame_to_queue("FROWN")

        self.assertEqual(ag._FacialAnswerGenerator__past_frames[ag.QUEUE_SIZE - 1], "FROWN")

    def test_iris_overfill_queue(self):
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

    def test_facial_add_invalid_frame(self):
        with self.assertRaises(Exception) as context:
            ag = AnswerGenerator.FacialAnswerGenerator()        
            ag.add_frame_to_queue("San Pellegrino")
            
        self.assertTrue("FacialAnswerGenerator: Invalid frame cannot be added to queue" in str(context.exception))

   # Unit tests for IrisAnswerGenerator 

    def test_add_eyes_up_to_queue(self):

        ag = AnswerGenerator.IrisAnswerGenerator()        
        ag.add_frame_to_queue("EYES_UP")

        self.assertEqual(ag._IrisAnswerGenerator__past_frames[ag.FRAME_QUEUE_SIZE - 1], "EYES_UP")

    def test_add_eyes_left_to_queue(self):

        ag = AnswerGenerator.IrisAnswerGenerator()        
        ag.add_frame_to_queue("EYES_LEFT")

        self.assertEqual(ag._IrisAnswerGenerator__past_frames[ag.FRAME_QUEUE_SIZE - 1], "EYES_LEFT")

    def test_iris_overfill_queue(self):
        ag = AnswerGenerator.IrisAnswerGenerator()

        for x in range(ag.FRAME_QUEUE_SIZE * 2):

            if x % 2 == 0:
                ag.add_frame_to_queue("EYES_UP")
            else:
                ag.add_frame_to_queue("EYES_DOWN")

        for x in range(ag.FRAME_QUEUE_SIZE):
            
            if x % 2 == 0:
                self.assertEqual(ag._IrisAnswerGenerator__past_frames[x], "EYES_UP")
            else:
                self.assertEqual(ag._IrisAnswerGenerator__past_frames[x], "EYES_DOWN")

    def test_iris_clear_queue(self):

        ag = AnswerGenerator.IrisAnswerGenerator()        
        ag.add_frame_to_queue("EYES_RIGHT")
        ag.clear_queue()

        for frame in ag._IrisAnswerGenerator__past_frames:
            self.assertEqual(frame, "INIT")

    def test_iris_clear_full_queue(self):
        ag = AnswerGenerator.IrisAnswerGenerator()        
        
        for x in range(ag.FRAME_QUEUE_SIZE):

            if x % 2 == 0:
                ag.add_frame_to_queue("EYES_LEFT")
            else:
                ag.add_frame_to_queue("EYES_RIGHT")

        ag.clear_queue()

        for frame in ag._IrisAnswerGenerator__past_frames:
            self.assertEqual(frame, "INIT")

    def test_iris_clear_empty_queue(self):

        ag = AnswerGenerator.IrisAnswerGenerator()        
        ag.clear_queue()

        for frame in ag._IrisAnswerGenerator__past_frames:
            self.assertEqual(frame, "INIT")

    def test_add_eyes_up_state_to_queue(self):
        ag = AnswerGenerator.IrisAnswerGenerator()

        for x in range(ag.FRAMES_FOR_STATE_LIST[AnswerGenerator.IrisState.EYES_UP.value]):
            
            ag.add_frame_to_queue("EYES_UP")

        self.assertEqual(ag._IrisAnswerGenerator__past_states[ag.STATE_QUEUE_SIZE - 2], "INIT")
        self.assertEqual(ag._IrisAnswerGenerator__past_states[ag.STATE_QUEUE_SIZE - 1], "EYES_UP")
    
    def test_add_eyes_down_state_to_queue(self):
        ag = AnswerGenerator.IrisAnswerGenerator()

        for x in range(ag.FRAMES_FOR_STATE_LIST[AnswerGenerator.IrisState.EYES_DOWN.value]):
            
            ag.add_frame_to_queue("EYES_DOWN")

        self.assertEqual(ag._IrisAnswerGenerator__past_states[ag.STATE_QUEUE_SIZE - 2], "INIT")
        self.assertEqual(ag._IrisAnswerGenerator__past_states[ag.STATE_QUEUE_SIZE - 1], "EYES_DOWN")
    
    def test_add_eyes_left_state_to_queue(self):
        ag = AnswerGenerator.IrisAnswerGenerator()

        for x in range(ag.FRAMES_FOR_STATE_LIST[AnswerGenerator.IrisState.EYES_LEFT.value]):
            
            ag.add_frame_to_queue("EYES_LEFT")

        self.assertEqual(ag._IrisAnswerGenerator__past_states[ag.STATE_QUEUE_SIZE - 2], "INIT")
        self.assertEqual(ag._IrisAnswerGenerator__past_states[ag.STATE_QUEUE_SIZE - 1], "EYES_LEFT")

    def test_add_eyes_up_state_to_queue(self):
        ag = AnswerGenerator.IrisAnswerGenerator()

        for x in range(ag.FRAMES_FOR_STATE_LIST[AnswerGenerator.IrisState.EYES_RIGHT.value]):
            
            ag.add_frame_to_queue("EYES_RIGHT")
        
        self.assertEqual(ag._IrisAnswerGenerator__past_states[ag.STATE_QUEUE_SIZE - 2], "INIT")
        self.assertEqual(ag._IrisAnswerGenerator__past_states[ag.STATE_QUEUE_SIZE - 1], "EYES_RIGHT")

    def test_add_eyes_centre_state_to_queue(self):
        ag = AnswerGenerator.IrisAnswerGenerator()

        for x in range(ag.FRAMES_FOR_STATE_LIST[AnswerGenerator.IrisState.EYES_CENTER.value]):
            
            ag.add_frame_to_queue("EYES_CENTRE")

        self.assertEqual(ag._IrisAnswerGenerator__past_states[ag.STATE_QUEUE_SIZE - 2], "INIT")
        self.assertEqual(ag._IrisAnswerGenerator__past_states[ag.STATE_QUEUE_SIZE - 1], "EYES_CENTRE")

    def test_add_invalid_state_to_queue(self):
        ag = AnswerGenerator.IrisAnswerGenerator()

        for x in range(ag.INVALID_BUFFER):
            
            if x % 2 == 0:
                ag.add_frame_to_queue("EYES_UP")
            else:
                ag.add_frame_to_queue("EYES_DOWN")  

        self.assertEqual(ag._IrisAnswerGenerator__past_states[ag.STATE_QUEUE_SIZE - 2], "INIT")
        self.assertEqual(ag._IrisAnswerGenerator__past_states[ag.STATE_QUEUE_SIZE - 1], "INVALID")

    def test_can_add_only_one_invalid_state_to_queue(self):
        ag = AnswerGenerator.IrisAnswerGenerator()

        for x in range(ag.INVALID_BUFFER + ag.MAX_FRAMES_PER_STATE + 1):
            
            if x % 2 == 0:
                ag.add_frame_to_queue("EYES_UP")
            else:
                ag.add_frame_to_queue("EYES_DOWN")  

        self.assertEqual(ag._IrisAnswerGenerator__past_states[ag.STATE_QUEUE_SIZE - 3], "INIT")
        self.assertEqual(ag._IrisAnswerGenerator__past_states[ag.STATE_QUEUE_SIZE - 2], "INIT")
        self.assertEqual(ag._IrisAnswerGenerator__past_states[ag.STATE_QUEUE_SIZE - 1], "INVALID")

    def test_add_two_eyes_up_states_to_queue(self):
        ag = AnswerGenerator.IrisAnswerGenerator()

        for x in range(ag.FRAMES_FOR_STATE_LIST[AnswerGenerator.IrisState.EYES_UP.value] + ag.MAX_FRAMES_PER_STATE + 1):
            
            ag.add_frame_to_queue("EYES_UP") 

        self.assertEqual(ag._IrisAnswerGenerator__past_states[ag.STATE_QUEUE_SIZE - 3], "INIT")
        self.assertEqual(ag._IrisAnswerGenerator__past_states[ag.STATE_QUEUE_SIZE - 2], "EYES_UP")
        self.assertEqual(ag._IrisAnswerGenerator__past_states[ag.STATE_QUEUE_SIZE - 1], "EYES_UP")

    def test_add_three_eyes_up_states_to_queue(self):
        ag = AnswerGenerator.IrisAnswerGenerator()

        for x in range(ag.FRAMES_FOR_STATE_LIST[AnswerGenerator.IrisState.EYES_UP.value] + (ag.MAX_FRAMES_PER_STATE + 1) *2):
            
            ag.add_frame_to_queue("EYES_UP") 

        self.assertEqual(ag._IrisAnswerGenerator__past_states[ag.STATE_QUEUE_SIZE - 4], "INIT")
        self.assertEqual(ag._IrisAnswerGenerator__past_states[ag.STATE_QUEUE_SIZE - 3], "EYES_UP")
        self.assertEqual(ag._IrisAnswerGenerator__past_states[ag.STATE_QUEUE_SIZE - 2], "EYES_UP")
        self.assertEqual(ag._IrisAnswerGenerator__past_states[ag.STATE_QUEUE_SIZE - 1], "EYES_UP")
    
    def test_add_two_eyes_up_and_one_eyes_down_states_to_queue(self):
        ag = AnswerGenerator.IrisAnswerGenerator()

        for x in range(ag.FRAMES_FOR_STATE_LIST[AnswerGenerator.IrisState.EYES_UP.value] + ag.MAX_FRAMES_PER_STATE + 1):
            
            ag.add_frame_to_queue("EYES_UP") 
        
        ag.add_frame_to_queue("EYES_RIGHT") 
        ag.add_frame_to_queue("EYES_LEFT") 

        for x in range(ag.FRAMES_FOR_STATE_LIST[AnswerGenerator.IrisState.EYES_DOWN.value]):
            
            ag.add_frame_to_queue("EYES_DOWN") 

        self.assertEqual(ag._IrisAnswerGenerator__past_states[ag.STATE_QUEUE_SIZE - 4], "INIT")
        self.assertEqual(ag._IrisAnswerGenerator__past_states[ag.STATE_QUEUE_SIZE - 3], "EYES_UP")
        self.assertEqual(ag._IrisAnswerGenerator__past_states[ag.STATE_QUEUE_SIZE - 2], "EYES_UP")
        self.assertEqual(ag._IrisAnswerGenerator__past_states[ag.STATE_QUEUE_SIZE - 1], "EYES_DOWN")

    def test_determine_yes_series(self):
        ag = AnswerGenerator.IrisAnswerGenerator()

        for i in range(ag.NUM_OF_UP_DOWN_PATTERNS_FOR_YES):

            for x in range(ag.FRAMES_FOR_STATE_LIST[AnswerGenerator.IrisState.EYES_UP.value]):
            
                ag.add_frame_to_queue("EYES_UP") 
            
            for x in range(ag.FRAMES_FOR_STATE_LIST[AnswerGenerator.IrisState.EYES_UP.value]):
            
                ag.add_frame_to_queue("EYES_DOWN") 
        
        self.assertEqual(ag.determine_answer(), Answer.YES)

    def test_determine_yes_series_reverse(self):
        ag = AnswerGenerator.IrisAnswerGenerator()

        for i in range(ag.NUM_OF_UP_DOWN_PATTERNS_FOR_YES):

            for x in range(ag.FRAMES_FOR_STATE_LIST[AnswerGenerator.IrisState.EYES_DOWN.value]):
            
                ag.add_frame_to_queue("EYES_DOWN") 
            
            for x in range(ag.FRAMES_FOR_STATE_LIST[AnswerGenerator.IrisState.EYES_UP.value]):
            
                ag.add_frame_to_queue("EYES_UP") 
        
        self.assertEqual(ag.determine_answer(), Answer.YES)

    def test_determine_no_series(self):
        ag = AnswerGenerator.IrisAnswerGenerator()

        for i in range(ag.NUM_OF_LEFT_RIGHT_PATTERNS_FOR_NO):

            for x in range(ag.FRAMES_FOR_STATE_LIST[AnswerGenerator.IrisState.EYES_LEFT.value]):
            
                ag.add_frame_to_queue("EYES_LEFT") 
            
            for x in range(ag.FRAMES_FOR_STATE_LIST[AnswerGenerator.IrisState.EYES_RIGHT.value]):
            
                ag.add_frame_to_queue("EYES_RIGHT") 
        
        self.assertEqual(ag.determine_answer(), Answer.NO)

    def test_determine_no_series_reverse(self):
        ag = AnswerGenerator.IrisAnswerGenerator()

        for i in range(ag.NUM_OF_LEFT_RIGHT_PATTERNS_FOR_NO):

            for x in range(ag.FRAMES_FOR_STATE_LIST[AnswerGenerator.IrisState.EYES_RIGHT.value]):
            
                ag.add_frame_to_queue("EYES_RIGHT") 
            
            for x in range(ag.FRAMES_FOR_STATE_LIST[AnswerGenerator.IrisState.EYES_LEFT.value]):
            
                ag.add_frame_to_queue("EYES_LEFT") 
        
        self.assertEqual(ag.determine_answer(), Answer.NO)

    def test_determine_undefined_series_0(self):
        ag = AnswerGenerator.IrisAnswerGenerator()

        for i in range(ag.NUM_OF_LEFT_RIGHT_PATTERNS_FOR_NO + 1):

            for x in range(ag.FRAMES_FOR_STATE_LIST[AnswerGenerator.IrisState.EYES_LEFT.value]):
            
                ag.add_frame_to_queue("EYES_LEFT") 
            
            for x in range(ag.FRAMES_FOR_STATE_LIST[AnswerGenerator.IrisState.EYES_RIGHT.value]):
            
                ag.add_frame_to_queue("EYES_UP") 
            
            for x in range(ag.FRAMES_FOR_STATE_LIST[AnswerGenerator.IrisState.EYES_RIGHT.value]):
            
                ag.add_frame_to_queue("EYES_RIGHT") 
        
        self.assertEqual(ag.determine_answer(), Answer.UNDEFINED)

    def test_determine_no_series_with_eyes_up_frames(self):
        ag = AnswerGenerator.IrisAnswerGenerator()

        for i in range(ag.NUM_OF_LEFT_RIGHT_PATTERNS_FOR_NO + 1):

            for x in range(ag.FRAMES_FOR_STATE_LIST[AnswerGenerator.IrisState.EYES_LEFT.value]):
            
                ag.add_frame_to_queue("EYES_LEFT") 

                if x % 5 == 0:
                    ag.add_frame_to_queue("EYES_UP") 
            
            for x in range(ag.FRAMES_FOR_STATE_LIST[AnswerGenerator.IrisState.EYES_RIGHT.value]):
            
                ag.add_frame_to_queue("EYES_RIGHT") 

                if x % 5 == 0:
                    ag.add_frame_to_queue("EYES_UP") 
        
        self.assertEqual(ag.determine_answer(), Answer.NO)

    def test_determine_yes_series_with_eyes_centre_frames(self):
        ag = AnswerGenerator.IrisAnswerGenerator()

        for i in range(ag.NUM_OF_LEFT_RIGHT_PATTERNS_FOR_NO + 1):

            for x in range(ag.FRAMES_FOR_STATE_LIST[AnswerGenerator.IrisState.EYES_LEFT.value]):
            
                ag.add_frame_to_queue("EYES_LEFT") 

                if x % 5 == 0:
                    ag.add_frame_to_queue("EYES_CENTRE") 
            
            for x in range(ag.FRAMES_FOR_STATE_LIST[AnswerGenerator.IrisState.EYES_RIGHT.value]):
            
                ag.add_frame_to_queue("EYES_RIGHT") 

                if x % 6 == 0:
                    ag.add_frame_to_queue("EYES_CENTRE") 

    def test_iris_add_invalid_frame(self):
        with self.assertRaises(Exception) as context:
            ag = AnswerGenerator.FacialAnswerGenerator()        
            ag.add_frame_to_queue("San Pellegrino")
            
        self.assertTrue("FacialAnswerGenerator: Invalid frame cannot be added to queue" in str(context.exception))