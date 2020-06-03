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
        if (max(len(self.num_coef), len(self.den_coef))-1 > 2):
            print("[WARNING] You have inputed a system of Order:" + str(max(len(self.num_coef), len(self.den_coef))-1) + "\n" + "Current support is for first and second order systems\n Continuing WILL NOT produce correct results")
            
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
        
    def time_domain_spec(self, settling_time_tolerance=0.05):
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
            self.phase_angle = float(np.arctan(self.damping_ratio/np.sqrt(np.abs(1 - self.damping_ratio**2))))            
            self.rise_time = float((np.pi - self.phase_angle)/(self.natural_frequency*np.sqrt(1 - self.damping_ratio**2)))
            self.peak_time = float(np.pi/(self.natural_frequency*np.sqrt(1 - self.damping_ratio**2)))
            self.max_overshoot = float(np.exp((-self.damping_ratio*np.pi)/(np.sqrt(1 - self.damping_ratio**2)))*100)
            self.settling_time = float(-np.log((self.settling_time_tolerance*np.sqrt(1 - self.damping_ratio**2))/(self.damping_ratio*self.natural_frequency)))
           
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
        self.input_type = input_type
        self.time_period = time_period
        self.sample_time = sample_time
        self.controller_time = np.array([i for i in np.arange(0, self.time_period, self.sample_time)])
        self.input_resp = {"impulse":"impulse(self)", "step":"step(self)", "ramp":"ramp(self)"}
        self.order = max(len(self.num_coef), len(self.den_coef)) - 1
        
        def impulse(self):
            
            def impulse_order1(self):
                resp = (float(self.num_coef[0])/float(self.den_coef[0]))*np.exp(-self.controller_time/float(self.den_coef[0]))
                return resp
            
            def impulse_order2(self):
                
                self.natural_frequency = float(np.sqrt(self.den_coef[2]))
                self.damping_ratio = float(self.den_coef[1]/(2*self.natural_frequency))
                
                if float(self.damping_ratio) > 1: 
                    resp = (self.natural_frequency/(np.sqrt(self.damping_ratio**2 - 1)))*np.exp(-self.damping_ratio*self.natural_frequency*self.controller_time)*np.sinh(self.natural_frequency*np.sqrt(self.damping_ratio**2 - 1)*self.controller_time)
                elif float(self.damping_ratio) < 1:
                    resp = (self.natural_frequency/(np.sqrt(1 - self.damping_ratio**2)))*np.exp(-self.damping_ratio*self.natural_frequency*self.controller_time)*np.sin(self.natural_frequency*np.sqrt(1- self.damping_ratio**2)*self.controller_time)                
                elif float(self.damping_ratio) == 1:
                    resp = (self.natural_frequency**2)*self.controller_time*(np.exp(-self.natural_frequency*self.controller_time))
                elif float(self.damping_ratio) == 0:
                    resp = self.natural_frequency*np.sin(self.natural_frequency*self.controller_time)
                return resp
        
            if self.order == 1:
                resp = impulse_order1(self)
            elif self.order == 2:
                resp = (float(self.num_coef[0]/self.den_coef[2]))*impulse_order2(self)
                
            return resp
        
        def step(self):
            
            def step_order1(self):
                resp = float(self.num_coef[0])*(1 - np.exp(-self.controller_time/float(self.den_coef[0])))
                return resp
            
            def step_order2(self):
                
                self.natural_frequency = float(np.sqrt(self.den_coef[2]))
                self.damping_ratio = float(self.den_coef[1]/(2*self.natural_frequency))
                self.phase_angle = float(np.arctan(np.sqrt(1 - self.damping_ratio**2)/self.damping_ratio))
                
                
                if float(self.damping_ratio == 1):
                    resp = 1 - (1 + (self.natural_frequency*self.controller_time))*np.exp(-self.damping_ratio*self.natural_frequency*self.controller_time)
                elif float(self.damping_ratio < 1):
                    resp = 1 - ((np.exp(-self.damping_ratio*self.natural_frequency*self.controller_time)/np.sqrt(1 - self.damping_ratio**2))*np.sin(self.natural_frequency*np.sqrt(1 - self.damping_ratio**2)*self.controller_time + self.phase_angle))
                elif float(self.damping_ratio > 1):
                    resp = 1 - (np.exp(-self.damping_ratio*self.natural_frequency*self.controller_time)/(2*np.sqrt(self.damping_ratio**2 - 1)))*((np.exp(self.natural_frequency*np.sqrt(self.damping_ratio**2 - 1)*self.controller_time)/(self.damping_ratio - np.sqrt(self.damping_ratio**2 - 1))) + (np.exp(-self.natural_frequency*np.sqrt(self.damping_ratio**2 - 1)*self.controller_time)/(self.damping_ratio + np.sqrt(self.damping_ratio**2 - 1))))
                elif float(self.damping_ratio == 0):
                    resp = 1 - (np.e*np.sin(self.natural_frequency*self.controller_time + 1.5707963267948966))        
                return resp
            
            if self.order == 1:
                resp = step_order1(self)
            elif self.order == 2:
                resp = (float(self.num_coef[0]/self.den_coef[2]))*step_order2(self)
                
            return resp
        
        def ramp(self):
            
            def ramp_order1(self):
                resp = float(self.num_coef[0])*(float(-self.den_coef[0]) + self.controller_time + np.exp(-self.controller_time/float(self.den_coef[0])))
                return resp
        
            def ramp_order2(self):
                
                self.natural_frequency = float(np.sqrt(self.den_coef[2]))
                self.damping_ratio = float(self.den_coef[1]/(2*self.natural_frequency))
                
                if 0 <= float(self.damping_ratio) < 1:
                    resp = (1/self.natural_frequency**2)*((self.controller_time + (np.exp(-self.damping_ratio*self.natural_frequency*self.controller_time)/self.natural_frequency)*((2*self.damping_ratio*np.cos(self.natural_frequency*np.sqrt(1 - self.damping_ratio**2)*self.controller_time)) + (((2*self.damping_ratio**2 -1)/np.sqrt(1 - self.damping_ratio**2))*np.sin(self.natural_frequency*np.sqrt(1 - self.damping_ratio**2)*self.controller_time))) - (2*self.damping_ratio/self.natural_frequency)))
                elif float(self.damping_ratio) == 1:
                    resp = (1/self.natural_frequency**2)*(self.controller_time + ((2*np.exp(-self.natural_frequency*self.controller_time))/self.natural_frequency) + (self.controller_time*np.exp(-self.natural_frequency*self.controller_time)) - (2/self.natural_frequency))
                elif float(self.damping_ratio) > 1:
                    resp = (1/self.damping_ratio**2)*(self.controller_time + (self.natural_frequency/(2*np.sqrt(np.abs(1 - self.damping_ratio**2))))*((((1/((self.damping_ratio*self.natural_frequency) - np.sqrt(np.abs(1 - self.damping_ratio**2))*self.natural_frequency))**2)*np.exp(-self.controller_time/(1/((self.damping_ratio*self.natural_frequency) - np.sqrt(np.abs(1 - self.damping_ratio**2))*self.natural_frequency)))) - (((1/((self.damping_ratio*self.natural_frequency) + np.sqrt(np.abs(1 - self.damping_ratio**2))*self.natural_frequency))**2)*(np.exp(-self.controller_time/(1/((self.damping_ratio*self.natural_frequency) + np.sqrt(np.abs(1 - self.damping_ratio**2))*self.natural_frequency)))))) - (2*self.damping_ratio/self.natural_frequency))
                return resp
                
            if self.order == 1:
                resp = ramp_order1(self)
            elif self.order == 2:
                resp = float(self.num_coef[0]/self.den_coef[2])*ramp_order2(self)
                
            return resp
            
        resp = eval(self.input_resp[self.input_type])
        
        plt.plot(self.controller_time, resp)
        plt.show()
                          
        if ret == True:
            return resp

    def error(self, input_type, system_type):
        self.input_type = input_type
        self.system_type = system_type
        self.system_types = {"0":"type0(self)", "1":"type1(self)", "2":"type2(self)"}
        #self.input_resp = {"step":"step(self)", "ramp":"ramp(self)", "parabolic":"parabolic(self)"}
        
        def type0(self):
            def step(self):    
                self.position_error = self.num_coef[0]/self.den_coef[-1]
                self.error0 = 1/(1+self.position_error)
                return self.error0
            def ramp(self):
                self.error0 = np.inf
                return self.error0
            def parabolic(self):
                self.error0 = np.inf
                return self.error0
            
            self.error_step = self.step()
            self.error_ramp = self.ramp()
            self.error_parabolic = self.parabolic()
            self.error_total = {"Type":self.system_type, "Position Error":self.error_step, "Velocity Error":self.error_ramp, "Acceleration Error":self.error_parabolic}
            
            return self.error_total
            
        def type1(self):
            def step(self):    
                self.error1 = 0
                return self.error1
            def ramp(self):
                #self.velocity_error = 
                self.error1 = np.inf
                return self.error
            def parabolic(self):
                self.error1 = np.inf
                return self.error1
            
            self.error_step = self.step()
            self.error_ramp = self.ramp()
            self.error_parabolic = self.parabolic()
            self.error_total = {"Type":self.system_type, "Position Error":self.error_step, "Velocity Error":self.error_ramp, "Acceleration Error":self.error_parabolic}
            
            return self.error_total
            
        def type2(self):
            def step(self):    
                self.error2 = 0
                return self.error2
            def ramp(self):
                self.error2 = np.inf
                return self.error2
            def parabolic(self):
                #self.velocity_error =
                self.error2 = np.inf
                return self.error2
            
            self.error_step = step(self)
            self.error_ramp = ramp(self)
            self.error_parabolic = parabolic(self)
            self.error_total = {"Type":self.system_type, "Position Error":self.error_step, "Velocity Error":self.error_ramp, "Acceleration Error":self.error_parabolic}
            
            return self.error_total
        
        eval(self.system_types[self.system_type])