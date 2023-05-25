# -*- coding: utf-8 -*-
"""
In this example, plots from section 3.1 of "Hysteresis - A Python Library 
for Analysing Structural Data" from WTCE 2023 are showcased.

An overview is given on how to compare an analysis and 
experimental hysteresis. This process is compeleted by sampling both curves
at regular intervals, and comparing the difference between them.

Data taken from Ryan Ganey's 2015 thesis:
https://digital.lib.washington.edu/researchworks/handle/1773/33664

Data for the analysis is taken from an opensees analysis of the wall.

"""

import numpy as np
import matplotlib.pyplot as plt
import hysteresis as hys

# =============================================================================
# Load initial stuff
# =============================================================================

"""
Once again, we load test data and make our hysteresis objects.
We'll also use the settings from the prior example to find revesal points in
the experimental data.
"""

Wall_exp = np.loadtxt('TS1_Experiment_Shear.csv', delimiter=',')
Wall_analysis_disp = np.loadtxt('Ts1_Load_Dsp.out', delimiter=' ')[1:, 1]
Wall_analysis_shear =np.loadtxt('Ts1_Wall_Reaction.out', delimiter=' ')[1:, 1]

Wall_exp_xy = np.column_stack([Wall_exp[:,0], Wall_exp[:,1]/1000])
Wall_anal_xy = np.column_stack([Wall_analysis_disp, -Wall_analysis_shear/1000])

ExpHys = hys.Hysteresis(Wall_exp_xy)
AnalHys = hys.Hysteresis(Wall_anal_xy)
ExpHys = hys.Hysteresis(Wall_exp_xy[8420:,:])


# =============================================================================
# Figures 10  
# =============================================================================

"""
Experimental Hysteresis
"""
fig, ax = plt.subplots(dpi = 150)
ExpHys.plot()
ax.set_xlabel('Deformation (m)')
ax.set_ylabel('Force (kN)')
plt.minorticks_on()
ax.grid(which='major', color='grey', linewidth=0.5, alpha = 0.8)
ax.grid(which='minor', linewidth=0.5, alpha = 0.4)
ax.legend(loc='lower right')

"""
Analysis Hysteresis
"""
fig, ax = plt.subplots(dpi = 150)
AnalHys.plot()
ax.set_xlabel('Deformation (m)')
ax.set_ylabel('Force (kN)')
plt.minorticks_on()
ax.grid(which='major', color='grey', linewidth=0.5, alpha = 0.8)
ax.grid(which='minor', linewidth=0.5, alpha = 0.4)
ax.legend(loc='lower right')

# =============================================================================
# Figure 11
# =============================================================================

"""
Show the initial failed attempt to find reversal points.
"""
fig, ax = plt.subplots(dpi = 150)
ExpHys.plotLoadProtocol()
ax.set_xlabel('Reversal point (#)')
ax.set_ylabel('Deformation (m)')
plt.minorticks_on()
ax.grid(which='major', color='grey', linewidth=0.5, alpha = 0.8)
ax.legend(loc='lower right')

"""
Show the fixed experiment
"""
ExpHys.recalculateCycles(revProminence = 0.0008)

fig, ax = plt.subplots(dpi = 150)
ExpHys.plotLoadProtocol()
ax.set_xlabel('Reversal point (#)')
ax.set_ylabel('Deformation (m)')
plt.minorticks_on()
ax.grid(which='major', color='grey', linewidth=0.5, alpha = 0.8)
ax.legend(loc='lower right')


# =============================================================================
# Figure 12 - This is a bad comparision, don't do this!
# =============================================================================

"""
A typical comparison where two plots are put on top of eachother.
"""

fig, ax = plt.subplots(dpi = 150)
ExpHys.plot(label='Experiment')
AnalHys.plot(label='Analysis')
ax.set_xlabel('Displacement (m)')
ax.set_ylabel('Force (kN)')
plt.minorticks_on()
ax.grid(which='major', color='grey', linewidth=0.5, alpha = 0.8)
ax.grid(which='minor', linewidth=0.5, alpha = 0.4)

# =============================================================================
# 13 Compare cycles directly  - This is a bad comparision, don't do this!
# =============================================================================
"""
We need to fix the analyis hysteresis first and make sure it's not skipping
any peaks
"""
AnalHys.recalculateCycles(revProminence = 0.01)


inds = [50,51]
fig, ax = plt.subplots(dpi = 150)
ExpHys.plotCycles(inds)
AnalHys.plotCycles(inds)
ax.set_xlabel('Cumulative Displacement (m)')
ax.set_ylabel('Energy (kJ)')
plt.minorticks_on()
ax.grid(which='major', color='grey', linewidth=0.5, alpha = 0.8)
ax.grid(which='minor', linewidth=0.5, alpha = 0.4)

ax.lines[0].set_label('Experiment')
ax.lines[2].set_color('C1')
ax.lines[2].set_label('Analysis')
ax.lines[3].set_color('C1')
ax.legend()


# =============================================================================
# Figure 14
# =============================================================================

"""
We can compare area under the graph for the experiment and analysis hysteresis.
"""

fig, ax = plt.subplots(dpi = 150)
ExpHys.plotCumArea(label='Experiment')
AnalHys.plotCumArea(label='Analysis')
ax.set_xlabel('Cumulative Displacement (m)')
ax.set_ylabel('Energy (kJ)')
plt.minorticks_on()
ax.grid(which='major', color='grey', linewidth=0.5, alpha = 0.8)
ax.grid(which='minor', linewidth=0.5, alpha = 0.4)


# =============================================================================
# Figure 15
# =============================================================================

AnalHys.recalculateCycles(revProminence = 0.01)
fig, ax = plt.subplots()

# not a plot in the paper but kind of fun.
AnalHys.plotLoadProtocol(comparisonProtocol = ExpHys.loadProtocol)

"""
The comparHys function can be used to guage how similar two hystereses are.
By default the function returns the average distance between each point on the
two curves. While the number alone may not be the most meaningful, it's 
magnitude will determine how similar different each cycle is. 

"""
NsamplesPerCurve = 10
AnalHysDx = hys.resample(AnalHys, NsamplesPerCurve)
ExpHysDx = hys.resample(ExpHys, NsamplesPerCurve)
ExpHysDx.recalculateCycles(revProminence = 0.005)

Diff, Diffs = hys.compareHys(AnalHysDx, ExpHysDx)


"""
We can plot the difference over each cycle, and view which cycles are the most
similar/different.

"""
fig, ax = plt.subplots(dpi=150)
plt.plot(Diffs)
ax.set_xlabel('Cycle (#)')
ax.set_ylabel('Avg. difference between Curves (unitless)')
plt.minorticks_on()
ax.grid(which='major', color='grey', linewidth=0.5, alpha = 0.8)
ax.grid( which='minor', linewidth=0.5, alpha = 0.4)
ax.set_ylim((0,20))

