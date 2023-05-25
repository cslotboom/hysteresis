
from .defaultDataFuncs import (defaultAreaFunction, defaultSlopeFunction, 
                                defaultSampleFunction, defaultCombineDiff,
                                defaultLengthFunction)

from .defaultPlotFuncs import initializeFig, defaultPlotFunction, defaultShowCycles



# =============================================================================
# Curve objects
# =============================================================================



class HYSTERESIS_ENVIRONMENT:
    
    def __init__(self):
        """
        Contains the standard functions needed by the hysteresis analysis.
        """
        
        self.fslope = defaultSlopeFunction
        self.fArea = defaultAreaFunction
        self.flength = defaultLengthFunction
        
        self.finit = initializeFig
        self.fplot = defaultPlotFunction
        self.fcycles = defaultShowCycles
        
        self.fSample = defaultSampleFunction
        self.fCombineDiff = defaultCombineDiff
        
    def restart(self):
        self.__init__()


environment = HYSTERESIS_ENVIRONMENT()

