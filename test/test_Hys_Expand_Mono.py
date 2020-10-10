# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 23:47:36 2020

@author: Christian
"""
import hysteresis.hys as hys
import numpy as np
import matplotlib.pyplot as plt
        

def test_getReturnCycle():
    """ Tests if the getReturnCycle function"""
    t = np.linspace(0,1,101)
    x1 = 1 - 1.5*t
    y1 =  (3)*x1**2 - 1
    x2 = x1[-1] + t*2
    y2 = y1[-1] + t*4
    
    
    TestCycle1 = hys.SimpleCycle(np.column_stack([x1,y1]))
    TestCycle2 = hys.SimpleCycle(np.column_stack([x2,y2]))
    TestCycle3 = hys.getReturnCycle(TestCycle1, TestCycle2)
    
    xySolution = np.zeros([76,2])
    xySolution[:75, :] = TestCycle2.xy[:75, :]
    xySolution[-1, :] = TestCycle1.xy[0, :]
    
    assert(np.all(xySolution == TestCycle3.xy))
    