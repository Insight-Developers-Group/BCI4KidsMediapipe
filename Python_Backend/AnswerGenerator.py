import abc
from enum import Enum
from StateGenerator import ModelStates

class Answer(Enum):
    NO = 0
    YES = 1
    UNDEFINED = 2

class FaceState(Enum):
    NEUTRAL = 0
    SMILE = 1 
    FROWN = 2

class IrisState(Enum):
    EYES_UP = 0
    EYES_DOWN = 1
    EYES_LEFT = 2
    EYES_RIGHT = 3
    EYES_CENTER = 4
    INVALID_INIT = 5



class AnswerGeneratorInterface(metaclass=abc.ABCMeta):


    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError


    @abc.abstractmethod
    def clear_queue(self):
        """Removes all elements from the queue"""
        raise NotImplementedError


    @abc.abstractmethod
    def add_frame_to_queue(self):
        """Removes all elements from the queue"""
        raise NotImplementedError


    @abc.abstractmethod
    def determine_answer(self):
        """looks at the current queue of frames and passes along a yes/no or raises an error"""
        raise NotImplementedError




class IrisAnswerGenerator(AnswerGeneratorInterface):

    # Tuning Variables
    NUM_OF_UP_DOWN_PATTERNS_FOR_YES = 3
    NUM_OF_LEFT_RIGHT_PATTERNS_FOR_NO = 3

    FRAME_QUEUE_SIZE = 30
    STATE_QUEUE_SIZE = max(NUM_OF_LEFT_RIGHT_PATTERNS_FOR_NO, NUM_OF_UP_DOWN_PATTERNS_FOR_YES) * 2

    # Required number of frames in __past_frames queue for state to be added to __past_states queue
    FRAMES_FOR_STATE_LIST = [25,  # eyes_up
                             25,  # eyes_down
                             25,  # eyes_left
                             25,  # eyes_right
                             25]  # eyes_center

    INVALID_BUFFER = FRAME_QUEUE_SIZE * 2 # Number of frames queue can be invalid (no state) before an invalid state is added to __past_states

    INIT_STATE = "INIT"

    __frames_with_invalid_state = 0

    __past_frames = []
    __past_states = []

    __state_counters = [] # [eyes_left_counter, eyes_right_counter, eyes_up_counter, eyes_down_counter, eyes_center_counter]


    def __init__(self):
        
       self.clear_queue()


    def clear_queue(self):
        """Reinitializes queues"""

        __frames_with_invalid_state = 0

        self.__past_frames.clear()
        self.__past_states.clear()
        self.__state_counters.clear()

        for x in range(len(ModelStates.IRIS_STATES)):
            self.__state_counters.append(0)
        
        for x in range(self.FRAME_QUEUE_SIZE):
          self.__past_frames.append(self.INIT_STATE)

        for x in range(self.STATE_QUEUE_SIZE):
          self.__past_states.append(self.INIT_STATE)


    def add_frame_to_queue(self, frame):
        """Adds an element to the queue"""

        for face_frame in ModelStates.IRIS_STATES:

            if face_frame == frame:
                popped_frame = self.__past_frames.pop(0)
                self.__past_frames.append(frame)

                self.__update_counters(popped_frame, frame)

                return
        
        raise Exception("IrisAnswerGenerator: Invalid frame cannot be added to queue")


    def __update_counters(self, popped_frame, added_frame):
        """Increment and decrement counters corresponding to the frame added or removed from __past_frames queue"""
        
        for x in range(len(ModelStates.IRIS_STATES)):

            if ModelStates.IRIS_STATES[x] == popped_frame:
                
                self.__state_counters[x] -= 1
            
            elif ModelStates.IRIS_STATES[x] == added_frame:

                self.__state_counters[x] += 1

        return


    def determine_answer(self):
        """Returns Yes, No, Undefined, or Error based on current states in queue"""

        self.__update_past_states()

        if self.__determine_yes_series():
            return Answer.YES

        elif self.__determine_no_series():
            return Answer.NO
        
        return Answer.UNDEFINED
        

    def __update_past_states(self):

        for x in range(len(self.__state_counters)):

            if self.__state_counters[x] >= self.FRAMES_FOR_STATE_LIST[x]:

                self.__add_state_to_queue(ModelStates.IRIS_STATES[x])
                self.__frames_with_invalid_state = 0
                return

        self.__frames_with_invalid_state += 1

        if self.__frames_with_invalid_state > self.INVALID_BUFFER:

            self.__add_state_to_queue(ModelStates.IRIS_STATES[IrisState.INVALID_INIT])


    def __add_state_to_queue(self, state):

        # Check that the last state added is not the same as the current state
        if self.__past_states[self.STATE_QUEUE_SIZE - 1] != state:

            self.__past_states.append(state)
            self.__past_states.pop()


    def __determine_yes_series(self):
        """Returns true if there is a "Yes" series"""
        
        num_of_smile = 0

        for face_frame in self.__past_frames:
            
            if face_frame == ModelStates.FACE_STATES[FaceState.SMILE.value]:
            
                num_of_smile += 1

        if (num_of_smile >= self.NUM_OF_FRAMES_TO_CREATE_SERIES):

            return True

        return False



    def __determine_no_series(self):
        """Returns true if there is a "No" series"""

        num_of_frown = 0

        for face_frame in self.__past_frames:
            
            if face_frame == ModelStates.FACE_STATES[FaceState.FROWN.value]:
            
                num_of_frown += 1

        if (num_of_frown >= self.NUM_OF_FRAMES_TO_CREATE_SERIES):

            return True

        return False





class FacialAnswerGenerator(AnswerGeneratorInterface):

    # Tuning Varaibles
    QUEUE_SIZE = 30
    NUM_OF_STATES_TO_CREATE_YES_SERIES = 25
    NUM_OF_STATES_TO_CREATE_NO_SERIES = 25

    INIT_STATE = "INIT"

    __past_frames = []


    def __init__(self):
        
       self.clear_queue()



    def clear_queue(self):
        """Reinitializes queue"""

        self.__past_frames.clear()

        for x in range(self.QUEUE_SIZE):
          self.__past_frames.append(self.INIT_STATE)



    def add_frame_to_queue(self, frame):
        """Adds an element to the queue"""

        for face_frame in ModelStates.FACE_STATES:

            if face_frame == frame:
                self.__past_frames.pop(0)
                self.__past_frames.append(frame)

                return
        
        raise Exception("FacialAnswerGenerator: Invalid frame cannot be added to queue")



    def determine_answer(self):
        """Returns Yes, No, Undefined, or Error based on current frames in queue"""

        if self.__determine_yes_series():
            return Answer.YES

        elif self.__determine_no_series():
            return Answer.NO
        
        return Answer.UNDEFINED
        


    def __determine_yes_series(self):
        """Returns true if there is a "Yes" series"""
        
        num_of_smile = 0

        for face_frame in self.__past_frames:
            
            if face_frame == ModelStates.FACE_STATES[FaceState.SMILE.value]:
            
                num_of_smile += 1

        if (num_of_smile >= self.NUM_OF_FRAMES_TO_CREATE_YES_SERIES):

            return True

        return False



    def __determine_no_series(self):
        """Returns true if there is a "No" series"""

        num_of_frown = 0

        for face_frame in self.__past_frames:
            
            if face_frame == ModelStates.FACE_STATES[FaceState.FROWN.value]:
            
                num_of_frown += 1

        if (num_of_frown >= self.NUM_OF_FRAMES_TO_CREATE_NO_SERIES):

            return True

        return False