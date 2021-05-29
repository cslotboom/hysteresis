# -*- coding: utf-8 -*-
"""
In this example, an overview is given on how to compare an analysis and 
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
ExpHys.recalculateCycles(revProminence = 0.0008)

"""
To compare each hysteresis, they need to have the same number of cycles.

Recall that the experimental data is missing cycles. Therefore we will filter
out the initial cycles in the analysis hysteresis.

We can confirm that each analysis has a different load protcol by plotting both
"""


fig, ax = plt.subplots()
AnalHys.plotLoadProtocol()
ExpHys.plotLoadProtocol()

"""
This analysis data is very clean, and doesn't need much manual adjustment. 
We will once again recalcualte the reversal points, setting the reversal
prominence variable.

Note that the experimental dispalcement doesn't exactly match the analysis or 
expected load protocol. This behaviour can occur if the testing aparatus is 
flexible, or the actuator is not precise enough.

"""

AnalHys.recalculateCycles(revProminence = 0.01)
fig, ax = plt.subplots()
AnalHys.plotLoadProtocol(comparisonProtocol = ExpHys.loadProtocol)




"""
Now that each hysteresis has the same number of cycles, it's possible to
compare how "similar" each cycle is.

We will first shift each curve into a similar domain/range using the resample
functon. This will take each curve in the hystersis, and use linear 
interpolation to define 10 evenly spaced points along that curve.

"""
NsamplesPerCurve = 10
AnalHysDx = hys.resample(AnalHys, NsamplesPerCurve)
ExpHysDx = hys.resample(ExpHys, NsamplesPerCurve)

fig, ax = plt.subplots()
line1 = AnalHysDx.plot(True)
line2 = ExpHysDx.plot(True)
ax.lines[2].set_color('C3')
ax.lines[3].set_color('C2')
ax.set_xlabel('Drift (%)')
ax.set_ylabel('Force (kN)')
plt.minorticks_on()
ax.grid(which='major', color='grey', linewidth=0.5, alpha = 0.8)
ax.grid(b=True, which='minor', linewidth=0.5, alpha = 0.4)


plt.show()

"""
The comparHys function can be used to guage how similar two hystereses are.
By default the function returns the average distance between each point on the
two curves. While the number alone may not be the most meaningful, it's 
magnitude will determine how similar different each cycle is. 

"""
Diff, Diffs = hys.compareHys(AnalHysDx, ExpHysDx)


"""
We can plot the difference over each cycle, and view which cycles are the most
similar/different.

"""
fig, ax = plt.subplots()
plt.plot(Diffs)
ax.set_xlabel('Cycle (#)')
ax.set_ylabel('Avg. difference between Curves (unitless)')
plt.minorticks_on()
ax.grid(which='major', color='grey', linewidth=0.5, alpha = 0.8)
ax.grid(b=True, which='minor', linewidth=0.5, alpha = 0.4)


