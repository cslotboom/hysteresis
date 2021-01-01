# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 23:47:36 2020

@author: Christian
"""
import hysteresis as hys
import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit
# Note, 2D array


data =  np.array([[-0.724, -0.834], [-0.680, -1.239], [-0.479, -1.032],
                  [-0.488, -0.871], [-0.526, -0.774], [-0.331, -0.741], 
                  [-0.008, -0.596], [0.060, -0.430],  [0.204, -0.256],
                  [0.289, 0.024],   [0.369, 0.234],   [0.554, 0.655],
                  [0.545, 0.724],   [0.635, 0.857],   [0.564, 0.868],
                  [0.368, 0.858],   [0.385, 0.725],   [0.349, 0.636],
                  [0.181, 0.496],   [0.042, 0.399],   [-0.204, 0.120],
                  [-0.380, 0.002],  [-0.429, -0.131], [-0.655, -0.421]])

Npoints = len(data)
t = np.arange(0, Npoints)/Npoints


def f(x, a, b):
    return a*x + b

def g(t, b, c, Cx):
    return b*np.cos(2*np.pi*t + c) + Cx

def geth(n = 1, m = 1):

    def h(t, a, b,c,d, Cy):
        return a*np.cos(2*np.pi*t + b)**n + c*np.sin(2*np.pi*t + d)**m + Cy
    
    return(h)

h = geth()

out = curve_fit(f, data[:,0], data[:,1])
out2 = curve_fit(g, t, data[:,0])
out3 = curve_fit(h, t, data[:,1])

fig, ax = plt.subplots()
# plt.plot(data[:,0], data[:,1], '.', linewidth = 0)
# plt.plot(data[:,0], f(data[:,0], *out[0]))
# plt.plot(g(t, *out2[0]), data[:,1])
plt.plot(t, g(t, *out2[0]))
plt.plot(t, h(t, *out3[0]))

fig, ax = plt.subplots()
plt.plot(data[:,0], data[:,1], '.', linewidth = 0)
plt.plot(g(t, *out2[0]), h(t, *out3[0]))
# smallTriangles.setArea()
# Anet = smallTriangles.getNetArea()
# 0.004982994450842999