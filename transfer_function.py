# -*- coding: utf-8 -*-
"""
Created on Thu May 28 19:31:48 2020

@author: Rushad
"""

def transfer_function(num_coef, den_coef, disp=False):
    '''
    Parameters
    ----------
    num_coef : TYPE : Numpy Array 
        DESCRIPTION: Numpy array of coefficients of the numerator of transfer function
    den_coef : TYPE: Numpy Array
        DESCRIPTION: Numpy array of coefficients of the denominator of transfer function
    disp : TYPE, optional
        DESCRIPTION. The default is False.

    Returns
    -------
    tf : TYPE: dict
        DESCRIPTION: dictionary consisting of TF data
    '''
    num_coef = num_coef.reshape([len(num_coef), 1])
    den_coef = den_coef.reshape([len(den_coef), 1])
    
    tf = {"num":num_coef, "den":den_coef}
    
    if disp == True:
        num_str = ""
        for n in range(len(num_coef)):
            
            if n < len(num_coef)-1:
                if num_coef[n] > 1:
                    #print("S^" + str(int(num_coef[n])) + " + ")
                    num_str = num_str + "S^" + str(int(num_coef[n])) + " + "
                elif num_coef[n] == 1:
                    #print("S + ")
                    num_str = num_str + "S + "
                elif num_coef[n] == 0:
                    #print("1 + ")
                    num_str = num_str + "1 + "
            else:
                if num_coef[n] > 1:
                    #print("S^" + str(int(num_coef[n])))
                    num_str = num_str + "S^" + str(int(num_coef[n]))
                elif num_coef[n] == 1:
                    #print("S")
                    num_str = num_str + "S"
                elif num_coef[n] == 0:
                    #print("1")
                    num_str = num_str + "1"
              
        den_str = ""
        for d in range(len(den_coef)):
            
            if d < len(den_coef)-1:
                if den_coef[d] > 1:
                    #print("S^" + str(int(den_coef[d])) + " + ")
                    den_str = den_str + "S^" + str(int(den_coef[d])) + " + "
                elif den_coef[d] == 1:
                    #print("S + ")
                    den_str = den_str + "S + "
                elif den_coef[d] == 0:
                    #print("1 + ")
                    den_str = den_str + "1 + "
            else:
                if den_coef[d] > 1:
                    #print("S^" + str(int(den_coef[d])))
                    den_str = den_str + "S^" + str(int(den_coef[d]))
                elif den_coef[d] == 1:
                    #print("S")
                    den_str = den_str + "S"
                elif den_coef[d] == 0:
                    #print("1")
                    den_str = den_str + "1"
    
    div_line_len = max(len(num_str), len(den_str))
    div_line = div_line_len*"-"
    tf_disp = str(num_str + " \n" + div_line + " \n" + den_str)
    if disp == True:
        return tf, tf_disp
    else:
        return tf

