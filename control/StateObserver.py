# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 16:36:40 2020

@author: Rushad
"""

from .system import StateSpace
import numpy as np
from sympy import symbols, Matrix, eye, det, solveset, poly

class StateObserver():
    
    '''
    State Observer.
    Returns State Observer Gain matrix
    '''
    
    def __init__(self, ss):
        '''
        Parameters
        ----------
        ss : StateSpace Object
            DESCRIPTION. State Space represenation the system.
            
        Returns
        -------
        None.

        '''
        
        self._ss = ss
        q = self._ss.obs(ret=True)
        
        if np.linalg.det(q) == 0: 
            print("Input a observable system")
            
        elif np.linalg.det(q) != 0: 
            print("Hence Full State observable is possible")
            
        self._lambd = symbols('lambd')
        
        k_str = ""
        for i in range(len(self._ss.A)):
            k_str = k_str + "k" + str(i+1) + ","
            
        k_str = k_str[:-1]
        k_var = symbols(k_str)
        k_matrix = Matrix(k_var).transpose()
        
        A_og = Matrix(ss.A)
        B_matrix = Matrix(ss.B)
        A_new = A_og - (B_matrix*k_matrix)
        
        char_eq = eye(len(ss.A))*self._lambd - A_new
        determinant = det(char_eq)
        self.charactaristic_eq = determinant
        
    def solve(self, roots):
        '''
        Parameters
        ----------
         roots : list
            DESCRIPTION. List of desired poles of the system

        Returns
        -------
        state_observer_matrix : numpy array
            DESCRIPTION. numpy array of state observer gains

        '''
        
        determinant = poly(self.charactaristic_eq, self._lambd)
        determinant_coefs = determinant.all_coeffs()
        
        char_eq_req = (self._lambd - roots[0])*(self._lambd - roots[1])*(self._lambd - roots[2])
        char_eq_req = char_eq_req.expand()
        char_eq_req = poly(char_eq_req)
        char_eq_req_coefs = char_eq_req.all_coeffs()
        
        state_observer_gain_list = []
        for i in range(len(self._ss.A)):
            k_elem = float(list(solveset(determinant_coefs[i+1] - char_eq_req_coefs[i+1]).evalf())[0])
            state_observer_gain_list.append(k_elem)
         
        state_observer_gain_list = state_observer_gain_list[::-1]
        self.state_observer_gain_matrix = np.array(state_observer_gain_list).reshape(1, len(self._ss.A))
        
        return self.state_observer_gain_matrix
    
    def model(self, k_ref=1):
        '''
        Parameters
        ----------
        k_ref : float/integer, optional
            DESCRIPTION. Reference gain. Increase/Decrease this to adjust the steady state error. The default is 1.

        Returns
        -------
        model : StateSpace object
            DESCRIPTION. Returns SS Model with State Observer added

        '''
        A = self._ss.A
        B = self._ss.B
        C = self._ss.C
        D = self._ss.D
        K = self.state_observer_gain_matrix
        
        A_new = A - np.matmul(B.reshape((len(self._ss.A),1)), K.reshape((1,len(self._ss.A))))
        B_new = B*k_ref
        model = StateSpace(A_new,B_new,C,D)
        
        return model
