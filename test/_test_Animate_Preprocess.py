# -*- coding: utf-8 -*-
"""
Created on Sat May  1 23:49:09 2021

@author: Christian
"""


import numpy as np
import hysteresis.Animate.core as ani
import hysteresis as hys
import scipy

np.random.seed(101)
x = np.linspace(0, 1, 1001)*10
triangleBig = scipy.signal.sawtooth(x*2,0.5)
permutate = np.random.normal(0,1,1001)/2
Ynoise = triangleBig + permutate
Ynoise = scipy.signal.savgol_filter(Ynoise,53,2)
trianglexy = np.column_stack((x, Ynoise))
test1 = hys.Hysteresis(trianglexy)
# test.plot()
permutate = np.random.normal(0,1,1001)/2
Ynoise = triangleBig + permutate
Ynoise = scipy.signal.savgol_filter(Ynoise,53,2)
trianglexy = np.column_stack((x, Ynoise))
test2 = hys.Hysteresis(trianglexy)

permutate = np.random.normal(0,1,1001)/2
Ynoise = triangleBig + permutate
Ynoise = scipy.signal.savgol_filter(Ynoise,53,2)
trianglexy = np.column_stack((x, Ynoise))
test3 = hys.Hysteresis(trianglexy)


# xyAni = ani.getAnixy(trianglexy, 2)

# frames  =ani.getAniFrames(trianglexy[:,0], 0.1)

# myAnimation = ani.Animation(test1,1,5)
# myAnimation.Animate()

myAnimation = ani.JointAnimation([test1, test2,test3],1,5)
myAnimation.Animate()

# myAnimation = ani.Animation(test,1,5)
# myAnimation.Animate()