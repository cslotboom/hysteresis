import numpy as np
from numpy import trapz

from scipy.interpolate import interp1d
from hysteresis import data


from .defaultDataFuncs import defaultAreaFunction, defaultSlopeFunction
from .defaultPlotFuncs import initializeFig, defaultPlotFunction, defaultShowCycles
from .baseClass import CurveBase

import matplotlib.pyplot as plt



# =============================================================================
# Curve objects
# =============================================================================


# T is normalized to 1/T

def getTemp(t, b, c, Cx):
    return b*np.cos(2*np.pi*t + c) + Cx

def getDeltaTemp(n = 1, m = 1):

    def h(t, a, b, c, d, Cy):
        return a*np.cos(2*np.pi*t + b)**n + c*np.sin(2*np.pi*t + d)**m + Cy
    
    return(h)





class SeasonalCurve(CurveBase):
    pass


    
    
    
    
    
