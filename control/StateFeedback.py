# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 19:41:45 2020

@author: Rushad
"""

import re
import system
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
        self.lambd = symbols('lambd')
        k1, k2, k3 = symbols('k1, k2, k3')
        k_matrix = Matrix([k1, k2, k3]).transpose()
        
        A_og = Matrix(ss.A)
        B_matrix = Matrix(ss.B)
        A_new = A_og - (B_matrix*k_matrix)
        
        char_eq = eye(len(ss.A))*self.lambd - A_new
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
        
        determinant = poly(self.charactaristic_eq, self.lambd)
        determinant_coefs = determinant.all_coeffs()
        
        char_eq_req = (self.lambd - roots[0])*(self.lambd - roots[1])*(self.lambd - roots[2])
        char_eq_req = char_eq_req.expand()
        char_eq_req = poly(char_eq_req)
        char_eq_req_coefs = char_eq_req.all_coeffs()
        
        k3 = float(list(solveset(determinant_coefs[1] - char_eq_req_coefs[1]).evalf())[0])
        k2 = float(list(solveset(determinant_coefs[2] - char_eq_req_coefs[2]).evalf())[0])
        k1 = float(list(solveset(determinant_coefs[3] - char_eq_req_coefs[3]).evalf())[0])
        
        self.state_feedback_gain_matrix = np.array([k1, k2, k3])
        return self.state_feedback_gain_matrix
