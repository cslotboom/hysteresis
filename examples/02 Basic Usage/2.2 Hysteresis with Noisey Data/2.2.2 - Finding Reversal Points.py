# -*- coding: utf-8 -*-
"""
While Hysteresis can find cycles reversal points, experimental data is often
very messy. Revesal points are found.

Luckily, there are a host of tools that can help us filter out these bad data
points. In this example, an overview is given on how to clean up the data in a 
hysteresis and find the correct cycle end points.


Data taken from Ryan Ganey's 2015 thesis:
https://digital.lib.washington.edu/researchworks/handle/1773/33664

Data for the analysis is taken from an opensees analysis of the wall.

"""

import numpy as np
import matplotlib.pyplot as plt
import hysteresis as hys
from hysteresis.protocol import createProtocol


# =============================================================================
# Load initial stuff
# =============================================================================

"""
Here we load the test data again.

"""

Wall_exp = np.loadtxt('TS1_Experiment_Shear.csv', delimiter=',')
Wall_analysis_disp = np.loadtxt('Ts1_Load_Dsp.out', delimiter=' ')[1:, 1]
Wall_analysis_shear =np.loadtxt('Ts1_Wall_Reaction.out', delimiter=' ')[1:, 1]

Wall_exp_xy = np.column_stack([Wall_exp[:,0], Wall_exp[:,1]/1000])
Wall_anal_xy = np.column_stack([Wall_analysis_disp, -Wall_analysis_shear/1000])



"""

To find the correct cycles points, it is often useful to know the input load
protocol for our data. First we manually enter the absolute values of our load 
protocol. 

We'll manually input a trace of the load protocol that was input the the 
actuator. Values are converted to % drift, but units don't really matter.

Given the trance of a load protcol, we can expand that into a full 
load protocol that has both positive and negative points, and the correct 
number of cycles.

In this experimetn there were three repeats for each step in the load protocol.
Therefore, we would have a total of Nx3x2 cycles

"""


loadProtocolTrace = np.array([0.035 ,0.05, 0.075 ,0.1, 0.15, 0.2, 0.3, 0.4, 0.6, 
                        0.9   ,1.35, 2.0,   3.0, 4.0])*4.1/100

Ncycles = len(loadProtocolTrace)*3*2

Indexes = np.ones_like(loadProtocolTrace, dtype=int) * 3
loadProtocol = createProtocol(loadProtocolTrace, Indexes)


"""
Here we make hysteresis objects of our experimental and analysis load protcol.
When create the Hysteresis object, it will attempt to find the reversal points.
"""
ExpHys = hys.Hysteresis(Wall_exp_xy)
AnalHys = hys.Hysteresis(Wall_anal_xy)


"""
Let's see how well our the initial guess did. We'll print the number of cycles,
as well as make a plot that has the cycle locations

"""
print(ExpHys.NCycles)
fig, ax = plt.subplots()
ExpHys.plot(True)


"""
Wow, there are way too many cycles early on!
It's hard to get a sense of what's wrong from our initial plot.
Let's make a new plot of the values vs. the index of each point to see what's
going on. We will turn on the plot cycles option to see where out cycles are.
We'll can also use the "plotLoadProtocol()" plot, to see the hysteresis' 
load protocol.
"""

fig, ax = ExpHys.initFig()
ExpHys.plotVsIndex(True)

fig, ax = ExpHys.initFig()
ExpHys.plotLoadProtocol()

"""
It looks like we are picking up a whole bunch of noise in our data.
In fact, in this particular set of data, the intial dispacement is so small it 
hasn't been recorded very well. The initial cycles are completely masked by 
noise

We have a few options to remove this. The  one thing we may try is to 
just to remove the extranious points. After some trial and error, we try 
removing the first 8420 data points. 
The number 8420 may seem oddly specific - this is about the  earliest where
peaks are distnguishable from noise.

"""

ExpHys = hys.Hysteresis(Wall_exp_xy[8400:,:])
fig, ax = ExpHys.initFig(xlims=[-1,50], ylims=[-0.05, 0.05])
ExpHys.plotVsIndex(True)


ExpHys = hys.Hysteresis(Wall_exp_xy[8420:,:])


"""
Let's make a new figure and plot the results again.
This time we'll use the "plotLoadProtocol()" option, to see how our protocol
is doing. This is a plot of the peak x values for each cycle.

"""

fig, ax = ExpHys.initFig()
ExpHys.plotLoadProtocol()
print(ExpHys.NCycles)


"""
Better, but there are still more cycles than we'd like. 
Lets filter out any peak that has a height less than a target input by
setting the revProminence parameter. This removes reverasals that aren't of a 
certain height compared to the surrounding peaks.

We will remove all reversals with prominence less than half the first value in
our load protocol. 

"""

ExpHys.recalculateCycles(revProminence = loadProtocol[1]/2)
fig, ax = ExpHys.initFig()
ExpHys.plotLoadProtocol(comparisonProtocol = loadProtocol)

fig, ax = ExpHys.initFig([-1,50], [-0.05, 0.05])
ExpHys.plotVsIndex(True)

"""
We're doing pretty good, but we can see that we've lost some data - the early
cycles should have more peaks. We'll make a note of this, but due to the poor
quality of data there isn't much we can do to "find" these peaks. They just
aren't recorded in the input data!

Moving forward, we will remake our input load protol and compare it with the 
experimental data.

"""
loadProtocolTrace = np.array([0.15, 0.2, 0.3, 0.4, 0.6, 
                        0.9   ,1.35, 2.0,   3.0, 4.0])*4.1/100

Indexes = np.ones_like(loadProtocolTrace, dtype=int) * 3
loadProtocol = createProtocol(loadProtocolTrace, Indexes)

fig, ax = ExpHys.initFig()
ExpHys.plotLoadProtocol(comparisonProtocol = loadProtocol)

fig, ax = ExpHys.initFig()
ExpHys.plotVsIndex(True)

"""
This looks pretty good! Comparing to the input load protocol, we see that the 
peak x values are in the correct place.

We can return our reversal indexes and store them for later use.

"""

xyRev = ExpHys.getReversalxy()


