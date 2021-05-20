# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 23:47:36 2020

@author: Christian
"""
import hysteresis as hys
import numpy as np
import matplotlib.pyplot as plt
from hysteresis.plotSpecial import CycleViewer


disp = np.loadtxt('UFP_Disp.out',delimiter=' ')
force = np.loadtxt('UFP_RFrc.out',delimiter=' ')
testHys2 = np.column_stack([disp[:,1], -force[:,1]])

DamperHys = hys.Hysteresis(testHys2) 
# DamperHys.plot(True)

# viewer = ani.CycleViewer(DamperHys)
# viewer = ani.CycleViewerCum(DamperHys)


# fig, ax = plt.subplots()
# ax.set_xlim([0,1])
CycleViewer(DamperHys, xlims = [0,20])
# viewer.updateplt(0)
# viewer.updateplt(0)
