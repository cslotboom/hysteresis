
import hysteresis.curve as hys
import numpy as np
import pytest

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
    
def test_len():
    curve = makeCurve(function2)
    length = len(curve)
    assert length == 1001

# =============================================================================
# 
# =============================================================================

def test_get_Operand_scalar():
    assert hys._getOperand(2) == 2

def test_get_Operand_flat_array():
    arrayIn = np.linspace(0,4,101)
    assert np.all(hys._getOperand(arrayIn) == arrayIn)

def test_get_Operand_2D_array():
    xdata = np.linspace(0,4,1001)
    y = function3(xdata)
    xy = np.column_stack([xdata, y])
    assert np.all(hys._getOperand(xy) == y)

def test_get_Operand_2D_array_failure():
    with pytest.raises(Exception):
        xdata = np.linspace(0,4,1001)
        y = function3(xdata)
        xy = np.column_stack([xdata, y,y])
        hys._getOperand(xy)

# =============================================================================
# 
# =============================================================================

def test_multiplication_scalar():
    curve = makeCurve(function2)
    newCurve = curve*8
    assert np.all(newCurve.xy[:,1] == curve.xy[:,1]*8)

def test_multiplication_Array():
    curve = makeCurve(function2)
    newCurve = curve*curve.xy
    assert np.all(newCurve.xy[:,1] == curve.xy[:,1]**2)

def test_multiplication_Curve():
    curve = makeCurve(function3)
    newCurve = curve*curve
    assert np.all(newCurve.xy[:,1] == curve.xy[:,1]**2)
# =============================================================================
# 
# =============================================================================

def test_addition_scalar():
    curve = makeCurve(function2)
    newCurve = curve+8
    assert np.all(newCurve.xy[:,1] == curve.xy[:,1]+8)

def test_addition_Array():
    curve = makeCurve(function2)
    newCurve = curve + curve.xy
    assert np.all(newCurve.xy[:,1] == curve.xy[:,1]*2)

def test_addition_Curve():
    curve = makeCurve(function3)
    newCurve = curve+curve
    assert np.all(newCurve.xy[:,1] == curve.xy[:,1]*2)

# =============================================================================
# 
# =============================================================================

def test_subtraction_scalar_L():
    curve = makeCurve(function2)
    newCurve = curve-8
    assert np.all(newCurve.xy[:,1] == curve.xy[:,1]-8)

def test_subtraction_scalar_R():
    curve = makeCurve(function2)
    newCurve = 8 - curve
    assert np.all(newCurve.xy[:,1] == 8 - curve.xy[:,1])
    
    
def test_subtraction_Array_L():
    curve = makeCurve(function2)
    newCurve = curve - curve.xy
    assert np.all(newCurve.xy[:,1] == 0)
    
def test_subtraction_Array_R():
    curve = makeCurve(function2)
    newCurve =  curve.xy - curve 
    assert np.all(newCurve.xy[:,1] == 0)
    
    
def test_subtraction_Curve():
    curve = makeCurve(function3)
    newCurve = curve-curve
    assert np.all(newCurve.xy[:,1] == 0)

# =============================================================================
# 
# =============================================================================

def test_division_scalar_L():
    curve = makeCurve(function2)
    newCurve = curve/8
    assert np.all(newCurve.xy[:,1] == curve.xy[:,1]/8)

def test_division_scalar_R():
    curve = makeCurve(function2)
    newCurve = 8 / curve
    assert np.all(newCurve.xy[:,1] == 8 / curve.xy[:,1])
    
    
def test_division_Array_L():
    curve = makeCurve(function2)
    newCurve = curve / curve.xy
    assert np.all(newCurve.xy[:,1] == 1)
    
def test_division_Array_R():
    curve = makeCurve(function2)
    newCurve =  curve.xy / curve 
    assert np.all(newCurve.xy[:,1] == 1)
    
    
def test_division_Curve():
    curve = makeCurve(function3)
    newCurve = curve/curve
    assert np.all(newCurve.xy[:,1] == 1)
    


# curve = makeCurve(function2)
# test = np.array(curve)



# test_subtraction_scalar_L()
# test_subtraction_scalar_R()
# test_subtraction_Array_L()
# # test_subtraction_Array_R()
# test_subtraction_Curve()