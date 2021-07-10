# -*- coding: utf-8 -*-
"""
Created on Sat May 29
@author: Christian

An example of how to find the a equivalent elastic perfectly plastic curve 
for a set of input data, using the ASTM E2126 methodology:
    http://www.materialstandard.com/wp-content/uploads/2019/10/E2126-11.pdf


The raw data was provided by Dr. Thomas Tannert at the University of Northern 
British Columbia:
    http://blogs.unbc.ca/thomastannert/

Drexler M, Dires S, Tannert T (2021) 
Internal perforated-steel-plate connections for CLT shear walls. 
In proceedings of World Conference for Timber Engineering, Santiago de Chile. 

"""

import numpy as np
import matplotlib.pyplot as plt
import hysteresis as hys

# Load the input data using numpy's loadtxt function.
name = 'SPC1'
data = np.loadtxt(name + '.csv', skiprows=2, delimiter = ',')

# Sort the data into a xy curve
x = data[:,1]
y = data[:,0]
xy = np.column_stack([x,y]) 

# Make a hysteresis object
myHys = hys.Hysteresis(xy)

# Plot the object to see if the cycles are detected properly.
# This data is really clean, good job Dr. Tannert!
fig, ax = plt.subplots()
myHys.plotVsIndex(True)

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
ax.grid(b=True, which='minor', linewidth=0.5, alpha = 0.4)
ax.legend(loc='lower right')
ax.set_xlabel('Actuator Displacement (mm)')
ax.set_ylabel('Actuator Force (kN)')

