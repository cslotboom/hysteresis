# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 15:13:13 2019
@author: Christian
"""
import numpy as np
import matplotlib.pyplot as plt
import hysteresis as hys

from OpenSeesAnalysis import runAnalysis
from scipy.interpolate import interp1d


# =============================================================================
# Load initial stuff
# =============================================================================

# Run an opensees analysis using the runAnalysis Comand
k = 3.2*10**6
xy = runAnalysis(k)
lpSteps = [2]*9

skipEnd = 0
skipStart = 0

# =============================================================================
# Find the backbone
# =============================================================================

# InputParser - Decides what to do with the variable LoadProtcol
# if you get an interger use that for all cycles
shift = lpSteps[0] - 1
Indexes = np.concatenate([[0], np.cumsum(lpSteps,dtype=int) - shift])

# Function: get envelope curve
analHys = hys.Hysteresis(xy)
analHys.plotVsIndex(True)

# Get the backbone
backbone = hys.getBackboneCurve(analHys, lpSteps)

# Check if the outputs make sense with a plot
fig, ax = plt.subplots()
analHys.plot()
backbone.plot()


