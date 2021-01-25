# -*- coding: utf-8 -*-

"""
In this example I will show some of the basic functionality of the hystresis
module on a real hystresis.

"""
import numpy as np
import hysteresis as hys
import matplotlib.pyplot as plt

# =============================================================================
# Load initial stuff
# =============================================================================

"""
Here we load some test data.
"""

inputxy = np.loadtxt('BackboneData.csv',delimiter=',')
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

DamperHys = hys.Hysteresis(inputxy)
xy = DamperHys.xy


"""
We can then show some of the outputs. Lets use some of the basic plotting 
features to visualize our data. Here we use the plot command to create a plot
of our data. The plot command is similar to matplotlib's plot comand - it
doesn't make a figure
"""

DamperHys.plot()

"""
All outputs are matplotlib plots, so we can make changes after the plotting.
Let's add some labels to our chart!
"""

fig, ax = DamperHys.initFig()
DamperHys.plot(plotCycles=True)
# DamperHys.plot()

ax.set_xlabel('Actuator Displacement (mm)')
ax.set_ylabel('Applied Force (kN)')
ax.set_xlim(-3.5,3.5)
ax.set_ylim(-6,6)
plt.minorticks_on()
ax.grid(which='major', color='grey', linewidth=0.5, alpha = 0.8)
ax.grid(b=True, which='minor', linewidth=0.5, alpha = 0.4)


""" 
By defualt, hysteresis objects will try to find revesal points in our data, and 
break the curve up into a number of cycles. We can access and plot these cycles.

The data we are working with is quite smooth, and the default settings did a 
good job of finding reversal points! You might have to play around with the 
input settings.
"""
reversalIndexes = DamperHys.reversalIndexes
fig, ax = DamperHys.initFig()
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
the total energy added to a system.

"""
fig, ax = DamperHys.initFig()
# DamperHys.plotCumArea()
DamperHys.plotCumArea(True, labelCycles = [0, 5, 10, 15, 20])
# fig, ax = DamperHys.plotArea(True, labelCycles = [0, 5, 10, 15, 20])


ax.set_xlabel('Cumulative Deformation (mm)')
ax.set_ylabel('Energy (kNm)')
plt.minorticks_on()
ax.grid(which='major', color='grey', linewidth=0.5, alpha = 0.8)
ax.grid(b=True, which='minor', linewidth=0.5, alpha = 0.4)

# DamperHys.plot(True, labelCycles = 'all')

# =============================================================================
# Test hysteresis, Ganey 2
# =============================================================================

DamperHys = hys.Hysteresis(testHys2)
fig, ax = DamperHys.initFig()
DamperHys.plot(plotCycles = True, labelCycles = [17,18,19,23])
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
