# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 22:19:58 2020

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




hysTrace = hys.Hysteresis(xyData)
hysTrace.plotLoadProtocol()
hysTrace.plot(True)
hysTrace.plotCycles()

# print(hysTrace.loadProtocol)
# print(LoadProtocol[:,1])

hysProt = hysTrace.loadProtocol
cycles = hysTrace.Cycles

FullHys = hys.exandHysTrace(hysTrace, LoadProtocol[3:,2], skipStart = 1, skipEnd = 3)
FullHys.plot(True)
# FullHys.plotLoadProtocol(comparisonProtocol = LoadProtocol[:,1])


cumulativex = FullHys.getCumDisp()
netDisp = FullHys.getNetCumDisp()
cumulativeArea = FullHys.getCumArea()






fig, ax = FullHys.plotCumArea(True)
# ax.plot(Energy[:,0],Energy[:,1])
ax.set_xlabel('Cumulative Deformation (mm)')
ax.set_ylabel('Energy (kNm)')
plt.minorticks_on()
ax.grid(which='major', color='grey', linewidth=0.5, alpha = 0.8)
ax.grid(b=True, which='minor', linewidth=0.5, alpha = 0.4)

lines = fig.axes[0].lines
for line in lines:
    plt.setp(line, linestyle='--')





