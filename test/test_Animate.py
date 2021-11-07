# -*- coding: utf-8 -*-
"""
Created on Sat May  1 23:49:09 2021

@author: Christian
"""


import numpy as np
import hysteresis.plotSpecial.animate as ani

import matplotlib.pyplot as plt
import matplotlib.lines as lines
import hysteresis as hys
import scipy

np.random.seed(101)
x = np.linspace(0, 1, 101)*10
y = np.sin(x)
trianglexy = np.column_stack((x, y))

test = hys.Hysteresis(trianglexy)
# testBase = ani.AnimationBase()
# testBase.initAnimation()
skipStart  =3
skipEnd = 3
myAnimation = ani.Animation(test, skipStart = 3, skipEnd = 3)
# Animation
# myAnimatino.skipStartEnd


def test_skip():
    
    xy = myAnimation.skipStartEnd(trianglexy, skipStart, skipEnd)
    assert len(xy) == 101 - skipStart - skipEnd

def test_skip_start():
    
    xy = myAnimation.skipStartEnd(trianglexy, skipStart, 0)
    assert len(xy) == 101 - skipStart
    
def test_update(monkeypatch):
    """ Tests if the cycles can plot correctly"""
    
    monkeypatch.setattr(plt, 'show', lambda: None)
    myAnimation.initAnimation()
    line, = myAnimation.update(10)
    test1 = isinstance(line, lines.Line2D)
    temp = trianglexy[skipStart:-skipEnd,:]
    x, y = line.get_data()
    # print(temp[:10,:] )
    # print(line._xy )
    test2 = np.all(y - temp[:10,1] == 0)
    
    test =  np.all([test1, test2])
    
    assert test
    



