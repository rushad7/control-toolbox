# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 19:01:57 2020

@author: Rushad
"""

import numpy as np
import matplotlib.pyplot as plt

class KalmanFilter():
    
    def __init__(self, ss, Q, R, P=None, x0=None):

        self._ss = ss
        self._A = self._ss.A
        self._B = self._ss.B
        self._C = self._ss.C

        self._n = self._A.shape[1]
        self._m = self._C.shape[1]

        self.Q = Q
        self.R = R
        self.P = np.eye(self._n) if P is None else P
        self.x = np.zeros((self._n, 1)) if x0 is None else x0

    def predict(self, u = 0):
        
        self.x = np.dot(self._A, self.x) + np.dot(self._B, u)
        self.P = np.dot(np.dot(self._A, self.P), self._A.T) + self.Q
        
        return self.x

    def update(self, z):
        
        inv = np.linalg.inv(self.R + np.dot(self._C, np.dot(self.P, self._C.T)))
        K = np.dot(np.dot(self.P, self._C.T), inv)
        
        y = z - np.dot(self._C, self.x)
        self.x = self.x + np.dot(K, y)
        
        I = np.eye(self._n)
        self.P = np.dot(np.dot(I - np.dot(K, self._C), self.P), (I - np.dot(K, self._C)).T) + np.dot(np.dot(K, self.R), K.T)
        
        y = np.dot(self._C,self.x)
        return y

    def solve(self, measurements):
        
        time = np.array(range(len(measurements)))
        state_predictions = []
        output_predictions = []
        
        for z in measurements:
            state_predictions.append(np.dot(self._C,  self.predict())[0])
            output_predictions.append(self.update(z)[0][0])
        
        plt.plot(time, np.array(output_predictions), label = 'Kalman Filter Prediction')
        plt.plot(time, measurements, label = 'Measurements')
        plt.legend()
        plt.show()
        
        return output_predictions