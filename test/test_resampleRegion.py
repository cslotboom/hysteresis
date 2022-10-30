import numpy as np
import hysteresis as hys
import matplotlib.pyplot as plt

from hysteresis.resample import (_getBreakPoints, _getOutsideRegions,
                                 resampleRegion)

t = np.linspace(0,4,1000)*np.pi
x = np.sin(t)
y = np.cos(t)*t
xy = np.column_stack([x,y])
ty = np.column_stack([t ,y])
tyReversed = np.column_stack([t[::-1] ,y[::-1]+y])



t2 = np.linspace(0,4,100)*np.pi
x2 = np.sin(t2)
y2 = np.cos(t2)*t2
xy = np.column_stack([x2,y2])
ty2 = np.column_stack([t2 ,y2])
tyReversed = np.column_stack([t2[::-1] ,y2[::-1]+y2])

tt = np.column_stack([t2 ,t2])
tHys = hys.Hysteresis(np.concatenate([ty2, tyReversed]))
# test.plot()
tHys.plot(marker='.')
resampled = hys.resampleRegion(tHys,20)
resampled.cycles[0].plot(marker='.', linewidth=0)
tHys.cycles[0].plot(marker='.', linewidth=0)
len(resampled)


regions1 = [[0.2,0.3], [0.8, 0.9]]
regions2 = [[0.,0.2], [0.8, 1]]

def test_getBreakpoints():
    breakpoints1 = np.array(_getBreakPoints(regions1))
    breakpoints2 = np.array(_getBreakPoints(regions2))
    check1 = np.sum(np.array([0.2, 0.3, 0.8, 0.9]) - breakpoints1) == 0
    check2 = np.sum(np.array([0., 0.2, 0.8, 1]) - breakpoints2) == 0
    assert check1 and check2

def test_getOutsideRegions():
    breakpoints1,_ = _getOutsideRegions(regions1)
    breakpoints2,_ = _getOutsideRegions(regions2)
    breakpoints1 = np.array(breakpoints1)
    breakpoints2 = np.array(breakpoints2)
    check1 = np.sum(np.array([[0, 0.2], [0.2, 0.3], [0.3, 0.8], [0.8, 0.9], [0.9, 1]]) - breakpoints1) == 0
    check2 = np.sum(np.array([[0, 0.2], [0.2, 0.8], [0.8, 1]]) - breakpoints2) == 0
    assert check1 and check2

"""
I'm having trouble thinking of a way to test these properly..
For now, I'm just checking that the number of indexes changed
correctly as a proxy. Not great.
"""

def test_resampleRegion_length():
    xy = hys.resampleRegion(tt,20)

    myHys = hys.Hysteresis(xy)
    assert len(myHys) == 120

def test_resampleRegion_length2():

    xy = hys.resampleRegion(ty, 5, regions1)
    myHys = hys.Hysteresis(xy)
    assert len(myHys) == 808
     
def test_resampleRegion_length3():
    xy = hys.resampleRegion(ty, 5, regions2)
    myHys = hys.Hysteresis(xy)
    # myHys.plot(marker='.')
    assert len(myHys) == 610
    


def test_resample_Monotonic():
    
    curve = hys.MonotonicCurve(tt)
    resampled = hys.resampleRegion(curve,20)

    assert len(resampled) == 120    
    
def test_resample_SimpleCycle_NoSubCycles():
    
    curve = hys.SimpleCycle(tt)
    resampled = hys.resampleRegion(curve,20)

    assert len(resampled) == 120    

def test_resample_SimpleCycle_SubCycles():
    """
    Confirms that the subcycle is resampled properly!
    """
    
    myHys = hys.SimpleCycle(ty2,True)
    # curve = hys.SimpleCycle(tt)
    resampled = hys.resampleRegion(myHys,20)
       
    assert len(resampled.subCycles[0]) == 46    


def test_resample_Hysteresis():
    """
    This is a test by proxy - I've manually looked a the curve to see
    I'm happy with it, and now we just confirm it's the same.
    Again, not great.

    """
    
    
    resampled = hys.resampleRegion(tHys,20)
       
    assert len(resampled) == 239   
