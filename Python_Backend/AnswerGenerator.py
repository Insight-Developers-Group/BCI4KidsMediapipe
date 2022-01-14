class AnswerGeneratorInterface(metaclass=abc.ABCMeta):
	pastStates = []
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'load_data_source') and 
                callable(subclass.load_data_source) and 
                hasattr(subclass, 'extract_text') and 
                callable(subclass.extract_text) or 
                NotImplemented)

    @abc.abstractmethod
    def determineAnswer(self):
        """looks at the current queue of states and passes along a yes/no or raises an error"""
        raise NotImplementedError

	@abc.abstractmethod
    def determineYesSeries(self):
        """the technical stuff surrounding determining what constitutes a yes"""
        raise NotImplementedError

	@abc.abstractmethod
    def determineNoSeries(self):
        """the technical stuff surrounding determining what constitutes a no"""
        raise NotImplementedError
    @abc.abstractmethod
    def clearQueue(self):
        """Removes all elements from the queue"""
        raise NotImplementedError
    @abc.abstractmethod
    def addStateToQueue(self):
        """Removes all elements from the queue"""
        raise NotImplementedError

class IrisDFGenerator(DFGeneratorInterface):
    """Facial Landmark Dataframe Generator"""
    def generateDF(self, image):
        """Overrides DFGeneratorInterface.generateDF()"""
		get_iris_Landmarks(image)
        pass

	def get_iris_Landmarks(image):
		"""get landmarks for iris and format dataframe appropriately"""
        pass


class FacialDFGenerator(DFGeneratorInterface):
    """Facial Landmark Dataframe Generator"""
    def generateDF(self, image):
        """Overrides DFGeneratorInterface.generateDF()"""
		get_face_Landmarks(image)
        pass

	def get_face_Landmarks(image):
		"""get landmarks for face and format dataframe appropriately"""
        pass

