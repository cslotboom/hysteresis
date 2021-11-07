# -*- coding: utf-8 -*-
"""
Created on Sat May  1 23:49:09 2021

@author: Christian
"""


import numpy as np
import hysteresis.plotSpecial.animate as ani
import hysteresis as hys
import pytest

np.random.seed(101)
x = np.linspace(0, 1, 101)*10
y1 = np.sin(x)
y2 = np.cos(x)

x2 = np.linspace(0, 1, 10)

trianglexy1 = np.column_stack((x, y1))
trianglexy2 = np.column_stack((x, y2))
trianglexy3 = np.column_stack([x2, x2])
test1 = hys.Hysteresis(trianglexy1)
test2 = hys.Hysteresis(trianglexy2)
test3 = hys.Hysteresis(trianglexy3)


def test_validate_pass():
    
    curves = [test1, test2]
    ani.JointAnimation(curves)


def test_validate_fail():

    with pytest.raises(Exception):
        curves = [test1, test2, test3]
        ani.JointAnimation(curves)
