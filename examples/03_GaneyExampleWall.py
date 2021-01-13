# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 15:13:13 2019
@author: Christian
"""
import numpy as np
import matplotlib.pyplot as plt
import hysteresis as hys


# =============================================================================
# Load initial stuff
# =============================================================================

# in the first step we'll load our data and create the necessary arrays
Wall_exp = np.loadtxt('TS1_Experiment_Shear.csv', delimiter=',')
Wall_analysis_disp = np.loadtxt('Ts1_Load_Dsp.out', delimiter=' ')[1:, 1]
Wall_analysis_shear =np.loadtxt('Ts1_Wall_Reaction.out', delimiter=' ')[1:, 1]

Wall_exp_xy = np.column_stack([Wall_exp[:,0], Wall_exp[:,1]/1000])
Wall_anal_xy = np.column_stack([Wall_analysis_disp, -Wall_analysis_shear/1000])

# We'll also input the absolute value of the load protocol
loadProtocol = np.array([0.035 ,0.05, 0.075 ,0.1, 0.15, 0.2, 0.3, 0.4, 0.6, 
                       0.9   ,1.35, 2.0,   3.0, 4.0])*4.1/100

# We want this may cycles total!
Ncycles = len(loadProtocol)*3
Indexes = np.ones_like(loadProtocol, dtype=int) * 3
loadProtocolout = hys.protocol.createProtocol(loadProtocol, Indexes)

# =============================================================================
# TestHys. Ganey wall
# =============================================================================

# Lets first load make our experimental hysteresis object
ExpHys = hys.Hysteresis(Wall_exp_xy)
ExpHys.plot()
# We can find out out how many cycles the initial hysteresis has
print(ExpHys.NCycles)


# Wow, there are way too many cycles early on!
# Let's make a new plot of the values vs. the index of each point to see what's
# going on. We will turn on the plot cycles option to see where out cycles are.
fig, ax = ExpHys.initFig()
ExpHys.plotVsIndex(True)

# It looks like we are picking up a whole bunch of noise.
# We have a few options to remove this - One thing we may try is to 
# just to remove the extranious points. After some trial and error, we try 
# Removing the first 8300 points
ExpHys = hys.Hysteresis(Wall_exp_xy[8300:,:])

# let's make a new figure and plot the results again
fig, ax = ExpHys.initFig()
ExpHys.plotLoadProtocol()
print(ExpHys.NCycles)


# Better, but there are still more cycles than we'd like. 
# Lets filter out any peak that has a prominence less than the target input
# The peakProminence filter removes peaks that aren't of a certain height
# compared to the surrounding peaks

# We will remove all peaks with prominence less than half the first value in
# the load protocol. 
ExpHys.recalculateCycles(peakProminence = loadProtocol[0]/2)
fig, ax = ExpHys.initFig()
# ExpHys.plotVsIndex(True)
ExpHys.plotLoadProtocol(comparisonProtocol = loadProtocol)

# Printing the number of cycles, we see that we're at the 
print(ExpHys.NCycles)


# We're doing pretty good, lets make our analysis hystersis now
AnalHys = hys.Hysteresis(Wall_anal_xy)
AnalHys.initFig()
AnalHys.plot(True)


# Because there are few data points int the experimental data set, I'm 
# comfortable skipping the initial cycles. We can filter them out 
# by recalculating the peaks with a prominence comand
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

fig, ax = plt.subplots()
ExpHys.plot()
AnalHys.plot()
ax.set_xlabel('Actuator Drift (m)')
ax.set_ylabel('Average difference between Curves (kN)')
plt.minorticks_on()
ax.grid(which='major', color='grey', linewidth=0.5, alpha = 0.8)
ax.grid(b=True, which='minor', linewidth=0.5, alpha = 0.4)










# =============================================================================
# resample
# =============================================================================


# Now we can resample and compare the curves!
AnalHysDx = hys.resample(AnalHys, 10)
ExpHysDx = hys.resample(ExpHys, 10)
fig, ax = plt.subplots()
AnalHysDx.plotLoadProtocol(comparisonProtocol = ExpHysDx.loadProtocol)

fig, ax = plt.subplots()
AnalHysDx.plot(True)

fig, ax = plt.subplots()
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
fig, ax = ExpHys.initFig()
ExpHys.plot(True)

fig, ax = ExpHys.initFig()
ExpHys.plotCumArea(True)
ax.set_xlabel('Cumulative Drift (mm)')
ax.set_ylabel('Energy (kNm)')
plt.minorticks_on()
ax.grid(which='major', color='grey', linewidth=0.5, alpha = 0.8)
ax.grid(b=True, which='minor', linewidth=0.5, alpha = 0.4)


