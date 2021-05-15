# -*- coding: utf-8 -*-
"""
Many of the Hysteresis default functions can be overwritten by assigning
a new function to the environment object, located at 
hys.env.environment 

In this example, this feature is showcased by implementing a custom slope 
function.


"""
import hysteresis as hys
import numpy as np

# =============================================================================
# Input Data
# =============================================================================
# We create a set of input xy data using numpy, create a hysteresis, then
# plot a figure of our object.

x = np.linspace(0,3,301)
y = x**3 + x**2 + 2
xy = np.column_stack((x,y))
myHys = hys.Hysteresis(xy)

fig, ax = myHys.initFig()
myHys.plot()
myHys.plotSlope()
ax.set_title('Default slope Function')

# =============================================================================
# Define a custom function
# =============================================================================


# define a custom slope function - it makes the slope always 1. 
def fslope(xy):
    slope = np.ones_like(xy[:,0])
    return slope 

# Overwrite the slope function in the environment.
hys.env.environment.fslope = fslope

# Plot to show it's worked
myHys = hys.Hysteresis(xy)
fig, ax = myHys.initFig()
myHys.plot()
myHys.plotSlope()


# If we want the behaviour to return to normal, restart the environment.
hys.env.environment.restart()

