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

from openseespytools import data
import openseespytools.hysteresis as hys

import openseespy
import time



"""
In this example I will show some of the basic functionality of our hystresis


"""
# =============================================================================
# Load initial stuff
# =============================================================================

# We will load the hystresis test data, and 
testHys = np.loadtxt('BackboneData.csv',delimiter=',')
disp = np.loadtxt('Disp.out',delimiter=' ')
force = np.loadtxt('RFrc.out',delimiter=' ')

testHys2 = np.column_stack([disp[:,1], -force[:,1]])

# =============================================================================
# Test hysteresis, Ganey UFP
# =============================================================================

"""
First, we create the hysteresis object from our xy input information. 
The hystresis object represents a curve that changes several times.

If needed, we can access the xy data of the hystresis.

"""

DamperHys = hys.Hysteresis(testHys)
xy = DamperHys.xy


"""
We can then show some of the outputs. Lets use some of the basic plotting 
features to visualize our data. Here we use the plot command to create a plot
of our data.
"""

DamperHys.plot()

"""
All outputs are matplotlib plots, so we can make changes after the plotting.
Let's add some labels to our chart!
"""

fig, ax = DamperHys.plot()
ax.set_xlabel('Actuator Displacement (mm)')
ax.set_ylabel('Applied Force (kN)')


""" 
By defualt, hysteresis objects will try to find revesal points in our data, and 
break the curve up into a number of cycles. We can access and plot these cycles.

The data we are working with is quite smooth, and the default settings did a 
good job of finding reversal points! You might have to play around with the 
input settings.
"""
reversalIndexes = DamperHys.reversalIndexes

Cycle = DamperHys.getCycle(1)
Cycle.plot()
DamperHys.plotCycles(plotCycles = True)


# DamperHys.plotCycles([0,1,5,18,19], True, labelCycles = [0,1,5,18,19])


"""
By default, the hystresis will numerically estimate the area under each point
on the curve, as well as the slope. We can access and plot these quantities!

Note that slope is undefined at reversal points. 

You can subsitute your own function to estimate area or slope if you'd like!
"""

Area = DamperHys.Area
NetArea = DamperHys.getNetArea()

Slope = DamperHys.Slope
Cycle1 = DamperHys.Cycles[1]

curvexy = Cycle1.xy



"""
We can also plot the cumulative area. This could be useful for finding 
the total energy added to a system
"""
# We plot the cumulative area under the graph
DamperHys.plotCumArea(xlim = [0,5], ylim = [0,1])

# The outputs from the plot object can be treated like any other matplotlib figure
fig, ax = DamperHys.plotCumArea(True)

# =============================================================================
# Test hysteresis, Ganey 2
# =============================================================================

# DamperHys = hys.Hysteresis(testHys2)

# DamperHys.plot(plotCycles = True, labelCycles = [17,18,19,23])
# DamperHys.plotCycles(plotCycles = True, labelCycles = [3,6,8])
# DamperHys.plotCycles([0,1])
# slope = DamperHys.Slope
# DamperHys.plotSlope()
# DamperHys.plotArea()

# Cycle = DamperHys.getCycle(20)
# Cycle.setSlope()

# Cycle.plotSlope()

# DamperHys.plotCycles([2,3])
# DamperHys.plotCycles([4,5])
# DamperHys.plotCycles([6,7])

# # DamperHys.plotCycle(1)

# xy = DamperHys.xy
# reversalIndexes = DamperHys.reversalIndexes
# Curve = DamperHys.getCycle(1)
# curvexy = Curve.xy
# # reversalIndexes

# A = DamperHys.getNetArea()
