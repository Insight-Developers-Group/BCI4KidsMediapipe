import abc

class DFGeneratorInterface(metaclass=abc.ABCMeta):
    
    @staticmethod
    @abc.abstractmethod
    def generateDF(self, image):
        """Return a pandas dataframe """
        raise NotImplementedError


class IrisDFGenerator(DFGeneratorInterface):
    """Facial Landmark Dataframe Generator"""

    @staticmethod
    def generateDF(image):
        """Overrides DFGeneratorInterface.generateDF()"""
        IrisDFGenerator.get_iris_Landmarks(image)
        pass

    @staticmethod
    def get_iris_Landmarks(image):
        """get landmarks for iris and format dataframe appropriately"""
        pass


class FacialDFGenerator(DFGeneratorInterface):
    """Facial Landmark Dataframe Generator"""

    @staticmethod
    def generateDF(image):
        """Overrides DFGeneratorInterface.generateDF()"""
        FacialDFGenerator.get_face_Landmarks(image)
        pass
    
    @staticmethod
    def get_face_Landmarks(image):
        """get landmarks for face and format dataframe appropriately"""
        pass

