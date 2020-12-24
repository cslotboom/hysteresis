import numpy as np
import hysteresis.hys as hys

t = np.linspace(0,4,1000)*np.pi
x = np.sin(t)
y = np.cos(t)*t

xy = np.column_stack([x,y])



myHys = hys.Hysteresis(xy)
myHys.plot(plotCycles = True)
samllHys = hys.reSample(myHys, 10)
samllHys.plot()

out = hys.CompareHys(samllHys,myHys)









