import numpy as np

from sklearn.base import BaseEstimator
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler


class MockIrisClassifier(BaseEstimator):
    """Class to emulate a predictive model using a simple heuristic."""

    def __init__(self):
        """Set the classes for binary classification"""
        self.n_classes_ = 5
        self.classes_ = np.array([0, 1,2,3,4])

    def fit(
        self,
        features: np.ndarray,
        target: np.ndarray,
        sample_weight: np.ndarray = None
    ):
        """
        Mocks out the fit function for a standard scikit-learn estimator. Since
        the heuristic doesn't rely on any previous data, the function simply
        returns self.

        :param features:
            Ignored.
        :param target:
            Ignored.
        :param sample_weight:
            Ignored.
        :return:
            Returns the estimator without any changes.
        """
        return self

    def predict(self, features: np.ndarray) -> np.ndarray:
        """
        Emulate a machine learning model's behavior. This function will return
        the most probable class for each instance. It only uses the first
        feature of the `features` array.

        If the feature value is less than or equal to 0, it will return a
        class 0. If feature value is greater than zero, it will return a
        class 1.

        :param features:
            Ndarray that corresponds to features used in a classification model.
        :return:
            Predicted class for all instances of `features`.
        """
        return features[0]


import numpy as np

from sklearn.base import BaseEstimator
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler


class MockFaceClassifier(BaseEstimator):
    """Class to emulate a predictive model using a simple heuristic."""

    def __init__(self):
        """Set the classes for binary classification"""
        self.n_classes_ = 3
        self.classes_ = np.array([0, 1,2])

    def fit(
        self,
        features: np.ndarray,
        target: np.ndarray,
        sample_weight: np.ndarray = None
    ):
        """
        Mocks out the fit function for a standard scikit-learn estimator. Since
        the heuristic doesn't rely on any previous data, the function simply
        returns self.

        :param features:
            Ignored.
        :param target:
            Ignored.
        :param sample_weight:
            Ignored.
        :return:
            Returns the estimator without any changes.
        """
        return self

    def predict(self, features: np.ndarray) -> np.ndarray:
        """
        Emulate a machine learning model's behavior. This function will return
        the most probable class for each instance. It only uses the first
        feature of the `features` array.

        If the feature value is less than or equal to 0, it will return a
        class 0. If feature value is greater than zero, it will return a
        class 1.

        :param features:
            Ndarray that corresponds to features used in a classification model.
        :return:
            Predicted class for all instances of `features`.
        """
        return features[0]