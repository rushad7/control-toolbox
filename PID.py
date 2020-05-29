# -*- coding: utf-8 -*-
"""
Created on Fri May 29 14:28:21 2020

@author: Rushad
"""
import numpy as np

def def_pid(K_p, K_i, K_d, transfer_function, input_type, time_period=3):
    
    pid_controller = {"kp":K_p, "ki":K_i, "kd":K_d}
    #inputs = {"impulse" : "[1 if i == 0 else 0 for i in range(5)]", "step" : "[1 for i in range(4)]", "ramp" : " [i for i in range(4)]"}
    inputs = {"impulse" : "[1 if i == 0 else 0 for i in np.arange(0, time_period, 0.2)]", "step" : "[1 for i in np.arange(0, time_period, 0.2)]", "ramp" : " [i for i in np.arange(0, time_period, 0.2)]"} 
    time = eval(inputs[input_type])
    
    