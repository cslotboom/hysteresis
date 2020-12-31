# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 23:47:36 2020

@author: Christian
"""
import hysteresis as hys
import numpy as np
import matplotlib.pyplot as plt
        
Wall_exp = np.loadtxt('Ts1_Experiment_Shear.csv',delimiter=',')
Wall_analysis_disp = np.loadtxt('Ts1_Load_Dsp.out',delimiter=' ')[1:, 1]
Wall_analysis_shear =np.loadtxt('Ts1_Wall_Reaction.out',delimiter=' ')[1:, 1]

Wall_exp_xy = np.column_stack([Wall_exp[:,0], Wall_exp[:,1]/1000])
Wall_anal_xy = np.column_stack([Wall_analysis_disp, -Wall_analysis_shear/1000])

def getHys():
    ExpHys = hys.Hysteresis(Wall_exp_xy[8300:,:])
    AnalHys = hys.Hysteresis(Wall_anal_xy[500:,:])
    
    return ExpHys, AnalHys

def test_Plot(monkeypatch):
    monkeypatch.setattr(plt, 'show', lambda: None)
    
    ExpHys,AnalHys= getHys()
    
    ExpHys.plot(True)
    plt.close()
    AnalHys.plot(True) 
    plt.close()
    
    assert True == True

def test_Plot_Index(monkeypatch):
    monkeypatch.setattr(plt, 'show', lambda: None)
    ExpHys,AnalHys= getHys()
    
    ExpHys.plotVsIndex(True)
    plt.close()
    AnalHys.plotVsIndex(True)
    plt.close()
    AnalHys.plotLoadProtocol(comparisonProtocol = ExpHys.loadProtocol)
    plt.close()

    assert True == True

def test_Plot_LoadProtocol(monkeypatch):
    monkeypatch.setattr(plt, 'show', lambda: None)
    
    ExpHys,AnalHys= getHys()
    ExpHys.plotLoadProtocol()
    plt.close()
    AnalHys.plotLoadProtocol(comparisonProtocol = ExpHys.loadProtocol)
    plt.close()
    assert True == True

def test_ReCalc():

    
    ExpHys, AnalHys= getHys()
    AnalHys.recalculateCycles(peakProminence = 0.005)

    assert True == True
    
def test_compare_loadProt(monkeypatch):
    
    ExpHys,AnalHys= getHys()
    AnalHys.recalculateCycles(peakProminence = 0.0045)
    ExpHys.recalculateCycles(peakProminence = 0.035*4.1/100/2)
    test1 = len(AnalHys.loadProtocol) == len(ExpHys.loadProtocol)

    assert test1 == True

def test_compare(monkeypatch):
    
    ExpHys,AnalHys= getHys()
    AnalHys.recalculateCycles(peakProminence = 0.0045)
    ExpHys.recalculateCycles(peakProminence = 0.035*4.1/100/2)
    
    AnalHys = hys.resample(AnalHys, 10)
    ExpHys = hys.resample(ExpHys, 10)
    
    Diff, Diffs = hys.compareHys(AnalHys, ExpHys)
    
    test1 = abs(Diff - 6.800144) < 0.00001
    
    assert test1 == True



# # Now we can resample and compare the curves!
# AnalHysDx = hys.reSample(AnalHys, 10)
# ExpHysDx = hys.reSample(ExpHys, 10)
# AnalHysDx.plotLoadProtocol(comparisonProtocol = ExpHysDx.loadProtocol)
# AnalHysDx.plot(True)
# ExpHysDx.plot(True)

# Diff, Diffs = hys.CompareHys(AnalHysDx, ExpHysDx)
    
    
#     assert True == True


