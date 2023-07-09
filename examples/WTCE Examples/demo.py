# -*- coding: utf-8 -*-
"""
@author: Christian

In this example, plots from section 2.1,2.2, and 2.3 of 
"Hysteresis - A Python Library for Analysing Structural Data" from 
WTCE 2023 are showcased.

Curves in the hysteresis module are compatible with basic operations, i.e.
addition, subtraction, multiplication, and 


"""

import numpy as np
import matplotlib.pyplot as plt
import hysteresis as hys

# dark style baby.
plt.style.use('dark_background')

# Load the input data using numpy's loadtxt function.
name = 'SPC1'
data = np.loadtxt(name + '.csv', skiprows=2, delimiter = ',')

# Sort the data into a xy curve
x = data[:,1]
y = data[:,0]
xy = np.column_stack([x,y]) 

# Make a hysteresis object
myHys = hys.Hysteresis(xy)

backgroundColor = '#19232D'
# =============================================================================
# Extract data we want.
# =============================================================================

# get the filan cycle
finalCycle = myHys.cycles[-1]
finalCycle.setPeaks(peakProminence=5)
finalCycle.setSubCycles()


Cycle1 = myHys.cycles[-1]
Cycle2 = myHys.cycles[-2]
Cycle3 = myHys.cycles[-3]

# =============================================================================
# Title Image
# =============================================================================
fig, ax = plt.subplots()
myHys.plot(c='white')
Cycle2.plot(c='C3',linewidth=3)
Cycle3.plot(c='C3',linewidth=3)
ax.set_facecolor(backgroundColor)
ax.axis('off')
ax.add_artist(ax.patch)

# =============================================================================
# Figure 1
# =============================================================================

# A plot that shows roughly monotonic regions
fig, ax = plt.subplots()
myHys.plot()
ax.set_facecolor(backgroundColor)
ax.axis('off')
ax.add_artist(ax.patch)


# A plot that shows roughly monotonic regions
fig, ax = plt.subplots()
myHys.plot(showReversals=True)
# ax.axis('off')



# =============================================================================
# Figure 1
# =============================================================================


# A plot that shows roughly monotonic regions
fig, ax = plt.subplots()
ax.set_facecolor(backgroundColor)

Cycle1.plot()
Cycle2.plot(c='C0')
Cycle3.plot(c='C0')
ax.axis('off')
ax.add_artist(ax.patch)

# ax.axis('off')



# =============================================================================
# Figure 2
# =============================================================================

# get the filan cycle
Cycle1 = myHys.cycles[-1]
Cycle2 = myHys.cycles[-2]
Cycle3 = myHys.cycles[-3]

Cycle1.setPeaks(1000,peakProminence=12)
Cycle2.setPeaks(1000,peakProminence=12)
Cycle3.setPeaks(1000,peakProminence=12)

# A plot that shows roughly monotonic regions
fig, ax = plt.subplots()
ax.set_facecolor(backgroundColor)
Cycle3.plot()
Cycle2.plot()
Cycle1.plot()
ax.axis('off')
ax.add_artist(ax.patch)


# =============================================================================
# Figure 2
# =============================================================================

# get the filan cycle
finalCycle = myHys.cycles[-1]
finalCycle.setPeaks(peakProminence=5)
finalCycle.setSubCycles()

Cycle1 = myHys.cycles[-1]
Cycle2 = myHys.cycles[-2]
Cycle3 = myHys.cycles[-3]

# A plot that shows roughly monotonic regions
fig, ax = plt.subplots()
Cycle3.plot()
Cycle2.plot()
finalCycle.plotSubCycles(colorCycles=['C2', 'C3'])

ax.set_facecolor(backgroundColor)
ax.axis('off')
ax.add_artist(ax.patch)


# =============================================================================
# 
# =============================================================================

# finalCycle.plotSubCycles(showPeaks=True, colorCycles=['C1', 'C0'])
# plt.minorticks_on()
# ax.grid(which='major', color='grey', linewidth=0.5, alpha = 0.8)
# ax.grid(visible=True, which='minor', linewidth=0.5, alpha = 0.4)
# ax.set_xlabel('Actuator Displacement (mm)')
# ax.set_ylabel('Actuator Force (kN)')


# =============================================================================
# Figure 2 - Regions of the curve.
# =============================================================================
# fig, ax = plt.subplots()
# line1 = myHys.plot(linewidth = 0.7)

# plt.minorticks_on()
# ax.grid(which='major', color='grey', linewidth=0.5, alpha = 0.8)
# ax.grid(visible=True, which='minor', linewidth=0.5, alpha = 0.4)
# ax.set_xlabel('Actuator Displacement (mm)')
# ax.set_ylabel('Actuator Force (kN)')

# myHys.plotCycle(-3)
# myHys.plotCycle(-2, color='C3')
