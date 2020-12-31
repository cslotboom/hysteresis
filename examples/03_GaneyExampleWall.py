# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 15:13:13 2019
@author: Christian
"""
import numpy as np
import scipy
from scipy.interpolate import interp1d
from numpy import trapz

import matplotlib.pyplot as plt

from hysteresis import data
import hysteresis as hys

import openseespy
import time

# =============================================================================
# Load initial stuff
# =============================================================================

Wall_exp = np.loadtxt('TS1_Experiment_Shear.csv',delimiter=',')
Wall_analysis_disp = np.loadtxt('Ts1_Load_Dsp.out',delimiter=' ')[1:, 1]
Wall_analysis_shear =np.loadtxt('Ts1_Wall_Reaction.out',delimiter=' ')[1:, 1]

Wall_exp_xy = np.column_stack([Wall_exp[:,0], Wall_exp[:,1]/1000])
Wall_anal_xy = np.column_stack([Wall_analysis_disp, -Wall_analysis_shear/1000])



# =============================================================================
# TestHys. Ganey wall
# =============================================================================

# Let's start by looking at the load protocol for 
NCycles = 3
DriftRatio = np.array([0.035 ,0.05, 0.075 ,0.1, 0.15, 0.2, 0.3, 0.4, 0.6, 
                        0.9   ,1.35, 2.0,   3.0, 4.0])*4.1/100


# Lets first load our hysteresis
ExpHys = hys.Hysteresis(Wall_exp_xy)
# ExpHys.plot(True)
print(ExpHys.NCycles)


# There are way too many cycles found early on!
# Let's plot vs. the index
# ExpHys.plotVsIndex()


# We have a few options - we can try to filter our data. Here it might be simpler
# just to remove the extranious points. After some trial and error, we try 
# Removing the first 8400 points
ExpHys = hys.Hysteresis(Wall_exp_xy[8300:,:])
# ExpHys.plotVsIndex(True)
# ExpHys.plotLoadProtocol()
print(ExpHys.NCycles)


# There are still more cycles than we'd like. 
exploadProtocol = ExpHys.loadProtocol


# Better, but there are still more cycles than we'd like. 
# Lets filter out any peak that has a prominence less than the target input
ExpHys.recalculateCycles(peakProminence = DriftRatio[0]/2)
# ExpHys.plotVsIndex(True)
# ExpHys.plotLoadProtocol(comparisonProtocol = DriftRatio)
print(ExpHys.NCycles)


# We're doing pretty good, lets make our analysis hystersis now
AnalHys = hys.Hysteresis(Wall_anal_xy)
# AnalHys.plot(True)
# AnalHys.plotLoadProtocol(comparisonProtocol = ExpHys.loadProtocol)


# Because there are few data points int the experimental data set, I'm 
# comfortable skipping the initial cycles. We can filter them out with a promenence comand
AnalHys.recalculateCycles(peakProminence = 0.005)
# AnalHys.plotLoadProtocol(comparisonProtocol = ExpHys.loadProtocol)


# Almost there! It looks like we are missing one of the Analysis points
# To get there, lets cut off the appropriate number of points
AnalHys = hys.Hysteresis(Wall_anal_xy[500:,:])
AnalHys.recalculateCycles(peakProminence = 0.0045)
# AnalHys.plotLoadProtocol(comparisonProtocol = ExpHys.loadProtocol)


# =============================================================================
# Plot both Hystereses
# =============================================================================

# fig, ax = AnalHys.plot()
# plt.plot(Diffs)
# ax.set_xlabel('Actuator Drift (m)')
# ax.set_ylabel('Average difference between Curves (kN)')
# plt.minorticks_on()
# ax.grid(which='major', color='grey', linewidth=0.5, alpha = 0.8)
# ax.grid(b=True, which='minor', linewidth=0.5, alpha = 0.4)










# =============================================================================
# resample
# =============================================================================


# Now we can resample and compare the curves!
AnalHysDx = hys.resample(AnalHys, 10)
ExpHysDx = hys.resample(ExpHys, 10)
AnalHysDx.plotLoadProtocol(comparisonProtocol = ExpHysDx.loadProtocol)
AnalHysDx.plot(True)
ExpHysDx.plot(True)

Diff, Diffs = hys.compareHys(AnalHysDx, ExpHysDx)

# We can plot the difference over each cycle
fig, ax = plt.subplots()
plt.plot(Diffs)
ax.set_xlabel('Cycle (#)')
ax.set_ylabel('Average difference between Curves (kN)')
plt.minorticks_on()
ax.grid(which='major', color='grey', linewidth=0.5, alpha = 0.8)
ax.grid(b=True, which='minor', linewidth=0.5, alpha = 0.4)


# =============================================================================
# Cumulative Deformation
# =============================================================================

fig, ax = ExpHys.plot(True)
fig, ax = ExpHys.plotCumArea(True)

ax.set_xlabel('Cumulative Drift (mm)')
ax.set_ylabel('Energy (kNm)')
plt.minorticks_on()
ax.grid(which='major', color='grey', linewidth=0.5, alpha = 0.8)
ax.grid(b=True, which='minor', linewidth=0.5, alpha = 0.4)


