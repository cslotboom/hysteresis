# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 23:47:36 2020

@author: Christian
"""
import hysteresis as hys
import numpy as np

# Some random T/dT data
data =  np.array([[-0.724, -0.834], [-0.680, -1.239], [-0.479, -1.032],
                  [-0.488, -0.871], [-0.526, -0.774], [-0.331, -0.741], 
                  [-0.008, -0.596], [0.060, -0.430],  [0.204, -0.256],
                  [0.289, 0.024],   [0.369, 0.234],   [0.554, 0.655],
                  [0.545, 0.724],   [0.635, 0.857],   [0.564, 0.868],
                  [0.368, 0.858],   [0.385, 0.725],   [0.349, 0.636],
                  [0.181, 0.496],   [0.042, 0.399],   [-0.204, 0.120],
                  [-0.380, 0.002],  [-0.429, -0.131], [-0.655, -0.421]])


# np.random.shuffle(data)


# Make the seasonal Hysteresis data
climateHys = hys.SeasonalCurve(data, 12, n = 1, m = 1)

# Plot the scatter and fitter curve
fig, ax = climateHys.initFig()
climateHys.plotScatter()
climateHys.plotFittedCurve()

# Plot the temperature data
fig, ax = climateHys.initFig()
climateHys.plotTemp()
climateHys.plotDTemp()

# get some coeficients
Tcoefs = climateHys.tempCoef
dTcoefs = climateHys.dTempCoef

# Prints some info
climateHys.printT()
print()
climateHys.printDT()

