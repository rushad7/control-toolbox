# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 17:10:26 2020

@author: Rushad
"""

import numpy as np
from sympy import symbols, Matrix, exp
from .system import StateSpace

class linearize():
    
    def __init__(self, ss, x0, x_op, u_op, y_op):
        
        self._x_op = x_op
        self._y_op = y_op
        self._u_op = u_op
        
        t = symbols("t")
        
        x_str = ""
        for i in range(len(ss.A)):
            x_str = x_str + "x" + str(i+1) + ","
        x_str = x_str[:-1]
        x_var = symbols(x_str)
        self._x_matrix = Matrix([x_var])
        
        u_str = ""
        for i in range(len(ss.A)-1):
            u_str = u_str + "u" + str(i+1) + ","
        u_str = u_str[:-1]
        u_var = symbols(u_str)
        self._u_matrix = Matrix([u_var])

        state_trans_matrix = exp(Matrix(ss.A)*t)
        self._x0 = np.reshape(x0, (1,np.product(x0.shape)))
        self._xt = Matrix(state_trans_matrix.dot(Matrix(x0)))
        
        self._yt = Matrix(ss.C)*(self._x_matrix).T + Matrix(ss.D)*(self._u_matrix) 
        
        self._ft = Matrix(ss.A)*(self._x_matrix).T + Matrix(ss.B)*(self._u_matrix)
        self._gt = Matrix(ss.C)*(self._x_matrix).T + Matrix(ss.D)*(self._u_matrix)
        
    def lin(self):
        
        del_xt = self._xt - self._x_op
        del_yt = self._yt - self._y_op
        del_ut = self._u_matrix - self._u_op
        
        A_lin = self._ft.jacobian(self._x_matrix)
        B_lin = self._ft.jacobian(self._u_matrix)
        C_lin = self._gt.jacobian(self._x_matrix)
        D_lin = self._gt.jacobian(self._u_matrix)
        
        linearized_model = StateSpace(A_lin, B_lin, C_lin, D_lin)
        
        return linearized_model
        
        
        