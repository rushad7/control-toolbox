# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 16:01:30 2020

@author: Rushad
"""

import warnings
import numpy as np
import pandas as pd
from .system import StateSpace
from tensorflow.keras import initializers
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential

warnings.filterwarnings("ignore")

class SystemIdentification():
    
    def __init__(self, path_x, path_u, path_x_dot, path_y):
        
        data_x = pd.read_csv(path_x)
        data_x_dot = pd.read_csv(path_x_dot)
        data_u = pd.read_csv(path_u)
        data_y = pd.read_csv(path_y)
        
        self._x = (data_x.join(data_u)).to_numpy()
        self._x_dot = data_x_dot.to_numpy()
        self._y = data_y.to_numpy()
        
    def fit(self, num_epochs=500):
        
        self._stateModel = Sequential()
        self._stateModel.add(Dense(self._x.shape[0], input_dim=3, activation='sigmoid', kernel_initializer=initializers.glorot_normal()))
        self._stateModel.add(Dense(self._x.shape[0]/2, activation='sigmoid'))
        self._stateModel.add(Dense(2, activation='relu'))
        self._stateModel.compile(loss='mse', optimizer='adam', metrics=['accuracy'])
        self._stateModel.fit(self._x, self._x_dot, epochs=num_epochs, batch_size=10)
        
        self._outputModel = Sequential()
        self._outputModel.add(Dense(self._x.shape[0], input_dim=3, activation='sigmoid', kernel_initializer=initializers.glorot_normal()))
        self._outputModel.add(Dense(self._x.shape[0]/2, activation='sigmoid'))
        self._outputModel.add(Dense(1, activation='relu'))
        self._outputModel.compile(loss='mse', optimizer='adam', metrics=['accuracy'])
        self._outputModel.fit(self._x, self._y, epochs=num_epochs, batch_size=10)
        
    def model(self):
        
        hyp_state = self._stateModel.predict(self._x)
        hyp_output = self._stateModel.predict(self._x)
        print(hyp_output.shape)
        A = print(np.linalg.pinv(self._x).shape)#@hyp_state
        C = print(np.linalg.pinv(self._x).shape)
        
        B = D = 0
        
        ss_model = StateSpace(A, B, C, D)
        
        return ss_model