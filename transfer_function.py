# -*- coding: utf-8 -*-
"""
Created on Thu May 28 19:31:48 2020

@author: Rushad
"""

import numpy as np
import matplotlib.pyplot as plt

class TransferFunction():
    '''
    Define the Transfer Functions in standard form only for correct results
    Currently supports first and second order systems
    '''
    def __init__(self, num_coef, den_coef):
        self.num_coef = num_coef
        self.den_coef = den_coef
        self.num_coef = self.num_coef.reshape([len(self.num_coef), 1])
        self.den_coef = self.den_coef.reshape([len(self.den_coef), 1])
        if (max(len(self.num_coef), len(self.den_coef))-1 > 2):
            print("[WARNING] You have inputed a system of Order:" + str(max(len(self.num_coef), len(self.den_coef))-1) + "\n" + "Current support is for first and second order systems\n")
            print("Continuing WILL NOT produce correct results")
    def init(self):
        '''
        Returns
        -------
        tf : dictionary
            contains TF data
            
        '''
        tf = {"num":self.num_coef, "den":self.den_coef}
        return tf

    def display(self):
        '''
        Displays TF block
        
        '''
        
        self.num_str = ""
        for n in range(len(self.num_coef)):
            if n < len(self.num_coef)-1: #if not last
                if n != len(self.num_coef)-2: #if not second last
                    if self.num_coef[n] != 1 and self.num_coef[n] != 0: #if coef is not zero and one
                        self.num_str = self.num_str + str(int(self.num_coef[n])) + "*S^" + str(abs(n-len(self.num_coef)+1)) + " + "
                    elif self.num_coef[n] == 1: #if coef is one
                        self.num_str = self.num_str + "S^" + str(abs(n-len(self.num_coef)+1)) + " + "
                    elif self.num_coef[n] == 0: #if coef is zero
                        pass
                else: #if second last
                    if self.num_coef[n] != 1 and self.num_coef[n] != 0: #if coef is not zero and one
                        self.num_str = self.num_str + str(int(self.num_coef[n])) + "*S" + " + "
                    elif self.num_coef[n] == 1: #if coef is one
                        self.num_str = self.num_str  + "S" + " + "
                    elif self.num_coef[n] == 0: #if coef is zero
                        pass
                        
            else: #if last
                if self.num_coef[n] != 0: #if coef is not zero
                    self.num_str = self.num_str + str(int(self.num_coef[n]))
                elif self.num_coef[n] == 0: #if coef is zero
                    self.num_str = self.num_str[:-3]
                  
        self.den_str = ""
        for d in range(len(self.den_coef)):
            if d < len(self.den_coef)-1: #if not last 
                if d != len(self.den_coef)-2: #if not second last
                    if self.den_coef[d] != 1 and self.den_coef[d] != 0: #if coef not zero and one
                        self.den_str = self.den_str + str(int(self.den_coef[d])) + "*S^" + str(abs(d-len(self.den_coef)+1)) + " + "
                    elif self.den_coef[d] == 1: #if coef is one
                        self.den_str = self.den_str + "S^" + str(abs(d-len(self.den_coef)+1)) + " + "
                    elif self.den_coef[d] == 0: #if coef is zer0
                        pass
                else: #if second last
                    if self.den_coef[d] != 1 and self.den_coef[d] != 0: #if coef is not zero and one
                        self.den_str = self.den_str + str(int(self.den_coef[d])) + "*S" + " + "
                    elif self.den_coef[d] == 1: #if coef is one
                        self.den_str = self.den_str  + "S" + " + "
                    elif self.den_coef[d] == 0: #if coef is zero
                        pass
            else: #if last
                if self.den_coef[d] != 0: #if coef is not zero
                    self.den_str = self.den_str + str(int(self.den_coef[d]))
                elif self.den_coef[d] == 0: #if coef is zero
                    self.den_str = self.den_str[:-3]
        
        self.div_line_len = max(len(self.num_str), len(self.den_str))
        self.div_line = self.div_line_len*"-"
        tf_disp = str(self.num_str + " \n" + self.div_line + " \n" + self.den_str)
        print(tf_disp)
        
    def response(self, input_type, time_period=3, sample_time=0.2, ret=False):
        self.input_type = input_type
        self.time_period = time_period
        self.sample_time = sample_time
        self.controller_time = np.array([i for i in np.arange(0, self.time_period, self.sample_time)])
        self.input_resp = {"impulse":"impulse_order2(self)", "step":"step_order1(self)", "ramp":"ramp_order1(self)"}
        
        def impulse_order1(self):
            resp = (float(self.num_coef[0])/float(self.den_coef[0]))*np.exp(-self.controller_time/float(self.den_coef[0]))
            return resp
            
        def step_order1(self):
            resp = float(self.num_coef[0])*(1 - np.exp(-self.controller_time/float(self.den_coef[0])))
            return resp
            
        def ramp_order1(self):
            resp = float(self.num_coef[0])*(float(-self.den_coef[0]) + self.controller_time + np.exp(-self.controller_time/float(self.den_coef[0])))
            return resp
        
        def impulse_order2(self):
            self.natural_frequency = float(np.sqrt(self.den_coef[2]))
            self.damping_ratio = self.den_coef[1]/(2*self.natural_frequency)
            
            if self.damping_ratio > 1: 
                resp = (self.natural_frequency/(np.sqrt(self.damping_ratio**2 - 1)))*np.exp(-self.damping_ratio*self.natural_frequency*self.controller_time)*np.sinh(self.natural_frequency*np.sqrt(self.damping_ratio**2 - 1))*self.controller_time
            elif self.damping_ratio < 1:
                resp = (self.natural_frequency/(np.sqrt(1 - self.damping_ratio**2)))*np.exp(-self.damping_ratio*self.natural_frequency*self.controller_time)*np.sin(self.natural_frequency*np.sqrt(1- self.damping_ratio**2))*self.controller_time                
            
            return resp
            
        resp = eval(self.input_resp[self.input_type])
        
        plt.plot(self.controller_time, resp)
        plt.show()
                          
        if ret == True:
            return resp