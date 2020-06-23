# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 19:41:45 2020

@author: Rushad
"""

from .system import StateSpace
import numpy as np
from sympy import symbols, Matrix, eye, det, solveset, poly

class StateFeedback():
    
    '''
    State Feedback control.
    Returns State Feeback Gain matrix
    '''
    
    def __init__(self, ss):
        '''
        Parameters
        ----------
        ss : StateSpace Object
            DESCRIPTION. State Space represenation the system state feedback is applied to.
            
        Returns
        -------
        None.

        '''
        
        self._ss = ss
        q = self._ss.contr(ret=True)
        
        if np.linalg.det(q) == 0: 
            print("Input a controlable system")
            
        elif np.linalg.det(q) != 0: 
            print("Hence Full State Feedback is possible")
            
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
        
    def gain(self, roots):
        '''
        Parameters
        ----------
         roots : list
            DESCRIPTION. List of desired poles of the system

        Returns
        -------
        state_feedback_matrix : numpy array
            DESCRIPTION. numpy array of state feedback gains

        '''
        
        determinant = poly(self.charactaristic_eq, self._lambd)
        determinant_coefs = determinant.all_coeffs()
        
        char_eq_req = (self._lambd - roots[0])*(self._lambd - roots[1])*(self._lambd - roots[2])
        char_eq_req = char_eq_req.expand()
        char_eq_req = poly(char_eq_req)
        char_eq_req_coefs = char_eq_req.all_coeffs()
        
        state_feedback_gain_list = []
        for i in range(len(self._ss.A)):
            k_elem = float(list(solveset(determinant_coefs[i+1] - char_eq_req_coefs[i+1]).evalf())[0])
            state_feedback_gain_list.append(k_elem)
         
        state_feedback_gain_list = state_feedback_gain_list[::-1]
        self.state_feedback_gain_matrix = np.array(state_feedback_gain_list).reshape(1, len(self._ss.A))
        
        return self.state_feedback_gain_matrix
    
    def model(self, k_ref=1):
        '''
        Parameters
        ----------
        k_ref : float/integer, optional
            DESCRIPTION. Reference gain. Increase/Decrease this to adjust the steady state error. The default is 1.

        Returns
        -------
        model : StateSpace object
            DESCRIPTION. Returns SS Model with State Feedback

        '''
        A = self._ss.A
        B = self._ss.B
        C = self._ss.C
        D = self._ss.D
        K = self.state_feedback_gain_matrix
        
        A_new = A - np.matmul(B.reshape((len(self._ss.A),1)), K.reshape((1,len(self._ss.A))))
        B_new = B*k_ref
        model = StateSpace(A_new,B_new,C,D)
        
        return model
