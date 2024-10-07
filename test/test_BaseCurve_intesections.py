"""
Test if intersections can be found.
"""

import hysteresis.curve as hys
import numpy as np
from pytest import approx

# out = test_Curve3_Area()


def makeCurve(f):
    "lamda function that creates all curves"
    xdata = np.linspace(0,4,1001)
    y = f(xdata)
    xy = np.column_stack([xdata, y])
    Curve = hys.Curve(xy)   
    return Curve    

def function1(x):
    return x - 2

def function2(x):
    return x**3 - 5*x**2 + 5*x + -1

def function3(x):
    return 3 + (np.e)**x  
    


def test_data_Curve1():
    curve = makeCurve(function1)
    interInds = hys.data.getIntersections(curve.y)


    xyinter = curve.getXIntersections()
    assert len(interInds) ==1
    
def test_Curve1():
    curve = makeCurve(function1)

    xyinter = curve.getXIntersections()
    assert len(xyinter) ==1
    assert 2 == approx(xyinter[0][0],0.01)
    assert 0 == approx(xyinter[0][1],0.01,abs=True)
    
def test_data_Curve2():
    curve = makeCurve(function2)
    xyinter = hys.data.getIntersections(curve.y)
    
    assert len(xyinter) == 3

def test_Curve2():
    curve = makeCurve(function2)
    xyinter = curve.getXIntersections()
    
    assert len(xyinter) == 3    
    # assert 2 == approx(xyinter[0][0],0.01)
    assert 0 == approx(xyinter[0][1],0.01,abs=True)
    assert 0 == approx(xyinter[1][1],0.01,abs=True)
    assert 0 == approx(xyinter[2][1],0.01,abs=True)
    
    
    
def test_data_Curve3():
    curve = makeCurve(function3)
    xyinter = hys.data.getIntersections(curve.y)
    
    assert len(xyinter) == 0
   
def test_Curve3():
    curve = makeCurve(function3)
    xyinter = curve.getXIntersections()
    assert len(xyinter) == 0



def test_BMD_Curve():
    xyBmd = np.loadtxt('bmd.csv', delimiter=',')
    extraPoints = [[10,0],[10,0]]
    
    xyBmd = np.concatenate((xyBmd, extraPoints))
    myHys = hys.Curve(xyBmd) 

    xyinter = myHys.getXIntersections()
    
    # myHys.plot()
    # import matplotlib.pyplot as plt
    # plt.plot(xyinter[:,0], xyinter[:,1])
    assert len(xyinter) == 3


if __name__ == "__main__":
    test_data_Curve1()
    test_Curve1()
    
    test_data_Curve2()
    test_Curve2()
    
    test_data_Curve3()
    test_Curve3()
    
    test_BMD_Curve()