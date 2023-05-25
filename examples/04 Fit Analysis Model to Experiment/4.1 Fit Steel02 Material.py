# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 15:13:13 2019
@author: Christian

This example showcases fitting a model parameter (k) to a model using 
the hysteresis library. An openSees analysis is run using the opensees 
analysis file.

"""


import matplotlib.pyplot as plt
import hysteresis as hys

from OpenSeesAnalysis import runAnalysis

# Here we get our data from 
# Run an opensees analysis using the runAnalysis Comand
k = 3.2*10**6
xy = runAnalysis(k)


# There are 2 repeats at each load protocol step, and 9 steps in total.
lpSteps = [2]*9

# =============================================================================
# Find the backbone
# =============================================================================

# Function: get envelope curve
myHys = hys.Hysteresis(xy)
myHys.plotVsIndex(True)

# Get the backbone
backbone = hys.getBackboneCurve(myHys, lpSteps)

# Check if the outputs make sense with a plot
fig, ax = plt.subplots()
myHys.plot()    
backbone.plot()


