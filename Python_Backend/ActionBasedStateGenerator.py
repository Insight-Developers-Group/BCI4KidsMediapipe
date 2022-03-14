import pickle
import re
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import TensorBoard
import numpy as np

class ModelStates:
    
    STATES = ["YES", "NEUTRAL", "NO"]


class ActionBasedStateGenerator:
    def __init__(self, model_path, seqLen):
        self.model_path = model_path
        self.states = ModelStates.STATES
        if seqLen <0:
            raise ValueError("Sequence Length Cannot be Less than 0")
        self.seqLen = seqLen;    

    def get_model_path(self):
        return self.model_path
    def get_sequence_length(self):
        return self.seqLen
    
    def get_state(self, sequence):
        model = Sequential()
        model.add(LSTM(64, return_sequences=True, activation='relu', input_shape=(self.seqLen, 330)))
        model.add(LSTM(128, return_sequences=True, activation='relu'))
        model.add(LSTM(64, return_sequences=False, activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(self.states.shape[0], activation='softmax'))
        res = model.predict(np.expand_dims(sequence, axis=0))[0]
        print(res)
        return res