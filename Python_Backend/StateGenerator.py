import pickle
import pandas as pd

class ModelStates:
    
    FACE_STATES = ["NEUTRAL", "SMILE", "FROWN"]
    IRIS_STATES = ["EYES_UP", "EYES_DOWN", "EYES_LEFT", "EYES_RIGHT", "EYES_CENTRE"]


class StateGenerator:
    def __init__(self, model_path, model_type):
        self.model_path = model_path
        self.model_type = model_type
        self.states = None
        if (self.model_type == "FACE"):
            self.states = ModelStates.FACE_STATES
        elif (self.model_type == "IRIS"):
            self.states = ModelStates.IRIS_STATES
        else:
            raise ValueError(model_type)

    def get_model_path(self):
        return self.model_path
    def get_model_type(self):
        return self.model_type
    
    def get_state(self, img_df):
        with open(self.model_path, 'rb') as f:
            model = pickle.load(f)
            #body_language_class is a number between 0 and len(states -1) state numbers correspond to model
            #i.e. for FACE: 0 = Neutral, 1 = Smile, 2 = Frown
            body_language_class = model.predict(img_df)[0]
            return self.states[int(body_language_class)]