# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 22:19:58 2020

An example of finding the energy in a seismic damper.


@author: Christian
"""


import numpy as np
import hysteresis as hys
import time
import matplotlib.pyplot as plt


InputName = 'Hys1.csv'
LoadProtocolName = 'LoadProtocol.csv'
EnergyName = 'Hys1_Energy.csv'

xyData          = np.loadtxt(InputName,         delimiter=',')
LoadProtocol    = np.loadtxt(LoadProtocolName,  delimiter=',',skiprows = 1, dtype = int)
Energy   = np.loadtxt(EnergyName,  delimiter=',')

xyData[:,1] = xyData[:,1]/1000
Energy[:,1] = Energy[:,1]



# Make a few plots
hysTrace = hys.Hysteresis(xyData)

fig, ax = hysTrace.initFig()
hysTrace.plotLoadProtocol()

fig, ax = hysTrace.initFig()
hysTrace.plot(True)

fig, ax = hysTrace.initFig()
hysTrace.plotCycles()

# Expand the hysteresis trace
hysProt = hysTrace.loadProtocol
cycles = hysTrace.cycles
FullHys = hys.exandHysTrace(hysTrace, LoadProtocol[3:,2], skipStart = 1, skipEnd = 3)

# Get cumulative area and displacement.
cumulativex = FullHys.getCumDisp()
netDisp = FullHys.getNetCumDisp()
cumulativeArea = FullHys.getCumArea()


fig, ax = FullHys.initFig()
FullHys.plotCumArea(True)
ax.set_xlabel('Cumulative Deformation (mm)')
ax.set_ylabel('Energy (kNm)')
plt.minorticks_on()
ax.grid(which='major', color='grey', linewidth=0.5, alpha = 0.8)
ax.grid(b=True, which='minor', linewidth=0.5, alpha = 0.4)

# lines = fig.axes[0].lines
# for line in lines:
#     plt.setp(line, linestyle='--')





