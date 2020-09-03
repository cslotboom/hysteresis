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

# =============================================================================
# Load initial stuff
# =============================================================================


basePoints = np.linspace(0,10,1000)
testx = np.sin(basePoints)
testy = testx *1.2**-basePoints
testxy = np.column_stack((testx, testy))

t1 = time.time()
testHys = np.loadtxt('BackboneData.csv',delimiter=',')
disp = np.loadtxt('Disp.out',delimiter=' ')
force = np.loadtxt('RFrc.out',delimiter=' ')

Wall_exp = np.loadtxt('TS1_Experiment_Shear.csv',delimiter=',')
Wall_analysis_disp = np.loadtxt('Ts1_Load_Dsp.out',delimiter=' ')[1:,1]
Wall_analysis_shear =np.loadtxt('Ts1_Wall_Reaction.out',delimiter=' ')[1:,1]

t2 = time.time()

print(t2-t1)
testHys2 = np.column_stack([disp[:,1], -force[:,1]])

Wall_exp_xy = np.column_stack([Wall_exp[:,0], Wall_exp[:,1]/1000])
Wall_anal_xy = np.column_stack([Wall_analysis_disp, -Wall_analysis_shear/1000])







# =============================================================================
# Circle Area test - Tested
# =============================================================================

"""
Tests a basic Circle to see if some propreties are correct
"""

# basePoints = np.linspace(0,1,1000)*2*np.pi
# testCirclex = np.sin(basePoints)
# testCircley = np.cos(basePoints)
# Circlexy = np.column_stack((testCirclex, testCircley))

# Circle = hys.Hysteresis(Circlexy)

# Circle.plot(plotCycles=True)
# Circle.plotSlope(plotCycles=True, ylim = [-10,10])
# fig, ax = Circle.plotCycles()
# NetArea = Circle.getNetArea()
# print(NetArea)

# print(Circle.loadProtocol)
# Vector1 = Circle.subvectors[0]




# =============================================================================
# Tested Curve Base Tests, Area and Slope Functions - Tested
# =============================================================================

"""
Gets the area under a series of graphs
"""



# xdata = np.linspace(0,4,1001)
# y1 = xdata + 2
# y2 = xdata**3 - 3*xdata**2 + 3
# y3 = 3 + (np.e)**xdata

# xy1 = np.column_stack([xdata, y1])
# xy2 = np.column_stack([xdata, y2])
# xy3 = np.column_stack([xdata, y3])

# Curve1 = hys.CurveBase(xy1)
# Curve2 = hys.CurveBase(xy2)
# Curve3 = hys.CurveBase(xy3)

# Curves = [Curve1, Curve2, Curve3]

# for curve in Curves:
#     curve.setArea()
#     curve.setSlope
#     print()

# A1 = Curve1.getNetArea()
# A2 = Curve2.getNetArea()
# A3 = Curve3.getNetArea()



# =============================================================================
# Circle Plotting test - Tested
# =============================================================================

"""
This tests a Circle hysteresis can be plotted and if the resampled curves can be plotted.
"""

# basePoints = np.linspace(0,1,1000)*2*np.pi
# testCirclex = np.cos(basePoints)
# testCircley = np.sin(basePoints)
# Circlexy = np.column_stack((testCirclex, testCircley))

# Circle = hys.Hysteresis(Circlexy)

# Circle.plot(plotCycles=True)
# Circle.plotArea(plotCycles=True)
# Circle.plotSlope(plotCycles=True, ylim = [-10,10])
# Circle.setPeaks()
# fig, ax = Circle.plotCycles(plotCycles=True, plotPeaks=True)
# # fig, ax = Circle.plotSubVector(0)

# Vector1 = Circle.Cycles[0]
# Vector2 = hys.reSample(Vector1, 30)
# Vector3 = hys.reSample(Circle, 10)

# Vector1.plot()
# Vector2.plot()
# Vector3.plot(True)


# =============================================================================
# Test Hysteresis, Ganey UFP
# =============================================================================

# DamperHys = hys.Hysteresis(testHys)

# # Plots
# DamperHys.plot(plotCycles = True)
# DamperHys.plotCycles(plotCycles = True)
# DamperHys.plotCycles([0,1], True)
# DamperHys.plotCycles([2,3])
# DamperHys.plotCycles([4,5])
# DamperHys.plotCycles([6,7])

# # DamperHys.plotCycle(1)


# xy = DamperHys.xy
# Area = DamperHys.Area
# reversalIndexes = DamperHys.reversalIndexes
# Curve = DamperHys.getCycle(1)
# curvexy = Curve.xy

# # Cumulative area reversalIndexes
# DamperHys.plotCumArea(xlim = [0,5], ylim = [0,1])
# DamperHys.plotCumArea(True)
# A = DamperHys.getNetArea()

# =============================================================================
# Test Hysteresis, Ganey 2 - Tested
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





# =============================================================================
# Resample Hys Example - Tested
# =============================================================================


# DamperHys = hys.Hysteresis(testHys2)

# # Resample hysteresis
# downsampledHys = hys.reSample(DamperHys, 20)
# downsampledHys.plot(plotCycles = True)
# downsampledHys.plotCycles([2,3])
# downsampledHys.plotArea()



# =============================================================================
# Resampledx Hys Example
# =============================================================================

# DamperHys = hys.Hysteresis(testHys2)
# cycles = DamperHys.Cycles
# output = hys.concatenateHys(*cycles)
# T1 = DamperHys.xy
# T2 = output.xy

# # Resample Hys
# downsampledHys = hys.reSampledx(DamperHys, 0.01)
# downsampledHys.plot(plotCycles = True)
# xy = downsampledHys.xy


# # Resample Cycle
# Cycle = DamperHys.Cycles[0]
# resampleCycle = hys.reSampledx(Cycle, 0.00001)
# resampleCycle.plot()

# # Resample SubCycle
# Cycle.setPeaks()
# Cycle.setSubCycles()
# subcycle = Cycle.SubCycles[0]
# resampleSubCycle = hys.reSampledx(subcycle, 0.00001)
# resampleSubCycle.plot()

# # Resample np.Array
# resampleNP = hys.reSampledx(resampleSubCycle.xy, 0.0001)


# downsampledHys.plotCycles([2,3])
# downsampledHys.plotArea()




# =============================================================================
# Triangle Example Small - Tested
# =============================================================================

# x = np.linspace(0, 1, 1000)*10

# # a triangle with small reversals
# triangleSmall = scipy.signal.sawtooth(x*20,0.5)/7
# trianglexy = np.column_stack((x,triangleSmall))


# smallTriangles = hys.SimpleCycle(trianglexy, FindPeaks = True)
# smallTriangles.setPeaks()
# smallTriangles.plot(plotPeaks = True)
# smallTriangles.plotSubCycles()

# subCycle = smallTriangles.getSubCycle(1)
# smallTriangles.setSlope()
# smallTriangles.plotSlope()

# =============================================================================
# Triangle Example Combined - Tested
# =============================================================================


# # a triangle with small reversals
# x = np.linspace(0, 1, 1000)*10
# triangleBig = scipy.signal.sawtooth(x*2,0.5)
# triangleSmall = scipy.signal.sawtooth(x*20,0.5)/7
# triangle = triangleBig + triangleSmall
# trianglexy = np.column_stack((x,triangle))

# # Standard plot
# notchedTriangles = hys.SimpleCycle(trianglexy, FindPeaks = True)
# notchedTriangles.setPeaks()
# peaks = notchedTriangles.peakIndexes
# notchedTriangles.plot(plotPeaks = True)
# notchedTriangles.plotSubCycles()

# notchedTriangles.setSlope()
# slope = notchedTriangles.Slope
# notchedTriangles.plotSlope()

# notchedTriangles.setArea()
# Area = notchedTriangles.getNetArea()



# # fine absolute peaks
# notchedTriangles = hys.SimpleCycle(trianglexy, FindPeaks = True)
# notchedTriangles.recalculatePeaks(peakProminence = 0.8)
# peaks2 = notchedTriangles.peakIndexes
# notchedTriangles.plot(plotPeaks = True)




# slope = smallTriangles.Slope
# area = smallTriangles.Slope
# plt.plot(slope)




# =============================================================================
# Triangle Example Combined - Noise - Tested
# =============================================================================
# np.random.seed(101)

# # a noisey triangle signal
# x = np.linspace(0, 1, 1000)*10
# triangleBig = scipy.signal.sawtooth(x*2,0.5)
# permutate = np.random.normal(0,1,1000)/2
# Ynoise = triangleBig + permutate
# Ynoise = scipy.signal.savgol_filter(Ynoise,53,2)

# trianglexy = np.column_stack((x, Ynoise))

# noiseyTriangles = hys.SimpleCycle(trianglexy, FindPeaks = True)
# peak1 = noiseyTriangles.peakIndexes
# noiseyTriangles.recalculatePeaks(peakWidth = 100)
# peak2 = noiseyTriangles.peakIndexes
# noiseyTriangles.plot(plotPeaks = True)


# smallTriangles.plotSubCycles()

# subCycle = smallTriangles.getSubCycle(1)
# smallTriangles.setSlope()
# smallTriangles.plotSlope()
# slope = smallTriangles.Slope
# area = noiseyTriangles.getNetArea()
# plt.plot(slope)


# t2 = time.time()
# # print(t2-t1)


# =============================================================================
# SubCycle Test
# =============================================================================

x = np.linspace(0, 1, 1000)*10
triangleSmall = scipy.signal.sawtooth(x*20,0.5)/7
trianglexy = np.column_stack((x,triangleSmall))

smallTriangles = hys.SimpleCycle(trianglexy, FindPeaks = True, setSlope=True)
smallTriangles.plotSlope()
smallTriangles.plot(plotPeaks=True)


subCycle = smallTriangles.getSubCycle(1)
subCycle.setSlope()
fig, ax = subCycle.plotSlope()
subCycle.setArea()
subCycle.Area



# =============================================================================
# Resample Tests
# =============================================================================

# np.random.seed(103)

# x = np.linspace(0, 1, 1000)*10

# # a triangle with small reversals
# triangleBig = scipy.signal.sawtooth(x*2,0.5)

# # a noisey triangle signla
# permutate = np.random.normal(0,1,1000)/2
# Ynoise = triangleBig + permutate
# Ynoise = scipy.signal.savgol_filter(Ynoise,53,2)

# xy = np.column_stack([x,Ynoise])

# TestHys = hys.monotonicCycle(xy)

# TestHys = hys.monotonicCycle(xy, FindPeaks = True)
# TestHys.plot(Peaks=True)

# TestHys.recalculatePeaks(peakWidth = 50, peakDist = 10)
# TestHys.plot(Peaks=True)




# =============================================================================
# Area tests
# =============================================================================

# # Curve1 = hysteresis.monotonicCycle(testxy)
# Curve1 = hysteresis.Hysteresis(testxy)
# Curve2 = hysteresis.Hysteresis(testHys)


# fig, ax = Curve1.plot(Cycles=True)


# Curve1.xy


# Curve1.reversalIndexes

# subVectors = Curve1.subvectors

# fig, ax = plt.subplots()
# for ii in range(len(subVectors)):
#     plt.plot(subVectors[ii].xy[:,0], subVectors[ii].xy[:,1])
#     # plt.plot(subVectors[ii][150:,0], subVectors[ii][150:,1])

# area1 = trapz(subVectors[0].xy[:,1], subVectors[0].xy[:,0])
# area2 = trapz(subVectors[1].xy[:,1], subVectors[1].xy[:,0])
# area3 = trapz(subVectors[2].xy[:,1], subVectors[2].xy[:,0])

# area = 0
# for ii in range(len(subVectors)):
#     area += trapz(subVectors[ii].xy[:,1], subVectors[ii].xy[:,0])
    
    
    
# Curve1.plotSubVector(1)





# =============================================================================
# # Slope function test
# =============================================================================

# domain = np.linspace(0,1,101)*np.pi
# sin = np.sin(domain)
# cos = np.cos(domain)
# xy = np.column_stack([domain, sin])

# xyp = xy[2:, :]
# xyn = xy[:-2, :]

# slopeMid = ( (xyp[:,1] - xyn[:,1]) / (xyp[:,0] - xyn[:,0]))
# slopeStart = (xy[1,1] - xy[0,1]) / (xy[1,0] - xy[0,0])
# slopeEnd = (xy[-1,1] - xy[-2,1]) / (xy[-1,0] - xy[-2,0])

# Slope = np.concatenate([[slopeStart], slopeMid, [slopeEnd]])



