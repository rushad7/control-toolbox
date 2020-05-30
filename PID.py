# -*- coding: utf-8 -*-
"""
Created on Fri May 29 14:28:21 2020

@author: Rushad
"""
import numpy as np
import matplotlib.pyplot as plt

class PID():
    
    def __init__(self, K_p, K_i, K_d, transfer_function, input_type, time_period=3):
        
        self.K_p = K_p
        self.K_i = K_i
        self.K_d = K_d
        self.transfer_function = transfer_function
        self.input_type = input_type
        self.time_period = time_period
        self.inputs = {"impulse" : "[1 if i == 0 else 0 for i in np.arange(0, self.time_period, 0.2)]", "step" : "[1 for i in np.arange(0, self.time_period, 0.2)]", "ramp" : " [i for i in np.arange(0, self.time_period, 0.2)]"}
        
    def init(self):        
        pid_controller = {"kp":self.K_p, "ki":self.K_i, "kd":self.K_d}
        return pid_controller
    
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
        
    def response(self):
        norm_response = []
        pid_response = []
        self.controller_input = eval(self.inputs[self.input_type])
        for s in self.controller_input:
            try:
                pid_response_elem = (float(self.K_d) + s**2 + float(self.K_p) + s + float(self.K_i))/s
            except ZeroDivisionError:
                pass
            
            power_num = len(self.transfer_function["num"]) - 1
            temp_vect_num = np.zeros(shape=(len(self.transfer_function["num"])))
            
            for temp in range(len(temp_vect_num)):
                temp_vect_num[temp] = (s**(power_num-temp))*self.transfer_function["num"][temp]
            tf_num = np.sum(temp_vect_num)

            power_den = len(self.transfer_function["den"]) - 1            
            temp_vect_den = np.zeros(shape=(len(self.transfer_function["den"])))
            
            for temp in range(len(temp_vect_den)):
                temp_vect_den[temp] = (s**(power_den-temp))*self.transfer_function["den"][temp]
            tf_den = np.sum(temp_vect_den)
            
            try:
                tf_total = tf_num/tf_den
            except ZeroDivisionError:
                pass
            
            total_response = pid_response_elem + tf_total
            norm_response.append(tf_total)
            pid_response.append(total_response)
        
        plt.plot(self.controller_input, norm_response)
        plt.plot(self.controller_input, pid_response)
        return pid_response, norm_response
                
                
                
                
                
                
                
                
                
                
                