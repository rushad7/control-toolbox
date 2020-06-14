# -*- coding: utf-8 -*-
"""
Created on Thu May 28 19:31:48 2020

@author: Rushad
"""

import warnings
import numpy as np
from scipy import signal, polyval
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")

class TransferFunction():
    '''
    Define the Transfer Functions in standard form only.
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
            
        elif self.order == 2:
            self.gain = float(self.num_coef[0]/self.den_coef[2])
            self.natural_frequency = float(np.sqrt(self.den_coef[2]))
            self.damping_ratio = float(self.den_coef[1]/(2*self.natural_frequency))
            self.damped_freq = self.natural_frequency*np.sqrt(abs(1 - self.damping_ratio**2))
            self.phase_angle = float(np.arctan(np.sqrt(np.abs(1 - self.damping_ratio**2))/self.damping_ratio))            
            self.rise_time = float((np.pi - self.phase_angle)/(self.natural_frequency*np.sqrt(abs(1 - self.damping_ratio**2))))
            self.peak_time = float(np.pi/(self.natural_frequency*np.sqrt((abs(1 - self.damping_ratio**2)))))
            self.max_overshoot = float(np.exp((-self.damping_ratio*np.pi)/(np.sqrt(abs( 1 - self.damping_ratio**2)))*100))
            self.settling_time = float(-np.log(self.settling_time_tolerance*np.sqrt(abs(1 - self.damping_ratio**2)))/(self.damping_ratio*self.natural_frequency))
           
            parameter = {"Order":self.order, "Gain":self.gain,"Natural Frequency":self.natural_frequency, "Damping Frequency":self.damped_freq, "Damping Ratio":self.damping_ratio, "Phase Angle":self.phase_angle, "Rise Time":self.rise_time, "Peak Time":self.peak_time, "Max Overshoot":self.max_overshoot, "Settling Time":self.settling_time}
            return parameter
        
        elif self.order > 2:
            print("[WARNING] You have inputed a system of Order:" + str(max(len(self.num_coef), len(self.den_coef))-1) + ". Currently supports first and second order systems")
           
    def response(self, input_type, time_period=10, sample_time=0.05, ret=False, show=True):
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
        show : bool, optional
            DESCRIPTION. Set to True if the systems response is to be displayed. The default is True.
        Returns
        -------
        resp : numpy array
            DESCRIPTION. numpy array of response of the system. Is only returned if ret is set to True

        '''
        
        controller_time = np.array([i for i in np.arange(0, time_period, sample_time)])
        input_resp = {"impulse":"impulse(self)", "step":"step(self)", "ramp":"ramp(self)"}
        
        def impulse(self):
            
            sys = signal.lti(self.num_coef.reshape(len(self.num_coef)), self.den_coef.reshape(len(self.den_coef)))
            _,resp = signal.impulse(sys, T=controller_time)
            return resp
        
        def step(self):
            
            sys = signal.lti(self.num_coef.reshape(len(self.num_coef)), self.den_coef.reshape(len(self.den_coef)))
            _,resp = signal.step(sys, T=controller_time)
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
                return resp
            elif self.order == 2:
                resp = float(self.num_coef[0]/self.den_coef[2])*ramp_order2(self) 
                return resp
            elif self.order > 2:
                print("[WARNING] You have inputed a system of Order:" + str(max(len(self.num_coef), len(self.den_coef))-1) + ". Ramp response currently supports first and second order systems")
            
        resp = eval(input_resp[input_type])
        
        if show == True:
            plt.plot(controller_time, resp)
            plt.show()
            
        if ret == True:
            return resp
            
    def pzplot(self, ret=True):
        '''
        Plots Pole-Zero plot of the system
        '''
        
        if len(self.num_coef) >= 1: 
            self.zeros = np.roots(self.num_coef.reshape(len(self.num_coef)))
            plt.plot(self.zeros.real, self.zeros.imag, "o", label="Zeros")
        if len(self.den_coef) >= 1:
            self.poles = np.roots(self.den_coef.reshape(len(self.den_coef)))
            plt.plot(self.poles.real, self.poles.imag, "x", label="Poles")
        
        plt.xlabel('Re')
        plt.ylabel('Im')
        plt.grid(True, which="both")
        plt.legend()
        plt.show()
        
        if ret == True:
            return self.poles, self.zeros

    def stability(self):
        '''
        Returns
        -------
        state : String
            Prints stability of the system
        '''
        
        if len(self.den_coef >= 1):
            poles = np.roots(self.den_coef.reshape(len(self.den_coef)))     
            poles_round = np.array(poles.imag, dtype="int")
            
            if (poles.real < 0).all():
                state = "System is Stable"
                            
            elif np.count_nonzero(poles_round) != len(poles_round) and (poles.real <= 0).all():
                if np.sum(poles) == np.sum(np.unique(poles)):
                    state = "System is Marginally Stable"
                else:
                    state = "System in Unstable"
            else:
                state = "System is Unstable"
                    
        return state

class feedback(TransferFunction):
    '''
    Add feedback TF to open loop TF. Define in standard form only.
    '''
    def __init__(self, G, H=1.0, feedback_type="negative"):
        '''
        Parameters
        ----------
        G : TransferFunction object
            DESCRIPTION. TF the feedback is to be implemented on
        H : TransferFunction object / integer / float, optional
            DESCRIPTION. Feedback block. The default is 1 (unity feedback)
        feedback_type : Negative or Positive feedback, optional
            DESCRIPTION. The default is "negative".

        Returns
        -------
        None.

        '''
        if type(H) == TransferFunction:
            
            G_num = G.num_coef
            G_num = G.num_coef.reshape(len(G_num))
            
            G_den = G.den_coef
            G_den = G.den_coef.reshape(len(G_den))
            
            H_num = H.num_coef
            H_num = H.num_coef.reshape(len(H_num))
            
            H_den = H.den_coef
            H_den = H.den_coef.reshape(len(H_den))
            
            if feedback_type == "negative":
                feedback_num = np.polymul(G_num, H_den)
                feedback_den = np.polyadd(np.polymul(G_den, H_den), np.polymul(G_den, H_num))              
            
            elif feedback_type == "positive": 
                feedback_num = np.polymul(G_num, H_den)
                feedback_den = np.polysub(np.polymul(G_den, H_den), np.polymul(G_den, H_num))
                
        
        elif type(H) == float or type(H) == int:
            num = G.num_coef
            den = G.den_coef
            
            if feedback_type == "negative":
                feedback_den0 =  float(den[0])
                feedback_den1 =  float(den[1])
                feedback_den2 =  float(den[2] + (num[-1]/H))
                
            elif feedback_type == "positive":
                feedback_den0 =  float(den[0])
                feedback_den1 =  float(den[1])
                feedback_den2 =  float(den[2] - (num[-1]/H))
            
            feedback_num = num
            feedback_den = np.array([feedback_den0, feedback_den1, feedback_den2])
            
            feedback_num = feedback_num.reshape([len(feedback_num), 1])
            feedback_den = feedback_den.reshape([len(feedback_den), 1])
            
            
        self.num_coef = feedback_num
        self.den_coef = feedback_den
                
        self.feedback_tf = TransferFunction(self.num_coef, self.den_coef)
        self.order = self.feedback_tf.order
        
class PID():
    '''
    PID control on a TF
    '''
    
    def __init__(self, K_p, K_i, K_d, tf):
        '''
        Parameters
        ----------
        K_p : float
            DESCRIPTION. Proportional Gain
        K_i : float
            DESCRIPTION. Integral Gain
        K_d : float
            DESCRIPTION. Derivative Gain
        tf : TranferFunction object
            DESCRIPTION. TF on which PID is to be implemeted

        Returns
        -------
        None.

        '''
        self.K_p = K_p
        self.K_i = K_i
        self.K_d = K_d
        self.tf = tf
        
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
        self.reduced_tf = TransferFunction(reduced_tf_num, reduced_tf_den)
    
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
        
    def response(self, input_type, time_period=10, sample_time=0.05, ret=False, show=True):
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
        show : bool, optional
            DESCRIPTION. Set to True if the systems response is to be displayed. The default is True.
        Returns
        -------
        resp : numpy array
            DESCRIPTION. numpy array of response of the system. Is only returned if ret is set to True

        '''
        try:
            resp = self.reduced_tf.response(input_type, time_period, sample_time, ret, show)
            if ret == True:
                return resp
            
        except ValueError:
            print("Improper transfer function. `num` is longer than `den`.")
            
    def tune(self, input_type="step", set_point=1, num_itr=70, rate=0.00000000001):
        '''
        Parameters
        ----------
        input_type : input signal type, optional
            DESCRIPTION. The default is "step" input.
        set_point : Optimal steady state value, optional
            DESCRIPTION. The default is 1.
        num_itr : number of iterations, optional
            DESCRIPTION. The default is 70. Might have to adjust this to prevent the cost from increasing after decreasing.
        rate : learning rate, optional
            DESCRIPTION. The default is 0.00000000001. Suggested not to increase it.

        Returns
        -------
        k : numpy array
            DESCRIPTION. numpy array of Kp, Ki, Kd values

        '''
        k = np.random.random(3).reshape(3,1)
        
        def red_tf():
            pid_num = [k[2][0], k[0][0], k[1][0]]
            pid_den = [1, 0]
            
            num = self.tf.num_coef
            den = self.tf.den_coef
            
            tf_num = list(self.tf.num_coef.reshape(len(num),))
            tf_den = list(self.tf.den_coef.reshape(len(den),))
                    
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
            reduced_tf = TransferFunction(reduced_tf_num, reduced_tf_den)
            resp = reduced_tf.response(input_type, ret=True, show=False)
            return resp
        
        costs = []
        
        y_hat = red_tf()
        m = len(y_hat)
        
        for n in range(num_itr):
            for s in range(1,m):
                
                y_hat = red_tf()
                y = np.zeros(m) + set_point
            
                loss = (1/2)*((y_hat - y)**2)
                cost = float((1/m)*np.sum(loss))
                
                
                grad_kp = (y_hat + y)/(s*(polyval(self.tf.num_coef, s)/polyval(self.tf.den_coef, s)))
                grad_ki = (y_hat + y)/(polyval(self.tf.num_coef, s)/polyval(self.tf.den_coef, s))
                grad_kd = (y_hat + y)/((s**2)*(polyval(self.tf.num_coef, s)/polyval(self.tf.den_coef, s)))
                
                grads = np.array([grad_kp, grad_ki, grad_kd])
                
                for i in range(m):
                    k = k - rate*grads
                    
            if n%10 == 0:
                print(f"cost {n}: {np.squeeze(cost)}")
            if n%20 == 0:
                costs.append(cost)
                
        plt.plot(costs)
        plt.show()
        print(s)
        return k
    
class reduce():
    '''
    Block Reduction
    '''
    def series(*tfs):
        '''
        Parameters
        ----------
        *tfs : TransferFunction objects
            DESCRIPTION. TF objects which need to be reduced

        Returns
        -------
        tfs : TransferFunction object
            DESCRIPTION. Reduced TransferFunction object

        '''
        tf_len = len(tfs)
        
        def series_mul(prev_tf, next_tf):    
            tf_num = np.polymul(prev_tf.num_coef.reshape(len(prev_tf.num_coef)), next_tf.num_coef.reshape(len(next_tf.num_coef)))
            tf_den = np.polymul(prev_tf.den_coef.reshape(len(prev_tf.den_coef)), next_tf.den_coef.reshape(len(next_tf.den_coef)))
            return tf_num, tf_den
        
        for i in range(tf_len-1):
            num, den = series_mul(tfs[0], tfs[1])
            tf = TransferFunction(num, den)
            tfs = (tf,) + tfs[2:]
        
        tfs = tfs[0]
        return tfs
    
    def parallel(*tfs):
        
        tf_len = len(tfs)
        
        def para_mul(prev_tf, next_tf):    
            tf_num = np.add(np.polymul(prev_tf.num_coef.reshape(len(prev_tf.num_coef)), next_tf.den_coef.reshape(len(next_tf.den_coef))), np.polymul(prev_tf.den_coef.reshape(len(prev_tf.den_coef)), next_tf.num_coef.reshape(len(next_tf.num_coef))))
            tf_den = np.polymul(prev_tf.den_coef.reshape(len(prev_tf.den_coef)), next_tf.den_coef.reshape(len(next_tf.den_coef)))
            return tf_num, tf_den
        
        for i in range(tf_len-1):
            num, den = para_mul(tfs[0], tfs[1])
            tf = TransferFunction(num, den)
            tfs = (tf,) + tfs[2:]
        
        tfs = tfs[0]
        return tfs

class StateSpace():
    
    def __init__(self, A, B, C, D):
        self.A = A
        self.B = B
        self.C = C
        self.D = D
        
    def display(self):
        print("X* = AX + Bu \n")
        print("Y = CX + Du \n")
        print("A = " + str(self.A) + "\n")
        print("B = " + str(self.B) + "\n")
        print("C = " + str(self.C) + "\n")
        print("D = " + str(self.D))