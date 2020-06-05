# -*- coding: utf-8 -*-
"""
Created on Thu May 28 19:31:48 2020

@author: Rushad
"""

import numpy as np
import matplotlib.pyplot as plt

class TransferFunction():
    '''
    Define the Transfer Functions in standard form only.
    Currently supports first and second order systems
    '''
    def __init__(self, num_coef, den_coef):
        '''
        Parameters
        ----------
        num_coef : numpy array OR list
            DESCRIPTION. Coefficient of Transfer Function's Numerator
        den_coef : TYPE numpy array OR list
            DESCRIPTION. Coefficient of Transfer Function's Denominator

        Returns
        -------
        None.

        '''
        self.num_coef = np.array(num_coef)
        self.den_coef = np.array(den_coef)
        self.num_coef = self.num_coef.reshape([len(self.num_coef), 1])
        self.den_coef = self.den_coef.reshape([len(self.den_coef), 1])
        self.order = max(len(self.num_coef), len(self.den_coef)) - 1
        
        if (max(len(self.num_coef), len(self.den_coef))-1 > 2):
            print("[WARNING] You have inputed a system of Order:" + str(max(len(self.num_coef), len(self.den_coef))-1) + "\n" + "Current support is for first and second order systems\n Continuing WILL NOT produce correct results")
            
    def display(self):
        '''
        Displays TF block
        
        '''
        
        num_str = ""
        for n in range(len(self.num_coef)):
            if n < len(self.num_coef)-1: #if not last
                if n != len(self.num_coef)-2: #if not second last
                    if self.num_coef[n] != 1 and self.num_coef[n] != 0: #if coef is not zero and one
                        num_str = num_str + str(float(self.num_coef[n])) + "*S^" + str(abs(n-len(self.num_coef)+1)) + " + "
                    elif self.num_coef[n] == 1: #if coef is one
                        num_str = num_str + "S^" + str(abs(n-len(self.num_coef)+1)) + " + "
                    elif self.num_coef[n] == 0: #if coef is zero
                        pass
                else: #if second last
                    if self.num_coef[n] != 1 and self.num_coef[n] != 0: #if coef is not zero and one
                        num_str = num_str + str(float(self.num_coef[n])) + "*S" + " + "
                    elif self.num_coef[n] == 1: #if coef is one
                        num_str = num_str  + "S" + " + "
                    elif self.num_coef[n] == 0: #if coef is zero
                        pass
                        
            else: #if last
                if self.num_coef[n] != 0: #if coef is not zero
                    num_str = num_str + str(float(self.num_coef[n]))
                elif self.num_coef[n] == 0: #if coef is zero
                    num_str = num_str[:-3]
                  
        den_str = ""
        for d in range(len(self.den_coef)):
            if d < len(self.den_coef)-1: #if not last 
                if d != len(self.den_coef)-2: #if not second last
                    if self.den_coef[d] != 1 and self.den_coef[d] != 0: #if coef not zero and one
                        den_str = den_str + str(float(self.den_coef[d])) + "*S^" + str(abs(d-len(self.den_coef)+1)) + " + "
                    elif self.den_coef[d] == 1: #if coef is one
                        den_str = den_str + "S^" + str(abs(d-len(self.den_coef)+1)) + " + "
                    elif self.den_coef[d] == 0: #if coef is zero
                        pass
                else: #if second last
                    if self.den_coef[d] != 1 and self.den_coef[d] != 0: #if coef is not zero and one
                        den_str = den_str + str(float(self.den_coef[d])) + "*S" + " + "
                    elif self.den_coef[d] == 1: #if coef is one
                        den_str = den_str  + "S" + " + "
                    elif self.den_coef[d] == 0: #if coef is zero
                        pass
            else: #if last
                if self.den_coef[d] != 0: #if coef is not zero
                    den_str = den_str + str(float(self.den_coef[d]))
                elif self.den_coef[d] == 0: #if coef is zero
                    den_str = den_str[:-3]
        
        div_line_len = max(len(num_str), len(den_str))
        div_line = div_line_len*"-"
        tf_disp = str(num_str + " \n" + div_line + " \n" + den_str)
        print(tf_disp)
        
    def parameters(self, settling_time_tolerance=0.02):
        '''
        Parameters
        ----------
        settling_time_tolerance : float, optional
            DESCRIPTION. Tolerance limit for error in settling time. The default is 0.05 (5%)

        Returns
        -------
        parameter : dictionary
            DESCRIPTION. Dictionary containing all the parameters/time domain specifications

        '''
        self.order = max(len(self.num_coef), len(self.den_coef)) - 1
        self.settling_time_tolerance = settling_time_tolerance
        
        if self.order == 1:
            self.gain = float(self.num_coef[0])
            self.time_constant = float(self.den_coef[0])
            parameter = {"Order":self.order, "Gain":self.gain, "Time Constant":self.time_constant}
            return parameter
            
        if self.order == 2:
            self.gain = float(self.num_coef[0]/self.den_coef[2])
            self.natural_frequency = float(np.sqrt(self.den_coef[2]))
            self.damping_ratio = float(self.den_coef[1]/(2*self.natural_frequency))
            self.damped_freq = self.natural_frequency*np.sqrt(1 - self.damping_ratio**2)
            self.phase_angle = float(np.arctan(np.sqrt(np.abs(1 - self.damping_ratio**2))/self.damping_ratio))            
            self.rise_time = float((np.pi - self.phase_angle)/(self.natural_frequency*np.sqrt(1 - self.damping_ratio**2)))
            self.peak_time = float(np.pi/(self.natural_frequency*np.sqrt(1 - self.damping_ratio**2)))
            self.max_overshoot = float(np.exp((-self.damping_ratio*np.pi)/(np.sqrt(1 - self.damping_ratio**2)))*100)
            self.settling_time = float(-np.log(self.settling_time_tolerance*np.sqrt(1 - self.damping_ratio**2))/(self.damping_ratio*self.natural_frequency))
           
            parameter = {"Order":self.order, "Gain":self.gain,"Natural Frequency":self.natural_frequency, "Damping Frequency":self.damped_freq, "Damping Ratio":self.damping_ratio, "Phase Angle":self.phase_angle, "Rise Time":self.rise_time, "Peak Time":self.peak_time, "Max Overshoot":self.max_overshoot, "Settling Time":self.settling_time}
            return parameter     
           
    def response(self, input_type, time_period=5, sample_time=0.2, ret=False):
        '''
        Parameters
        ----------
        input_type : string
            DESCRIPTION. input signal type: impulse, step or ramp
        time_period : integer, optional
            DESCRIPTION. The time duration the signal is processed for. The default is 5.
        sample_time : float, optional
            DESCRIPTION. Sample time of the signal. The default is 0.2.
        ret : bool, optional
            DESCRIPTION. Set to True if the systems response is to be returned. The default is False.

        Returns
        -------
        resp : numpy array
            DESCRIPTION. numpy array of response of the system. Is only returned if ret is set to True

        '''
        
        controller_time = np.array([i for i in np.arange(0, time_period, sample_time)])
        input_resp = {"impulse":"impulse(self)", "step":"step(self)", "ramp":"ramp(self)"}
        
        def impulse(self):
            
            def impulse_order1(self):
                resp = (float(self.num_coef[0])/float(self.den_coef[0]))*np.exp(-controller_time/float(self.den_coef[0]))
                return resp
            
            def impulse_order2(self):
                
                natural_frequency = float(np.sqrt(self.den_coef[2]))
                damping_ratio = float(self.den_coef[1]/(2*natural_frequency))
                
                if float(damping_ratio) > 1: 
                    resp = (natural_frequency/(np.sqrt(damping_ratio**2 - 1)))*np.exp(-damping_ratio*natural_frequency*controller_time)*np.sinh(natural_frequency*np.sqrt(damping_ratio**2 - 1)*controller_time)
                elif float(damping_ratio) < 1:
                    resp = (natural_frequency/(np.sqrt(1 - damping_ratio**2)))*np.exp(-damping_ratio*natural_frequency*controller_time)*np.sin(natural_frequency*np.sqrt(1- damping_ratio**2)*controller_time)                
                elif float(damping_ratio) == 1:
                    resp = (natural_frequency**2)*controller_time*(np.exp(-natural_frequency*controller_time))
                elif float(damping_ratio) == 0:
                    resp = natural_frequency*np.sin(natural_frequency*controller_time)
                return resp
        
            if self.order == 1:
                resp = impulse_order1(self)
            elif self.order == 2:
                resp = (float(self.num_coef[0]/self.den_coef[2]))*impulse_order2(self)
                
            return resp
        
        def step(self):
            
            def step_order1(self):
                resp = float(self.num_coef[0])*(1 - np.exp(-controller_time/float(self.den_coef[0])))
                return resp
            
            def step_order2(self):
                
                natural_frequency = float(np.sqrt(self.den_coef[2]))
                damping_ratio = float(self.den_coef[1]/(2*natural_frequency))
                phase_angle = float(np.arctan(np.sqrt(1 - damping_ratio**2)/damping_ratio))
                
                
                if float(damping_ratio == 1):
                    resp = 1 - (1 + (natural_frequency*controller_time))*np.exp(-damping_ratio*natural_frequency*controller_time)
                elif float(damping_ratio < 1):
                    resp = 1 - ((np.exp(-damping_ratio*natural_frequency*controller_time)/np.sqrt(1 - damping_ratio**2))*np.sin(natural_frequency*np.sqrt(1 - damping_ratio**2)*controller_time + phase_angle))
                elif float(damping_ratio > 1):
                    resp = 1 - (np.exp(-damping_ratio*natural_frequency*controller_time)/(2*np.sqrt(damping_ratio**2 - 1)))*((np.exp(natural_frequency*np.sqrt(damping_ratio**2 - 1)*controller_time)/(damping_ratio - np.sqrt(damping_ratio**2 - 1))) + (np.exp(-natural_frequency*np.sqrt(damping_ratio**2 - 1)*controller_time)/(damping_ratio + np.sqrt(damping_ratio**2 - 1))))
                elif float(damping_ratio == 0):
                    resp = 1 - (np.e*np.sin(natural_frequency*controller_time + 1.5707963267948966))        
                
                return resp
            
            if self.order == 1:
                resp = step_order1(self)
            elif self.order == 2:
                resp = (float(self.num_coef[0]/self.den_coef[2]))*step_order2(self)
                
            return resp
        
        def ramp(self):
            
            def ramp_order1(self):
                resp = float(self.num_coef[0])*(float(-self.den_coef[0]) + controller_time + np.exp(-controller_time/float(self.den_coef[0])))
                return resp
        
            def ramp_order2(self):
                
                natural_frequency = float(np.sqrt(self.den_coef[2]))
                damping_ratio = float(self.den_coef[1]/(2*natural_frequency))
                
                if 0 <= float(damping_ratio) < 1:
                    resp = (1/natural_frequency**2)*((controller_time + (np.exp(-damping_ratio*natural_frequency*controller_time)/natural_frequency)*((2*damping_ratio*np.cos(natural_frequency*np.sqrt(1 - damping_ratio**2)*controller_time)) + (((2*damping_ratio**2 -1)/np.sqrt(1 - damping_ratio**2))*np.sin(natural_frequency*np.sqrt(1 - damping_ratio**2)*controller_time))) - (2*damping_ratio/natural_frequency)))
                elif float(damping_ratio) == 1:
                    resp = (1/natural_frequency**2)*(controller_time + ((2*np.exp(-natural_frequency*controller_time))/natural_frequency) + (controller_time*np.exp(-natural_frequency*controller_time)) - (2/natural_frequency))
                elif float(damping_ratio) > 1:
                    resp = (1/damping_ratio**2)*(controller_time + (natural_frequency/(2*np.sqrt(np.abs(1 - damping_ratio**2))))*((((1/((damping_ratio*natural_frequency) - np.sqrt(np.abs(1 - damping_ratio**2))*natural_frequency))**2)*np.exp(-controller_time/(1/((damping_ratio*natural_frequency) - np.sqrt(np.abs(1 - damping_ratio**2))*natural_frequency)))) - (((1/((damping_ratio*natural_frequency) + np.sqrt(np.abs(1 - damping_ratio**2))*natural_frequency))**2)*(np.exp(-controller_time/(1/((damping_ratio*natural_frequency) + np.sqrt(np.abs(1 - damping_ratio**2))*natural_frequency)))))) - (2*damping_ratio/natural_frequency))
                
                return resp
                
            if self.order == 1:
                resp = ramp_order1(self)
            elif self.order == 2:
                resp = float(self.num_coef[0]/self.den_coef[2])*ramp_order2(self)
                
            return resp
            
        resp = eval(input_resp[input_type])
        
        plt.plot(controller_time, resp)
        plt.show()
                          
        if ret == True:
            return resp

    
class feedback(TransferFunction):
    '''
    Add feedback TF to open loop TF. Define in standard form only.
    '''
    def __init__(self, G, H=1.0):
        '''
        Parameters
        ----------
        G : TransferFunction object
            DESCRIPTION. TF the feedback is to be implemented on
        H : integer / float, optional
            DESCRIPTION. Feedback block (gain of feedback). The default is 1 (unity feedback)

        Returns
        -------
        None.

        '''
        
        num = G.num_coef
        den = G.den_coef

        feedback_den0 =  float(den[0])
        feedback_den1 =  float(den[1])
        feedback_den2 =  float(den[2] + (num[-1]/H))
        
        feedback_num = num
        feedback_den = np.array([feedback_den0, feedback_den1, feedback_den2])
        
        self.num_coef = feedback_num.reshape([len(feedback_num), 1])
        self.den_coef = feedback_den.reshape([len(feedback_den), 1])
        
        self.feedback_tf = TransferFunction(self.num_coef, self.den_coef)
        self.order = self.feedback_tf.order