import numpy as np
from numpy import trapz

from scipy.interpolate import interp1d
from hysteresis import data

import matplotlib.pyplot as plt




def defaultSlopeFunction(xy):
    """
    The standard slope function. The slope is undefined for reversal indexes.
    
    For middle points, a centeral finite difference scheme is used, which is 
    O(h**2) accurate for constant steps h.
    
    The slope is equal to the left difference for the end, and
    right difference for the start.
       
    Parameters
    ----------
    xy : Array
        The input xy data in dimension [Ndata, 2] .
        
    Returns
    -------
    The slope of the input cuve at each x point.

    """
    # TODO: Try to replace with numpy.gradient

    npoint = len(xy[:,0])
    if 3 < npoint:
        xyp = xy[2:, :]
        xyn = xy[:-2, :]
        
        dxMid = (xyp[:,0] - xyn[:,0])
        unDefinedIndex = np.array(np.where(dxMid == 0))
        dxMid[unDefinedIndex] = np.max(np.abs(dxMid))
        slopeMid = ((xyp[:,1] - xyn[:,1]) / dxMid)
        slopeMid[unDefinedIndex] = slopeMid[unDefinedIndex - 1]
        
    Startdx = xy[1,0] - xy[0,0]
    Enddx = xy[1,0] - xy[0,0]
    
    slopeStart = 0 
    slopeEnd = 0
    
    if Startdx != 0:
        slopeStart = (xy[1,1] - xy[0,1]) / Startdx
        
    if Startdx != 0:
        slopeEnd = (xy[-1,1] - xy[-2,1]) / Enddx
    
    return np.concatenate([[slopeStart], slopeMid, [slopeEnd]])  
   
def defaultAreaFunction(xy):
    """
    The standard area function. This is an implementation of the midpoint rule.
    
    Parameters
    ----------
    xy : Array
        The input xy data in dimension [Ndata, 2] .

    Returns
    -------
    Area of the xy curve under each point.

    """
    
    # calculate the difference between each point
    dx = np.diff(xy[:,0])    
    yMid = xy[0:-1,1] + np.diff(xy[:,1])/2
    
    areaMid = dx*yMid
    
    # Get the area on either side of the midpoint
    areap = areaMid[1:]
    arean = areaMid[:-1]
    
    # Get the total area of the point
    AreaCenter = ((areap + arean) / 2)
    AreaStart = (areaMid[0]) / 2
    AreaEnd = (areaMid[-1]) / 2   
    
    
    return np.concatenate([[AreaStart], AreaCenter, [AreaEnd]])

def defaultSampleFunction(xy1, xy2):
    """
    The sample function compares how similar two curves are. 
    If they are exactly the same it will return a value of zero.
    The default function returns the average error between each sample point in two arrays of x/y points,
    xy1 and xy2.
    
    Parameters
    ----------
    xy1 : array
        The first input 2D x/y array of points.
    xy2 : array
        The second input 2D x/y array of points.

    Returns
    -------
    float
        The average "distance" between each point on the curve. The output quantity is unitless.
    """

    
    x1 = xy1[:,0]
    x2 = xy2[:,0]
    y1 = xy1[:,1]
    y2 = xy2[:,1]
    
    diff = ((x1 - x2)**2 + (y1 - y2)**2)**(0.5)
    
    return np.sum(diff)/len(x1)


def defaultCombineDiff(diffs):
    """
    This function chooses how to combine the differences between the curves for each cycle.
    The default function returns the average difference for each cycle for a input list of differences
    

    Parameters
    ----------
    diffs : array
        The list of net differences for each input sample curve.

    Returns
    -------
    diffNet : float
        The total difference according too the function.

    """
    
    # The average difference for each curve
    diffNet = np.sum(diffs)/len(diffs)
    
    return diffNet


    

