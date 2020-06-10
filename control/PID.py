# -*- coding: utf-8 -*-
"""
Created on Fri May 29 14:28:21 2020

@author: Rushad
"""
import numpy as np
import matplotlib.pyplot as plt

class PID():
    
    def __init__(self, K_p, K_i, K_d, tf, time_period=3):
        
        self.K_p = K_p
        self.K_i = K_i
        self.K_d = K_d
        self.tf = tf
        self.time_period = time_period
        self.inputs = {"impulse" : "[1 if i == 0 else 0 for i in np.arange(0, self.time_period, 0.2)]", "step" : "[1 for i in np.arange(0, self.time_period, 0.2)]", "ramp" : " [i for i in np.arange(0, self.time_period, 0.2)]"}
        
    
    def display(self):
        '''
        Displays the PID TF block

        '''
        self.num_str = str(self.K_d) + "*S^2 + " + str(self.K_p) + "*S + " + str(self.K_i) 
        self.den_str = round(len(self.num_str)/2)*" " + "S" + " "*round(len(self.num_str)/2)
        self.div_line_len = max(len(self.num_str), len(self.den_str))
        self.div_line = self.div_line_len*"-"
        pid_tf_disp = str(self.num_str + " \n" + self.div_line + " \n" + self.den_str)
        print(pid_tf_disp)
        
    def response(self, input_type):
        
        pid_num = [self.K_d, self.K_p, self.K_i]
        pid_den = [1]
        num = self.tf.num_coef
        den = self.tf.den_coef
        tf_num = list(self.tf.num_coef.reshape(len(num),))
        tf_den = list(self.tf.den_coef.reshape(len(den),))
        
        num_size = max(len(pid_num), len(tf_num))
        den_size = max(len(pid_den), len(tf_den))
        
        num_diff = len(pid_num) - len(tf_num)
        den_diff = len(pid_den) - len(tf_den)
        
        try:
            if len(tf_num) < len(pid_num):
                temp_num = np.zeros(num_diff)
                tf_num = np.concatenate((temp_num, tf_num))
            elif len(tf_num) > len(pid_num):
                temp_num = np.zeros(abs(num_diff))
                pid_num = np.concatenate((temp_num, pid_num))
                            
            if len(tf_den) < len(pid_den):
                temp_den = np.zeros(den_diff)
                tf_den = np.concatenate((temp_den, tf_den))
            elif len(tf_den) > len(pid_den):
                temp_den = np.zeros(abs(den_diff))
                pid_den = np.concatenate((temp_den, pid_den))
            
        except ValueError:
            pass
        
        print(tf_num, pid_num)
        print(tf_den, pid_den)