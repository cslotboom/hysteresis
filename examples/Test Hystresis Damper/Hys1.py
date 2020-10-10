# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 22:19:58 2020

@author: Christian
"""

import numpy as np
import hysteresis.hys as hys
import matplotlib.pyplot as plt

# load the .csv Data
InputName    = 'Hys1.csv'
LPName       = 'LoadProtocol.csv'
EnergyName   = 'Hys1_Energy.csv'
xyData       = np.loadtxt(InputName,         delimiter=',')
LoadProtocol = np.loadtxt(LPName,  delimiter=',',skiprows = 1)
Energy       = np.loadtxt(EnergyName,  delimiter=',')

# some small adjustments
xyData = xyData[:-21,:]
xyData[-1,0] = xyData[-1,0] + 0.6

# Create the trace Hysteresis
hysTrace = hys.Hysteresis(xyData)
hysTrace.plotLoadProtocol()
fig, ax = hysTrace.plot(True)

# Expand the hysteresis 
FullHys = hys.exandHysTrace(hysTrace, LoadProtocol[:,2], skipStart = 1, skipEnd = 2)
FullHys.plot()
 
# Plot the load Protocol
FullHys.plotLoadProtocol()
hysProt = FullHys.loadProtocol

# Get cumulative displacement and area
cumDisp = FullHys.getCumDisp() + 6
cumArea = FullHys.getCumArea()/1000

# Make a nice plot
fig, ax = plt.subplots()
ax.plot(cumDisp, cumArea, label = 'Hysteresis Analysis')
ax.plot(Energy[:,0],Energy[:,1], label = 'Chan and Albermani')
ax.set_xlabel('Cumulative Deformation (mm)')
ax.set_ylabel('Cumulative Energy (kJ)')
plt.minorticks_on()
ax.grid(which='major', color='grey', linewidth=0.5, alpha = 0.8)
ax.grid(b=True, which='minor', linewidth=0.5, alpha = 0.4)
ax.legend()





