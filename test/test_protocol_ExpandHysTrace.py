
import hysteresis as hys
import numpy as np
import matplotlib.pyplot as plt

def makeCurve():
    "lamda function that creates all curves"
    t = np.linspace(0,4,1000)*np.pi
    x = np.cos(t)
    y = np.sin(t)*t
    
    xy = np.column_stack([x,y])
    Curve = hys.Hysteresis(xy)
    return Curve    



def test_expandHysTrace():
    curve = makeCurve()
    expand = hys.exandHysTrace(curve, [2])
    
    assert len(expand.cycles) == 6





# curve = makeCurve()
# curve.plotVsIndex()
# expand = hys.exandHysTrace(curve, [2])
# expand.plotVsIndex()
# test_expandHysTrace()

# curve = makeCurve()
# curve.plot()
# curve.plotLoadProtocol()
# fig, ax = curve.plotCycles()
# lines = fig.axes[0].lines
# for line in lines:
#     plt.setp(line, linestyle='--')

# print(curve.NCycles)
# # print(np.round(curve.loadProtocol))



# expand = hys.exandHysTrace(curve, [2])
# expand.plot()
# expand.plotLoadProtocol()
# fig, ax = curve.plotCycles()
# lines = fig.axes[0].lines
# for line in lines:
#     plt.setp(line, linestyle='--')
    



