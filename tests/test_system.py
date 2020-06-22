# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 19:03:05 2020

@author: Rushad
"""
import os
import sys
sys.path.append(os.getcwd())

import numpy as np
import system

s = system.TransferFunction([9], [1,4,9])
f = system.feedback(s, H=2)

def test_param_sys():
    s.parameters()
    assert s.order == 2
    assert s.gain == 1
    assert s.natural_frequency == 3
    assert round(s.damping_ratio, 2) == 0.67

def resp():
    exp = np.array([0.000000000000000000e+00,1.363228105640982291e-01,4.053197430745426599e-01,6.692282750367345434e-01,8.673716448218102837e-01,9.883047390441740410e-01,1.045456580991569906e+00,1.060202736406757662e+00,1.052347846841237722e+00,1.036227015843563803e+00,1.020269655010540122e+00,1.008224023100995792e+00,1.000833420179654043e+00,9.973121428986893022e-01,9.963764502287294489e-01,9.968276008818350853e-01,9.977933836424620617e-01,9.987581025771694598e-01,9.994902964519694066e-01,9.999418930559381691e-01,1.000158785146602058e+00,1.000218047925908404e+00,1.000192228616730628e+00,1.000134389865129814e+00,1.000076075997813119e+00])
    response = s.response("step", time_period=5, ret=True)
    assert np.array_equal(response, exp)

def test_stability():
    s.stability() == 'System is Stable'
    
def test_param_feedback():
    f.parameters()
    assert s.order == 2
    assert round(f.gain, 2) == 0.67
    assert round(f.natural_frequency, 2) == 3.67
    assert round(f.damping_ratio, 2) == 0.54

