import abc
from enum import Enum
from StateGenerator import ModelStates

class InvalidStateException(Exception):
    pass

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



class IrisAnswerGenerator(AnswerGeneratorInterface):

    # Tuning Variables
    NUM_OF_UP_DOWN_PATTERNS_FOR_YES   = 3
    NUM_OF_LEFT_RIGHT_PATTERNS_FOR_NO = 3

    FRAME_QUEUE_SIZE = 30
    STATE_QUEUE_SIZE = max(NUM_OF_LEFT_RIGHT_PATTERNS_FOR_NO, NUM_OF_UP_DOWN_PATTERNS_FOR_YES) * 2

    # Required number of frames in __past_frames queue for state to be added to __past_states queue
    FRAMES_FOR_STATE_LIST = [25,  # eyes_up
                             25,  # eyes_down
                             25,  # eyes_left
                             25,  # eyes_right
                             25]  # eyes_center

    INVALID_BUFFER       = FRAME_QUEUE_SIZE * 2 + 1 # Number of frames queue can be invalid (no state) before an invalid state is added to __past_states
    MAX_FRAMES_PER_STATE = FRAME_QUEUE_SIZE * 6     # Number of frames allowed in one state, before adding state to __past_states queue again

    INIT_STATE = "INIT"

    __frames_in_invalid_state = 0
    __frames_in_current_state = 0        

    __past_frames = []
    __past_states = []

    __state_counters = []  # [eyes_left_counter, eyes_right_counter, eyes_up_counter, eyes_down_counter, eyes_center_counter]


    def __init__(self):
        
       self.clear_queue()


    def clear_queue(self):
        """ Reinitializes queues and clears member variables """

        self.__frames_in_invalid_state = 0
        self.__frames_in_current_state = 0

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
        """ Adds an element to the queue """

        for face_frame in ModelStates.IRIS_STATES:

            if face_frame == frame:
                popped_frame = self.__past_frames.pop(0)
                self.__past_frames.append(frame)

                self.__update_counters(popped_frame, frame)
                self.__update_states_queue()
                return
        
        raise Exception("IrisAnswerGenerator: Invalid frame cannot be added to queue")


    def __update_counters(self, popped_frame, added_frame):
        """ Increment and decrement counters corresponding to the frame added or removed from __past_frames queue """
        
        for x in range(len(ModelStates.IRIS_STATES)):

            if ModelStates.IRIS_STATES[x] == popped_frame:
                self.__state_counters[x] -= 1
            
            if ModelStates.IRIS_STATES[x] == added_frame:
                self.__state_counters[x] += 1

        return


    def determine_answer(self):
        """ Returns Yes, No, or Undefined based on current states in queue """

        if self.__determine_series(IrisState.EYES_UP.value, IrisState.EYES_DOWN.value, self.NUM_OF_UP_DOWN_PATTERNS_FOR_YES):
            return Answer.YES

        elif self.__determine_series(IrisState.EYES_RIGHT.value, IrisState.EYES_LEFT.value, self.NUM_OF_LEFT_RIGHT_PATTERNS_FOR_NO):
            return Answer.NO
        
        return Answer.UNDEFINED
        

    def __update_states_queue(self):
        """ Determines the current state and adds it to __past_states queue """

        # Loops over __state_counters to determine current state
        for x in range(len(self.__state_counters)):

            if self.__state_counters[x] >= self.FRAMES_FOR_STATE_LIST[x]:

                self.__frames_in_invalid_state = 0

                if self.__add_state_to_queue(ModelStates.IRIS_STATES[x]):
                    self.__frames_in_current_state = 0

                else:
                    self.__frames_in_current_state += 1
                    
                return

        self.__frames_in_invalid_state += 1
        self.__frames_in_current_state = 0

        if self.__frames_in_invalid_state >= self.INVALID_BUFFER:
            self.__add_state_to_queue("INVALID")


    def __add_state_to_queue(self, state):
        """ Retruns True if state is added to __past_states queue """

        # Check that the last state added is not the same as the current state
        if self.__past_states[self.STATE_QUEUE_SIZE - 1] != state or self.__frames_in_current_state >= self.MAX_FRAMES_PER_STATE:

            self.__past_states.append(state)
            self.__past_states.pop(0)

            return True

        return False


    def __determine_series(self, state_0, state_1, num_of_required_patterns):
        """
        Returns True if there is a series given the arguments
        
        Arguments:
            state_0: Enum representing the first state in the pattern
            state_1: Enum representing the second state in the pattern
            num_of_required_patterns: Number of patterns required to create a series
        """

        num_of_up_down_patterns = 0

        for i in range(len(self.__past_states) - 1):
            
            if self.__past_states[i] == ModelStates.IRIS_STATES[state_0] and self.__past_states[i + 1] == ModelStates.IRIS_STATES[state_1]:            
                num_of_up_down_patterns += 1

            elif self.__past_states[i + 1] == ModelStates.IRIS_STATES[state_0] and self.__past_states[i] == ModelStates.IRIS_STATES[state_1]:
                num_of_up_down_patterns += 1
            
            else:
                num_of_up_down_patterns = 0


            if (num_of_up_down_patterns >= num_of_required_patterns * 2 - 1):
                return True

        return False




class FacialAnswerGenerator(AnswerGeneratorInterface):

    # Tuning Varaibles
    QUEUE_SIZE = 30
    NUM_OF_FRAMES_TO_CREATE_YES_SERIES = 25
    NUM_OF_FRAMES_TO_CREATE_NO_SERIES = 25

    INIT_STATE = "INIT"

    __past_frames = []


    def __init__(self):
        
       self.clear_queue()



    def clear_queue(self):
        """ Reinitializes queue """

        self.__past_frames.clear()

        for x in range(self.QUEUE_SIZE):
          self.__past_frames.append(self.INIT_STATE)



    def add_frame_to_queue(self, frame):
        """ Adds frame to the queue """

        for face_frame in ModelStates.FACE_STATES:

            if face_frame == frame:
                self.__past_frames.pop(0)
                self.__past_frames.append(frame)

                return
        

        raise Exception("FacialAnswerGenerator: Invalid frame cannot be added to queue")




    def determine_answer(self):
        """ Returns Yes, No, Undefined, or Error based on current frames in queue """

        if self.__determine_series(FaceState.SMILE.value, self.NUM_OF_FRAMES_TO_CREATE_YES_SERIES):
            return Answer.YES

        elif self.__determine_series(FaceState.FROWN.value, self.NUM_OF_FRAMES_TO_CREATE_NO_SERIES):
            return Answer.NO
        
        return Answer.UNDEFINED



    def __determine_series(self, state, num_of_requied_frames):
        """
        Returns True if there is a series given the arguments
        
        Arguments:
            state: Enum representing the state being checked
            num_of_required_frames: Number of frames required in that state to create a series
        """

        num_of_frames_in_state = 0

        for face_frame in self.__past_frames:
            
            if face_frame == ModelStates.FACE_STATES[state]:
                num_of_frames_in_state += 1

        if (num_of_frames_in_state >= num_of_requied_frames):
            return True

        return False