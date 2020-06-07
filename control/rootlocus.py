# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 16:20:26 2020

@author: Rushad
"""

import numpy as np
import matplotlib.pyplot as plt

def rootlocus(tf, gain_range=10.0):
    '''
    Parameters
    ----------
    tf : Transfer Function object
        DESCRIPTION. TF object whose root locus we want to find
    gain_range : float / int, optional
        DESCRIPTION. Range of the gain. The default is 10.0.

    Returns
    -------
    Root Locus plot of the system

    '''
    
    gains = np.linspace(0.0, float(gain_range), num=500)
    
    num = tf.num_coef
    num = list(tf.num_coef.reshape(len(num),))    
    den = tf.den_coef
    den = list(tf.den_coef.reshape(len(den),))
    size = len(den) - len(num)
    temp = np.zeros(size)
    num = np.concatenate((temp, num))
    tf = np.vstack((num, den))
    
    def compute_roots(tf, gains):
      num, den = tf[0], tf[1]
      roots = []
    
      for gain in gains:
        ch_eq = den +  gain*num
        ch_roots = np.roots(ch_eq)
        ch_roots.sort()
        roots.append(ch_roots)
    
      # convert final roots list into array
      roots = np.vstack(roots)
    
      return roots


    def plot_root_locus(gains, roots):
        
      real_vals = np.real(roots)
      imag_vals = np.imag(roots)
    
      colors = ['b', 'm', 'c', 'r', 'g']
    
      fig, ax = plt.subplots()
      ax.set_xlabel('Re')
      ax.set_ylabel('Im')
      ax.axvline(x=0, color='k', lw=1)
      ax.grid(True, which='both')
    
      # plots a blue "x" for the first roots
      ax.scatter(real_vals[0, :], imag_vals[0, :],
              marker='x',
              color='blue')
    
      # plots a red "o" for the last roots
      ax.scatter(real_vals[-1, :], imag_vals[-1, :], marker='o', color='red')
    
      temp_real_vals = real_vals[1:-1, :]
      temp_imag_vals = imag_vals[1:-1, :]
      color_range = range(temp_real_vals.shape[1])
    
      # plot the rest of the roots in different colors with respect to the regions
      for r, i, j in zip(temp_real_vals.T, temp_imag_vals.T, color_range):
        ax.plot(r, i, color=colors[j])
    
      return fig, ax
  
    roots = compute_roots(tf, gains)
    fig, ax = plot_root_locus(gains, roots)
    plt.show()