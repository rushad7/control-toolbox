# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 15:25:37 2020

@author: Rushad
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal.filter_design import freqs

class bode():
    '''
    Bode Plot of TF
    '''
    def __init__(self):
        pass
    
    def freqresp(self, tf):
        '''
        Parameters
        ----------
        tf : TransferFuction object
            DESCRIPTION. TF of which frequency resonse is needed
            
        Returns
        -------
        w : numpy array
            DESCRIPTION. Angular Frequency array [rad/s]
        h : numpy array
            DESCRIPTION. response of the system
        '''
        
        w, h = freqs(tf.num_coef.flatten(), tf.den_coef.flatten())
        return w, h

    def bode(self, system, ret=False, show=True):
        '''
        Parameters
        ----------
        system : TransferFunction object
            DESCRIPTION. TF object of which bode plot is needed
        ret : bool, optional
            DESCRIPTION. Return w, mag, phase. The default is False.
        show : bool, optional
            DESCRIPTION. Plot the response. The default is True.

        Returns
        -------
        w : numpy array
            DESCRIPTION. Frequency array
        mag : numpy array
            DESCRIPTION. magnitude array
        phase : numpy array
            DESCRIPTION. phase array
        '''
        
        w, y = self.freqresp(system)
        mag = 20.0 * np.log10(abs(y))
        phase = np.unwrap(np.arctan2(y.imag, y.real)) * 180.0 / np.pi
        
        if show == True:
            plt.figure()
            plt.semilogx(w, mag)
            plt.figure()
            plt.semilogx(w, phase)
            plt.show()
        
        if ret == True: 
            return w, mag, phase