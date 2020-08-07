# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 16:01:30 2020

@author: Rushad
"""

import numpy as np
import pandas as pd
from sympy import symbols, Matrix
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential

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
        
        def exp(x):
        
            expo = Matrix.zeros(x.shape[0], x.shape[1])    
            for i in range(x.shape[0]):
                for j in range(x.shape[1]):
                    expo[i+j] = np.e**(expo[i+j])
        
            return expo
        
        def sigmoid(z):
            
            exp_z = exp(-z)
            for i in range(exp_z.shape[0]*exp_z.shape[1]):
                exp_z[i] = exp_z[i] + 1
            
            for i in range(exp_z.shape[0]*exp_z.shape[1]):
                exp_z[i] = 1/exp_z[i]
            
            return exp_z
        
        x_str = ""
        for i in range(len(self._x[0])-1):
            x_str = x_str + "x" + str(i+1) + ","
            
        x_str = x_str + "u"
        x_var = symbols(x_str)
        self.x_matrix = Matrix([x_var]).transpose()
        x_matrix = Matrix([x_var]).transpose()
        
        for l in range(len(self._model.layers)):
            try:
                z = Matrix(Matrix(self._model.layers[0].get_weights()[0]).transpose().dot(x_matrix)) + Matrix(self._model.layers[0].get_weights()[1])
                a = sigmoid(z)
                x_matrix = a
            
            except ValueError:
                z = Matrix(Matrix(self._model.layers[0].get_weights()[0]).transpose().dot(x_matrix)) + Matrix(self._model.layers[0].get_weights()[1]).T
                a = sigmoid(z)
                x_matrix = a                
            
        return a