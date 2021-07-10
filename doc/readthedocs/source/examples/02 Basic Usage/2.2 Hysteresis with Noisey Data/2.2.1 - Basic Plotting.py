# -*- coding: utf-8 -*-
"""
In this example I will show some of the basic functionality of the hysteresis
module on a real hysteresis.

Data taken from Ryan Ganey's 2015 thesis:
https://digital.lib.washington.edu/researchworks/handle/1773/33664

"""

import numpy as np
import matplotlib.pyplot as plt
import hysteresis as hys


# =============================================================================
# Load initial stuff
# =============================================================================

"""
Here we load some test data.
"""

Wall_exp = np.loadtxt('TS1_Experiment_Shear.csv', delimiter=',')
Wall_analysis_disp = np.loadtxt('Ts1_Load_Dsp.out', delimiter=' ')[1:, 1]
Wall_analysis_shear =np.loadtxt('Ts1_Wall_Reaction.out', delimiter=' ')[1:, 1]

Wall_exp_xy = np.column_stack([Wall_exp[:,0], Wall_exp[:,1]/1000])
Wall_anal_xy = np.column_stack([Wall_analysis_disp, -Wall_analysis_shear/1000])


"""
We'll manually input a trace of the load protocol that was input the the actuator.
Values are converted to % drift, but units don't really matter.
"""

loadProtocol = np.array([0.035 ,0.05, 0.075 ,0.1, 0.15, 0.2, 0.3, 0.4, 0.6, 
                       0.9   ,1.35, 2.0,   3.0, 4.0])*4.1/100


# =============================================================================
# Plot both Hystereses
# =============================================================================


"""
Here we make hysteresis objects of our experimental and analysis load protcol.
"""
ExpHys = hys.Hysteresis(Wall_exp_xy)
AnalHys = hys.Hysteresis(Wall_anal_xy)

"""
We can find out out how many cycles the initial hysteresis has!
The Hysteresis object stores a bunch of useful information
"""
print(ExpHys.NCycles)


"""
We can also have a bunch of conveneint ways of viewing our data.
We can use the "plot" command to make a figure of our data.
All plotting uses matplotlib, and is compatible with matplotlib commands
In fact our plot can returns a matplotlib line object of the data!

"""
fig, ax = plt.subplots()
line = ExpHys.plot()


"""
We make a nice plot of each curve on the same graph.
"""
fig, ax = plt.subplots()
ExpHys.plot()
AnalHys.plot()
ax.set_xlabel('Actuator Drift (m)')
ax.set_ylabel('Actuator Force (kN)')
plt.minorticks_on()
ax.grid(which='major', color='grey', linewidth=0.5, alpha = 0.8)
ax.grid(b=True, which='minor', linewidth=0.5, alpha = 0.4)


"""
Here we plot some only some of our cycles for fun, we can pull out specific items
"""

fig, ax = plt.subplots()
AnalHys.plotCycles([20,21,22,30,50,60])


"""
We can also plot the energy contained in the hysteresis, using the cumulative
area plot funciton.
If cycles are set, they can be overlayed on the figure.
"""

fig, ax = ExpHys.initFig()
ExpHys.plot()

fig, ax = ExpHys.initFig()
ExpHys.plotCumArea()
ax.set_xlabel('Cumulative Drift (m)')
ax.set_ylabel('Energy (kNm)')
plt.minorticks_on()
ax.grid(which='major', color='grey', linewidth=0.5, alpha = 0.8)
ax.grid(b=True, which='minor', linewidth=0.5, alpha = 0.4)


