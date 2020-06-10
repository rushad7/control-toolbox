# -*- coding: utf-8 -*-
"""
Created on Fri May 29 14:28:21 2020

@author: Rushad
"""

import control.system as system
import numpy as np

class PID():
    
    def __init__(self, K_p, K_i, K_d, tf, time_period=3):
        
        self.K_p = K_p
        self.K_i = K_i
        self.K_d = K_d
        self.time_period = time_period
        
        pid_num = [self.K_d, self.K_p, self.K_i]
        pid_den = [1, 0]
        
        num = tf.num_coef
        den = tf.den_coef
        
        tf_num = list(tf.num_coef.reshape(len(num),))
        tf_den = list(tf.den_coef.reshape(len(den),))
                
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
        
        reduced_tf_num = np.polymul(np.array(tf_num), np.array(pid_num))
        reduced_tf_den = np.polymul(np.array(tf_den), np.array(pid_den))
        self.reduced_tf = system.TransferFunction(reduced_tf_num, reduced_tf_den)
    
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
        
    def response(self, input_type, time_period=10, sample_time=0.05, ret=False):
        '''
        Parameters
        ----------
        input_type : string
            DESCRIPTION. input signal type: impulse, step or ramp
        time_period : integer, optional
            DESCRIPTION. The time duration the signal is processed for. The default is 10.
        sample_time : float, optional
            DESCRIPTION. Sample time of the signal. The default is 0.05.
        ret : bool, optional
            DESCRIPTION. Set to True if the systems response is to be returned. The default is False.

        Returns
        -------
        resp : numpy array
            DESCRIPTION. numpy array of response of the system. Is only returned if ret is set to True

        '''
        try:
            resp = self.reduced_tf.response(input_type, time_period, sample_time, ret)
            if ret == True:
                return resp
            
        except ValueError:
            print("Improper transfer function. `num` is longer than `den`.")