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
    NEUTRAL = 0
    YES = 1
    NO = 2


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

    # Tuning Varaibles
    QUEUE_SIZE = 1
    NUM_OF_STATES_TO_CREATE_YES_SERIES = 1
    NUM_OF_STATES_TO_CREATE_NO_SERIES = 1

    INIT_STATE = "INIT"

    __past_states = []


    def __init__(self):
        
       self.clear_queue()



    def clear_queue(self):
        """ Reinitializes queue """

        self.__past_states.clear()

        for x in range(self.QUEUE_SIZE):
          self.__past_states.append(self.INIT_STATE)



    def add_frame_to_queue(self, frame):
        """ Adds state to the queue """

        for face_state in ModelStates.IRIS_STATES:

            if face_state == frame:
                self.__past_states.pop(0)
                self.__past_states.append(frame)

                return
        

        raise Exception("IrisAnswerGenerator: Invalid state cannot be added to queue")




    def determine_answer(self):
        """ Returns Yes, No, Undefined, or Error based on current states in queue """

        if self.__determine_series(IrisState.YES.value, self.NUM_OF_STATES_TO_CREATE_YES_SERIES):
            return Answer.YES

        elif self.__determine_series(IrisState.NO.value, self.NUM_OF_STATES_TO_CREATE_NO_SERIES):
            return Answer.NO
        
        return Answer.UNDEFINED



    def __determine_series(self, state, num_of_requied_states):
        """
        Returns True if there is a series given the arguments
        
        Arguments:
            state: Enum representing the state being checked
            num_of_required_states: Number of states required to create a series
        """

        num_of_states = 0

        for face_frame in self.__past_states:
            
            if face_frame == ModelStates.IRIS_STATES[state]:
                num_of_states += 1

        if (num_of_states >= num_of_requied_states):
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