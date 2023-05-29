import numpy as np


from .curve import Curve

import matplotlib.pyplot as plt
from scipy.optimize import curve_fit



# =============================================================================
# Curve objects
# =============================================================================



# T is normalized to 1/T

def getTemp(t, a, b, Cx):
    return a*np.cos(2*np.pi*t + b) + Cx

def getDeltaTemp(n = 1, m = 1):

    def h(t, a, b, c, d, Cy):
        return a*np.cos(2*np.pi*t + b)**n + c*np.sin(2*np.pi*t + d)**m + Cy
    
    return(h)

def defaultFitCurve(f, xy, **kwargs):
    """
    A simple curve fiting implementation using Scipy's nonlinear least 
    squares method.

    Parameters
    ----------
    f : function
        The function to be fit.
    xy : array
        The 2D input array of x/y data.
    **kwargs : kwargs
        The keyword arguements to be passed to curve_fit.

    Returns
    -------
    coef : TYPE
        The output coefficients for the fit function.
    correlation : TYPE
        The output correlation matrix for the fit variables.

    """
    
    coef, correlation = curve_fit(f, xy[:,0], xy[:,1], **kwargs)
    
    return coef, correlation


class SeasonalCurve(Curve):
    """
    The input XY data is assumed to be evenly spaced in time.
    
    The curve will be closed so that the first point is equal to the final
    point.
    """
    
    
    def __init__(self, xy, period = 1, n = 1, m = 1):
        Curve.__init__(self, xy)
        
        self.time = np.arange(0, self.Npoints)/self.Npoints
        self.period = period
        self.n = n
        self.m = m
        
        self.tempFunction = getTemp
        self.dTempFunction = getDeltaTemp(n,m)
        
        self.tempCoef, self.tempCoer = curve_fit(self.tempFunction, self.time, xy[:,0])
        self.dTempCoef, self.dtempCoer  = curve_fit(self.dTempFunction, self.time, xy[:,1])
        
        
        self.fittedT = self.tempFunction(self.time, *self.tempCoef)
        self.fittedDT= self.dTempFunction(self.time, *self.dTempCoef)
        
        # Close the curve
        self.time = np.append(self.time, 1)
        self.fittedT = np.append(self.fittedT,self.fittedT[0])
        self.fittedDT = np.append(self.fittedDT,self.fittedDT[0])
        
        
        self.Cx = self.tempCoef[-1]
        self.Cy = self.dTempCoef[-1]
        

    def plotScatter(self):
        x = self.xy[:,0]
        y = self.xy[:,1]
        plt.plot(x, y, '.', linewidth = 0)

    def plotFittedCurve(self, xlim = [], ylim = []):
        
        x = self.fittedT
        y = self.fittedDT
        plt.plot(x, y)
        
        # return self.plotfunction(self, x ,y, 0, 0, xlim, ylim, 0)
    
    def plotTemp(self, xlim = [], ylim = []):
        
        
        x = self.time*self.period
        y = self.fittedT
        plt.plot(x, y)
        # return self.plotfunction(self, x ,y, 0, 0, xlim, ylim, 0) 
    
    
    def plotDTemp(self, xlim = [], ylim = []):
        
        x = self.time*self.period
        y = self.fittedDT
        plt.plot(x, y)
        # return self.plotfunction(self, x ,y, 0, 0, xlim, ylim, 0)     
    
    def printT(self):
        print('The expression for temperature is: ')
        print('a * np.cos(2*np.pi*t / T + b) + Cx')
        
        print('Where the coeficients are:')
        print('a = ', self.tempCoef[0])
        print('b = ', self.tempCoef[1])
        print('Cx = ', self.tempCoef[2])

    
    def printDT(self):
        
        print('The expression for delta temperature is: ')
        print('a * np.cos(2*np.pi*t / T + b)**n + c*np.sin(2*np.pi*t / T + d)**m + Cy')
        
        print('Where the coeficients are:')
        print('n = ', self.n)
        print('m = ', self.m)        
        print('a = ', self.dTempCoef[0])
        print('b = ', self.dTempCoef[1])
        print('c = ', self.dTempCoef[2])
        print('d = ', self.dTempCoef[3])
        print('Cy = ', self.dTempCoef[4])    
    
    
