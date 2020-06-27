# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 18:37:14 2020

@author: Rushad
"""

import numpy as np
from .system import StateSpace

class LQR():
    
    def __init__(self, ss, Q, R, N):
        '''
        Parameters
        ----------
        ss : StateSpce object
            DESCRIPTION. StateSpace object on which LQR is to be done.
        Q : numpy array
            DESCRIPTION. Q matrix of cost function
        R : numpy 
            DESCRIPTION. R matrix of cost function
        N : integer
            DESCRIPTION. Time horizon.

        Returns
        -------
        None.

        '''
        self._ss = ss
        self._Q = Q
        self._R = R
        self._N = N

    def solve(self):
        '''
        Returns
        -------
        k : numpy array
            DESCRIPTION. numpy array of Feedback gain matix
            
        '''
        A = self._ss.A
        B = self._ss.B
        
        P_current = self._Q
        N_range = list(range(1, self._N))[::-1]
        
        P = {self._N:self._Q}
        K = {}
        
        for t in N_range:
            P_prev = self._Q + A.T@P_current@A - A.T@P_current@B@np.linalg.inv(self._R + B.T@P_current@B)@B.T@P_current@A
            P[t] = P_prev
            P_current = P_prev[:]
            
        for t in range(self._N):
            Kt = -np.linalg.inv(self._R + B.T@P[t+1]@B)@B.T@P[t+1]@A
            K[t] = Kt
        
        k = K[self._N-1]
            
        return k   
    
    def model(self):
        '''
        Returns
        -------
        ss_model : TYPE
            DESCRIPTION. StateSpace object of system with StateFeedback

        '''
        k = self.solve()
       
        A_new = self._ss.A - self._ss.B@k
        ss_model = StateSpace(A_new, self._ss.B, self._ss.C, self._ss.D)
        
        return ss_model
