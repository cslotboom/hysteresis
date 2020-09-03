# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 23:47:36 2020

@author: Christian

This tests if a simple cicle works
"""
import hysteresis as hys
import numpy as np
import matplotlib.pyplot as plt


def MakeCircle():
    basePoints = np.linspace(0,1,1000)*2*np.pi
    testCirclex = np.sin(basePoints)
    testCircley = np.cos(basePoints)
    Circlexy = np.column_stack((testCirclex, testCircley))

    Circle = hys.Hysteresis(Circlexy)

    return Circle

def test_Circle_Area():
    """ Test the net area of the circle """
    Circle = MakeCircle()
    NetArea = Circle.getNetArea()
    
    assert abs(NetArea - np.pi) < 0.0001
    
def test_Circle_SLope():
    """ Test the slope area of the circle """
    Circle = MakeCircle()
    Cycle1 = Circle.getCycle(0)
    Cycle1.setSlope()
    x = Cycle1.xy[:,0]
    ind = np.argmin( abs(x - 0.5))
    testSlope = -x[ind] / (1 - x[ind]**2)**0.5
    
    Slope2 = Cycle1.Slope[ind]
    
    assert abs(testSlope - Slope2) < 10**-5

def test_Circle_Plot(monkeypatch):
    monkeypatch.setattr(plt, 'show', lambda: None)
    
    Circle = MakeCircle()
    fig, ax = Circle.plotCycles()
    Circle.plot(plotCycles=True)
    Circle.plotSlope(plotCycles=True, ylim = [-10,10])
    
    assert True == True

def test_Circle_Subvector_Plot(monkeypatch):
    monkeypatch.setattr(plt, 'show', lambda: None)
    
    Circle = MakeCircle()
    Vector1 = Circle.Cycles[0]
    Vector2 = hys.reSample(Vector1, 30)
    Vector3 = hys.reSample(Circle, 10)
    
    Vector1.plot()
    Vector2.plot()
    Vector3.plot(True)
    
    assert True == True

