# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 15:13:13 2019
@author: Christian
"""
import numpy as np
import matplotlib.pyplot as plt
import hysteresis as hys

xFile = 'Disp.out'
yFile = 'RFrc.out'

xdata = np.loadtxt(xFile, delimiter = ' ' , skiprows = 2)
ydata = np.loadtxt(yFile, delimiter = ' ' , skiprows = 2)
x  = -xdata[:,1] * 1000
y  = ydata[:,1] / 1000
xy = np.column_stack([x,y])

"""
There are 2 repeats at each load protocol step, and 9 steps in total.
You can either find - if you ran the experiment, hopefully you know your load 
protocol! You can also plot vs. index to find out the number of repeasts
"""
lpSteps = [2]*9

# Make the Hysteresis object
myHys = hys.Hysteresis(xy)

# Get the POSITIVE backbone. Use get getAvgBackboneCurve for the average!
backbone = hys.getBackboneCurve(myHys, lpSteps)

# Make a nice looking plot.
fig, ax = plt.subplots()
myHys.plot(label = 'Analysis Data')
backbone.plot(label = 'Analysis Backbone Data')

ax.set_xlabel('Deformation (mm)')
ax.set_ylabel('Force (kN)')
plt.minorticks_on()
ax.grid(which='major', color='grey', linewidth=0.5, alpha = 0.8)
ax.grid(which='minor', linewidth=0.5, alpha = 0.4)
ax.legend()
ax.legend(loc='lower right')
