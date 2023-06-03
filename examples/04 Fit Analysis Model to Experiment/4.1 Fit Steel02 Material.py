# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 15:13:13 2019
@author: Christian

This example showcases fitting a model parameter (k) to an opensees steel02
damper model using the hysteresis library. We'll select an optimal solution 
from a group of soltions using brute force, but the principle will be the same
for more complicated .

Experimental data is taken from Ganey's 2015 thesis:
    https://digital.lib.washington.edu/researchworks/handle/1773/33664

An openSees analysis is run using the opensees 
analysis file. See that file for explation of how the opensees analysis
is run.


"""

import matplotlib.pyplot as plt
import numpy as np
import hysteresis as hys

# the opensees analysis function live here
from OpenSeesAnalysis import runAnalysis

# Load the experimental data, do some unit conversions
inches = 0.0254
kip = 4.45*10**3
EDataName = "BackboneData.csv"
ExperimentData = np.loadtxt(EDataName,delimiter=',')
Backbonex = ExperimentData[:,0]*inches
Backboney = ExperimentData[:,1]*kip
xyExp = np.column_stack([Backbonex, Backboney])
expHys = hys.Hysteresis(xyExp)

# Define the range of stiffness parameters we want for the model:
Ntrial = 101
stiffness = np.linspace(0.5,1.5,101) * 4*10**6
diffs = []

ii = 0
# Run the trials
for trial in stiffness:
    xy = runAnalysis(trial)
    myHys = hys.Hysteresis(xy)
    diff, _ = hys.compareHys(myHys, expHys)
    diffs.append(diff)
    ii+=1
    print(f'Complete trial {ii}.')
    
# Select the best value from the list!
ind = np.argmin(diffs)
ksolution = stiffness[ind]
print(f'The optimal solution was: {ksolution}')

# =============================================================================
# SHow the chosen plot vs. the data.
# =============================================================================
# Get the optimal solution again
xy = runAnalysis(ksolution)
myHys = hys.Hysteresis(xy)

fig, ax = plt.subplots()
expHys.plot()
myHys.plot()

# =============================================================================
# Find the backbone
# =============================================================================
"""
In this section, we show how to extract the backbone as a fun final step.
"""

k = ksolution
xy = runAnalysis(k, 2)

# Function: get envelope curve
myHys = hys.Hysteresis(xy)
fig, ax = plt.subplots()
myHys.plotVsIndex(True)

# There are 2 repeats at each load protocol step, and 9 steps in total.
lpSteps = [2]*9

# Get the backbone
backbone = hys.getBackboneCurve(myHys, lpSteps)

# Check if the outputs make sense with a plot
fig, ax = plt.subplots()
myHys.plot()    
backbone.plot()


