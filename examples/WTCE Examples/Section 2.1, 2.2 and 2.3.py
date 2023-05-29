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

# Load the input data using numpy's loadtxt function.
name = 'SPC1'
data = np.loadtxt(name + '.csv', skiprows=2, delimiter = ',')

# Sort the data into a xy curve
x = data[:,1]
y = data[:,0]
xy = np.column_stack([x,y]) 

# Make a hysteresis object
myHys = hys.Hysteresis(xy)

# Plot the object to see if the cycles are detected properly.
# This data is really clean, good job Dr. Tannert!
# fig, ax = plt.subplots()
# myHys.plot(True)

# fig, ax = plt.subplots()
# myHys.plotVsIndex(True)

# =============================================================================
# Figure 1
# =============================================================================

finalCycle = myHys.cycles[-1]
finalCycle.plotVsIndex()

finalCycle.setPeaks(peakProminence=5)
finalCycle.setSubCycles()

# A plot that shows roughly monotonic regions
fig, ax = plt.subplots()
finalCycle.plotSubCycles(showPeaks=True, colorCycles=['C1', 'C0'])
plt.minorticks_on()
ax.grid(which='major', color='grey', linewidth=0.5, alpha = 0.8)
ax.grid(visible=True, which='minor', linewidth=0.5, alpha = 0.4)
ax.set_xlabel('Actuator Displacement (mm)')
ax.set_ylabel('Actuator Force (kN)')


# =============================================================================
# Figure 2 - Regions of the curve.
# =============================================================================
fig, ax = plt.subplots()
line1 = myHys.plot(linewidth = 0.7)

plt.minorticks_on()
ax.grid(which='major', color='grey', linewidth=0.5, alpha = 0.8)
ax.grid(visible=True, which='minor', linewidth=0.5, alpha = 0.4)
ax.set_xlabel('Actuator Displacement (mm)')
ax.set_ylabel('Actuator Force (kN)')

myHys.plotCycle(-3)
myHys.plotCycle(-2, color='C3')

# =============================================================================
# Figure 3 - A bunch of random plots showing features.
# =============================================================================

"""
Set some propreties of the curve.
"""
thirdLastCycle = myHys.cycles[-3]
thirdLastCycle.setArea()
thirdLastCycle.setLength()
thirdLastCycle.setSlope()

fig, ax = plt.subplots()
line1 = thirdLastCycle.plot(label='Base (kN)')

thirdLastCycle.plotArea(label='Area (kNmm)', linestyle = 'dashed')
thirdLastCycle.plotSlope(label='slope (kN/mm)', linestyle = 'dotted')
ax.grid(which='major', color='grey', linewidth=0.5, alpha = 0.8)
ax.grid(visible=True, which='minor', linewidth=0.5, alpha = 0.4)
ax.legend(loc='lower right')
ax.set_xlabel('Actuator Displacement (mm)')
ax.set_ylabel('Force units')
plt.minorticks_on()

# =============================================================================
# Figure 4 - Cumulative area undera curve and reversal points
# =============================================================================

"""
Set some propreties of the curve.
"""
fig, ax = plt.subplots()
myHys.plotCumArea(True)

plt.minorticks_on()
ax.grid(which='major', color='grey', linewidth=0.5, alpha = 0.8)
ax.grid(visible=True, which='minor', linewidth=0.5, alpha = 0.4)
ax.set_xlabel('Cumulative Actuator Displacement (mm)')
ax.set_ylabel('Area Under Curve (J)')

ax.legend(loc='lower right')


fig, ax = plt.subplots()
myHys.plotVsIndex(True)
plt.minorticks_on()
ax.grid(which='major', color='grey', linewidth=0.5, alpha = 0.8)
ax.grid(visible=True, which='minor', linewidth=0.5, alpha = 0.4)
ax.set_xlabel('index of data (#)')
ax.set_ylabel('Actuator Displacement (mm)')

ax.legend(loc='lower right')

# =============================================================================
# Figure 6 - resample a curve.
# =============================================================================
"""
Plot the base curve
"""
fig, ax = plt.subplots()
finalCycle.plot(c = 'C0', label='Base Curve')
plt.minorticks_on()
ax.grid(which='major', color='grey', linewidth=0.5, alpha = 0.8)
ax.grid(visible=True, which='minor', linewidth=0.5, alpha = 0.4)
ax.set_xlabel('Actuator Displacement (mm)')
ax.set_ylabel('Actuator Force (kN)')

"""
Get the resample curve and add it to the plot
"""
resampled = hys.resample(finalCycle, 5)
resampled.plot(linestyle='dashed', c='black', label='Resampled Curve')
plt.minorticks_on()
ax.grid(which='major', color='grey', linewidth=0.5, alpha = 0.8)
ax.grid(visible=True, which='minor', linewidth=0.5, alpha = 0.4)
ax.set_xlabel('Actuator Displacement (mm)')
ax.set_ylabel('Actuator Force (kN)')

ax.legend(loc='lower right')

# =============================================================================
# Figure 7
# =============================================================================
"""
A visual example for what we what is meant by the difference between curves
"""

trial = -6
Nsample = 10
curve1 = -myHys.cycles[trial]
curve2 = -myHys.cycles[trial +2]

output = hys.compareCycle(curve1, curve2, Nsample)
roundOut = round(output*10)/10


c1Resampled = hys.resample(curve1, 10)
c2Resampled = hys.resample(curve2, 10)
x = [c1Resampled.xy[:,0], c2Resampled.xy[:,0]]
y = [c1Resampled.xy[:,1], c2Resampled.xy[:,1]]

fig, ax = plt.subplots(dpi=300)
curve1.plot(label='Cycle 1', linestyle = 'dashed')
curve2.plot(label='Cycle 2', linestyle = 'dotted')
ax.plot(x, y, c = 'C2')
ax.plot(x, y, 'x',c = 'C3')
ax.grid(which='major', color='grey', linewidth=0.5, alpha = 0.8)
ax.grid(visible=True, which='minor', linewidth=0.5, alpha = 0.4)
# ax.legend(loc='lower right')
ax.set_xlabel('Actuator Displacement (mm)')
ax.set_ylabel('Actuator Force (kN)')
plt.minorticks_on()
ax.legend()
ax.text(-38.5,-27.3,f'The average difference is: {roundOut}', backgroundcolor='white')
hys.envelope
