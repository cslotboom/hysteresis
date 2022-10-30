import hysteresis.baseFuncs as hys
from hysteresis.baseClass import Hysteresis, SimpleCycle
import numpy as np




x = np.linspace(0,1,101)
xy1 = np.column_stack([x,x])
xy2 = np.column_stack([x+1, x[::-1]])
# xy2 = np.column_stack([x+1, x[::-1]])
outputCurve1 = np.concatenate((xy1[:-1],xy2))
outputCurve_noskip = np.concatenate((xy1,xy1))


def test_concatenateHys():
    out = hys.concatenateHys((xy1,xy2))
    test1 = np.sum(out.xy - outputCurve1) < 0.0001
    test2 = isinstance(out, Hysteresis)
    assert test1 and test2

def test_concatenate():
    out = hys.concatenate((xy1, xy2), outputClass=SimpleCycle)
    print(out.xy)
    test1 = np.sum(out.xy - outputCurve1) < 0.0001
    test2 = isinstance(out, SimpleCycle)
    assert test1 and test2
    
def test_concatenate_noSkip():
    out = hys.concatenate((xy1, xy1), outputClass=SimpleCycle)
    test1 = np.sum(out.xy - outputCurve_noskip) < 0.0001
    test2 = isinstance(out, SimpleCycle)
    assert test1 and test2    
    

