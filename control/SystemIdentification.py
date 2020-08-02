# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 16:01:30 2020

@author: Rushad
"""

import pandas as pd
import numpy as np
import tensorflow
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Activation, Dropout, Dense
from tensorflow.keras.layers import Flatten, LSTM
from tensorflow.keras.layers import GlobalMaxPooling1D
from tensorflow.keras.models import Model
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.layers import Input
from tensorflow.keras.layers import Bidirectional

class SystemIdentification():
    
    def __init__(self, path_to_csv):
        
        data = pd.read_csv(path_to_csv)
        self._x = data[["x", "u"]].to_numpy()
        self._x_dot = data[["x_dot"]].to_numpy()
        self._y = data[["y"]].to_numpy()
        
    def solve(self):
        
        model = Sequential()
        model.add(Dense(12, input_dim=2, activation='relu'))
        model.add(Dense(8, activation='sigmoid'))
        model.add(Dense(1, activation='relu'))
        model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])
        print(model.summary())
        model.fit(self._x, self._x_dot, epochs=150, batch_size=10)