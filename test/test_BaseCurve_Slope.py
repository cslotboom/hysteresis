import hysteresis.curve as hys
import numpy as np

def makeCurve(f):
    "lamda function that creates all curves"
    xdata = np.linspace(0,4,1001)
    y = f(xdata)
    xy = np.column_stack([xdata, y])
    Curve = hys.Curve(xy)   
    return Curve    

def function1(x):
    return x + 2

def function2(x):
    return x**3 - 3*x**2 + 3

def function3(x):
    return 3 + (np.e)**x  
        
def test_Curve1_Area():
    Curve = makeCurve(function1)
    Curve.setSlope()
    slope = Curve.slope
    
    test1 = (abs(slope[0] - 1) < 0.0001)
    test2 = (abs(slope[-1] - 1) < 0.0001)
    test3 = (abs(slope[50] - 1) < 0.0001)

    assert np.all([test1,test2,test3])

def test_Curve2_Area():
    Curve = makeCurve(function2)
    Curve.setSlope()
    slope = Curve.slope
    
    test1 = (abs(slope[0] - 0) < 0.05)
    test2 = (abs(slope[-1] - 24) < 0.05)
    test3 = (abs(slope[200] - (3*0.8**2 - 6*0.8)) < 0.0001)

    assert np.all([test1,test2,test3])

def test_Curve3_Area():
    Curve = makeCurve(function3)
    Curve.setSlope()
    slope = Curve.slope

    test1 = (abs(slope[0] - 1) < 0.01)
    test2 = (abs(slope[-1] - (np.e)**4) < 0.2)
    test3 = (abs(slope[200] - ((np.e)**0.8)) < 0.0001)

    assert np.all([test1,test2,test3])


# out = test_Curve3_Area()
    

