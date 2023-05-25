# -*- coding: utf-8 -*-
"""
@author: Christian

In this example, plots from section 2.4 of "Hysteresis - A Python Library 
for Analysing Structural Data" from WTCE 2023 are showcased.

Curves in the hysteresis module are compatible with basic operations, i.e.
addition, subtraction, multiplication, and 

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
You can either find this by knowing it - if you ran the experiment,
hopefully you know your load protocol! You can also plot vs. index to find out.
"""
lpSteps = [2]*9

# Make the Hysteresis object
myHys = hys.Hysteresis(xy)

# Get the POSITIVE backbone. Use get getAvgBackboneCurve for the average!
backbone = hys.getBackboneCurve(myHys, lpSteps)


# =============================================================================
# Figure 8 
# =============================================================================

# Make a nice looking plot.
fig, ax = plt.subplots()
myHys.plot(label = 'Analysis Data')
backbone.plot(label = 'Analysis Backbone Data')

ax.set_xlabel('Deformation (mm)')
ax.set_ylabel('Force (kN)')
plt.minorticks_on()
ax.grid(which='major', color='grey', linewidth=0.5, alpha = 0.8)
ax.legend()
ax.legend(loc='lower right')



# =============================================================================
# Figure 9
# =============================================================================
name = 'SPC1'
data = np.loadtxt(name + '.csv', skiprows=2, delimiter = ',')

# Sort the data into a xy curve
x = data[:,1]
y = data[:,0]
xy = np.column_stack([x,y]) 

# Make a hysteresis object
myHys = hys.Hysteresis(xy)

# count the number of repeats in each 'step' of the load protocol
LPsteps = [5,5,5,3,3,3,3]

# Make the backbone curve
bavg, _, _ = hys.getAvgBackbone(myHys, LPsteps, returnPeaks=True)

# Fit the EEEP to the curve
myEEEP = hys.fitEEEP(bavg)

# Make a nice plot!
fig, ax = plt.subplots()
line1 = myHys.plot(linewidth = 0.7, label = 'SPC1 Raw Data')
line2 = bavg.plot(linestyle = '-.', label = 'SPC1 Avg. Backbone')
line3 = myEEEP.plot(color = 'black', label = 'SPC1 EEEP Curve')
plt.minorticks_on()
ax.grid(which='major', color='grey', linewidth=0.5, alpha = 0.8)
ax.grid(which='minor', linewidth=0.5, alpha = 0.4)
ax.legend(loc='lower right')
ax.set_xlabel('Actuator Displacement (mm)')
ax.set_ylabel('Actuator Force (kN)')