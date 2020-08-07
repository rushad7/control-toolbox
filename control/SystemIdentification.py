# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 16:01:30 2020

@author: Rushad
"""

import warnings
import numpy as np
import pandas as pd
from tensorflow.keras import initializers
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential

warnings.filterwarnings("ignore")

class SystemIdentification():
    '''
    System Identification module
    '''
    def __init__(self, path_x, path_x_dot, path_y):
        '''
        Parameters
        ----------
        path_x : file path
            DESCRIPTION. path to CSV file consisting the X matrix data. 
        path_x_dot : file path
            DESCRIPTION. path to CSV file consisting X_dot matrix data.
        path_y : file path
            DESCRIPTION. path to CSV file consisting Y matrix data.

        Returns
        -------
        None.

        '''
        data_x = pd.read_csv(path_x)
        data_x_dot = pd.read_csv(path_x_dot)
        data_y = pd.read_csv(path_y)
        
        self._x = data_x.to_numpy()
        self._x_dot = data_x_dot.to_numpy()
        self._y = data_y.to_numpy()
        
    def fit(self, num_epochs=500):
        '''
        Parameters
        ----------
        num_epochs : int, optional
            DESCRIPTION. Number of epochs. The default is 500.

        Returns
        -------
        None.

        '''
        self._stateModel = Sequential()
        self._stateModel.add(Dense(self._x.shape[0], input_dim=2, activation='sigmoid', kernel_initializer=initializers.glorot_normal()))
        self._stateModel.add(Dense(self._x.shape[0]/2, activation='sigmoid'))
        self._stateModel.add(Dense(2, activation='relu'))
        self._stateModel.compile(loss='mse', optimizer='adam', metrics=['accuracy'])
        self._stateModel.fit(self._x, self._x_dot, epochs=num_epochs, batch_size=10)
        
        self._outputModel = Sequential()
        self._outputModel.add(Dense(self._x.shape[0], input_dim=2, activation='sigmoid', kernel_initializer=initializers.glorot_normal()))
        self._outputModel.add(Dense(self._x.shape[0]/2, activation='sigmoid'))
        self._outputModel.add(Dense(1, activation='relu'))
        self._outputModel.compile(loss='mse', optimizer='adam', metrics=['accuracy'])
        self._outputModel.fit(self._x, self._y, epochs=num_epochs, batch_size=10)
        
    def model(self):
        '''
        Returns
        -------
        model_dict : dict
            DESCRIPTION. dictionary of matrices A and C.

        '''
        hyp_state = self._stateModel.predict(self._x)
        hyp_output = self._stateModel.predict(self._x)
        
        A = np.linalg.pinv(self._x)@hyp_state
        C = hyp_output.T@np.linalg.pinv(self._x).T
        
        model_dict = {"A":A, "C":C}
        
        return model_dict