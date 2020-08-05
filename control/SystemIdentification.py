# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 16:01:30 2020

@author: Rushad
"""

import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

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
        
        self._model = Sequential()
        self._model.add(Dense(self._x.shape[0], input_dim=3, activation='sigmoid'))
        self._model.add(Dense(self._x.shape[0]/2, activation='sigmoid'))
        self._model.add(Dense(2, activation='relu'))
        self._model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])
        self._model.fit(self._x, self._x_dot, epochs=num_epochs, batch_size=10)
        
    def model(self):
        
        def sigmoid(z):
            a = 1 / (1 + np.exp(-z))
            return a
        
        num_layers = len(self._model.layers)
        num_neurons = [12, 8, 1]
        activation_dict = {}
        prev_op = self._x
        
        for l in range(num_layers):
            
            try:
                z = self._model.layers[l].get_weights()[0].T@prev_op.T
                a = sigmoid(z)
                activation_dict["a"+str(l+1)] = a
                prev_op = a
            
            except ValueError:
                z = self._model.layers[l].get_weights()[0].T@prev_op
                a = sigmoid(z)
                activation_dict["a"+str(l+1)] = a
                prev_op = a
                
        return activation_dict