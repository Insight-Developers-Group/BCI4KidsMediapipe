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


class AnswerGeneratorInterface(metaclass=abc.ABCMeta):


    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError


    @abc.abstractmethod
    def clear_queue(self):
        """Removes all elements from the queue"""
        raise NotImplementedError


    @abc.abstractmethod
    def add_state_to_queue(self):
        """Removes all elements from the queue"""
        raise NotImplementedError


    @abc.abstractmethod
    def determine_answer(self):
        """looks at the current queue of states and passes along a yes/no or raises an error"""
        raise NotImplementedError




class IrisAnswerGenerator(AnswerGeneratorInterface):

    QUEUE_SIZE = 10
    __past_states = [QUEUE_SIZE]

 
    def __init__(self):
        raise NotImplementedError

    def clear_queue(self):
        """Removes all elements from the queue"""
        raise NotImplementedError


    def add_state_to_queue(self):
        """Removes all elements from the queue"""
        raise NotImplementedError


    def determine_answer(self):
        """looks at the current queue of states and passes along a yes/no or raises an error"""
        raise NotImplementedError


    def __determine_yes_series(self):
        """Returns true if there is a "Yes" series"""
        raise NotImplementedError


    def __determine_no_series(self):
        """Returns true if there is a "No" series"""
        raise NotImplementedError




class FacialAnswerGenerator(AnswerGeneratorInterface):

    QUEUE_SIZE = 5
    INIT_STATE = "INIT"
    NUM_OF_STATES_TO_CREATE_SERIES = 4

    __past_states = []


    def __init__(self):
        
       self.clear_queue()



    def clear_queue(self):
        """Reinitializes queue"""

        self.__past_states.clear()

        for x in range(self.QUEUE_SIZE):
          self.__past_states.append(self.INIT_STATE)



    def add_state_to_queue(self, state):
        """Adds an element to the queue"""

        for face_state in ModelStates.FACE_STATES:

            if face_state == state:
                self.__past_states.pop(0)
                self.__past_states.append(state)

                return
        
        raise Exception("FacialAnswerGenerator: Invalid state cannot be added to queue")



    def determine_answer(self):
        """Returns Yes, No, Undefined, or Error based on current states in queue"""

        if self.__determine_yes_series():
            return Answer.YES

        elif self.__determine_no_series():
            return Answer.NO
        
        return Answer.UNDEFINED
        


    def __determine_yes_series(self):
        """Returns true if there is a "Yes" series"""
        
        num_of_smile = 0

        for face_state in self.__past_states:
            
            if face_state == ModelStates.FACE_STATES[FaceState.SMILE.value]:
            
                num_of_smile += 1

        if (num_of_smile >= self.NUM_OF_STATES_TO_CREATE_SERIES):

            return True

        return False



    def __determine_no_series(self):
        """Returns true if there is a "No" series"""

        num_of_frown = 0

        for face_state in self.__past_states:
            
            if face_state == ModelStates.FACE_STATES[FaceState.FROWN.value]:
            
                num_of_frown += 1

        if (num_of_frown >= self.NUM_OF_STATES_TO_CREATE_SERIES):

            return True

        return False