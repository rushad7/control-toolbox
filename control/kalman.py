# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 19:01:57 2020

@author: Rushad
"""

import numpy as np

class KalmanFilter():
    
    def __init__(self, ss, Q = None, R = None, P = None, x0 = None):

        self._ss = ss
        self._A = self._ss.A
        self._B = self._ss.B
        self._C = self._ss.C

        if(self._A is None or self._C is None):
            raise ValueError("Set proper system dynamics.")

        self._n = self._A.shape[1]
        self._m = self._C.shape[1]

        self.Q = np.eye(self._n) if Q is None else Q
        self.R = np.eye(self._n) if R is None else R
        self.P = np.eye(self._n) if P is None else P
        self.x = np.zeros((self.n, 1)) if x0 is None else x0

    def predict(self, u = 0):
        
        self.x = self._A@self.x + self._B@u
        self.P = self._A@self.P@self._A.T + self.Q
        
        return self.x

    def update(self, z):
        
        inv = np.linalg.inv(self.R + self._C@self.P@self._C.T)
        K = self.P@self._C.T@inv
        
        y = z - self._C@self.x
        self.x = self.x + K@y
        
        I = np.eye(self._n)
        self.P = (I - K@self._C)@self.P@((I - K@self._C).T) + K@self.R@K.T

    def solve(self, measurements):
        
        m_upd = np.zeros(shape=measurements.shape)
        time = np.array(range(len(measurements)))
        predictions = []
    
        for z in m_upd:
            predictions.append(self._ss.C@self.predict())[0]
            self.update(z)
    
        import matplotlib.pyplot as plt
        plt.plot(time, m_upd, label = 'Measurements')
        plt.plot(time, np.array(predictions), label = 'Kalman Filter Prediction')
        plt.plot(time, measurements, label = 'Ideal')
        plt.legend()
        plt.show()
        return measurements