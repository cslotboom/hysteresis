
import hysteresis.baseClass as hys
import numpy as np


def makeCurveBase(f):
    "lamda function that creates all curves"
    xdata = np.linspace(0,4,1001)
    y = f(xdata)
    xy = np.column_stack([xdata, y])
    Curve = hys.CurveBase(xy)   
    return Curve    

def function1(x):
    return x + 2

def function2(x):
    return x**3 - 3*x**2 + 3

def function3(x):
    return 3 + (np.e)**x  
    
    
    
curve = makeCurveBase(function2)

length = len(curve)
A = curve / 2
A = 2 / curve
    
# def test_Curve1_Area():
#     Curve = makeCurveBase(function1)
#     Curve.setArea()
#     A = Curve.getNetArea()

#     assert abs(A - 16) < 0.0001

# def test_Curve2_Area():
#     Curve = makeCurveBase(function2)
#     Curve.setArea()
#     A = Curve.getNetArea()
    
#     assert abs(A - 12) < 0.0001
    
# def test_Curv3_Area():
#     Curve = makeCurveBase(function3)
#     Curve.setArea()
#     A = Curve.getNetArea()

#     assert abs(A - (np.e**4 + 11)) < 0.0001

