# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 15:25:37 2020

@author: Rushad
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal.filter_design import freqs

class bode():
    
    def __init__(self):
        pass
    
    def freqresp(self, tf, w=None, n=10000):
        w, h = freqs(tf.num_coef.flatten(), tf.den_coef.flatten())
        return w, h

    def bode(self, system, w=None, n=100, ret=False, show=True):
        
        w, y = self.freqresp(system, w=w, n=n)
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