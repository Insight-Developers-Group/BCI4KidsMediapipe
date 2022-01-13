class DFGeneratorInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'load_data_source') and 
                callable(subclass.load_data_source) and 
                hasattr(subclass, 'extract_text') and 
                callable(subclass.extract_text) or 
                NotImplemented)

    @abc.abstractmethod
    def generateDF(self, image):
        """Return a pandas dataframe """
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

