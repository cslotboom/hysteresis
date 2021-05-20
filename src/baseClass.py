import numpy as np
from numpy import trapz

from scipy.interpolate import interp1d
from hysteresis import data


import hysteresis.env as env
import matplotlib.pyplot as plt


"""
TODO:
    For Monotonic curves:
    Find and time between peaks is optional.
    Find interesections
    FInd area nearest to current peak
"""


"""
TODO:
    Allow for custom headings:
    Perhaps a style object?

    Add limitts to the style object?    
    Make the limits part of the hysteresis object, so they don't need
    to continually be passed to each funciton.
"""



"""
TODO: Make Plot functions Lamda function, then specialize for slope, area, etc.

"""


# =============================================================================
# Curve objects
# =============================================================================

class CurveBase:
    """
    
    The curve base object represents a generic xy curve with no limitations.
    
    All other curves inherit from the CurveBase class. It has access to methods
    all other curves should have access to.
    This uncludes plotting functionality, slope functions, area functions, 
    and displacement functions.
    
    """
    
    def __init__(self, XYData, xunit = '', yunit = ''):
        """
        
        Parameters
        ----------
        XYData : array
            The input array of XY date for the curve.
        areaFunction : function, optional
            The function to be used to calcualte area. 
            The default is defaultareaFunction.
        slopefunction : function, optional
            The function to be used to calcualte slope. 
            The default is defaultareaFunction.
        plotfunction : function, optional
            The function to be used to plot the curve. 
            The default is defaultPlotFunction.
        xunit : str, optional
            The units on the x axis. The default is ''.
        yunit : str, optional
            The units on the y axis. The default is ''.

        """
        self.xy = XYData
        self.Npoints = len(XYData[:,0])
        # self.areaFunction = fArea
        # self.slopefunction = fslope
        # self.plotfunction = fplot
        
        self.areaFunction = env.environment.fArea
        self.slopefunction = env.environment.fslope
        self.plotfunction = env.environment.fplot
        
        self.initializeFig = env.environment.finit
        self.plotfunction = env.environment.fplot
        self.showCycles = env.environment.fcycles
        
        self.colorDict = {0:'C0', 1:'C1', 2:'C3'}
        
        self.xunit = xunit
        self.yunit = yunit
        
    def __len__(self):
        return len(self.xy[:,0])

    # def __truediv__(self, x):
    #     return self.xy[:,1] / x

    # def __rtruediv__(self, x):
    #     return x / self.xy[:,1]
    
    # def __mul__(self, x):
    #     y = self.xy[:,1]*x
    #     xy = np.column_stack([x,y])
        
    #     return self.xy[:,1]*x

    # def __add__(self, x):
    #     return self.xy[:,1] + x
    
    # def __sub__(self, x):
    #     return self.xy[:,1] - x
        
    def setArea(self):
        """ sets the area under each point of the curve using the area function"""
        self.area = self.areaFunction(self.xy)
        return self.area
    
    def getCumDisp(self):
        """ Gets the absolute value of cumulative displacement of the curve at each x value.
        """
        dx = np.diff(self.xy[:,0])
        return np.append(0, np.cumsum(np.abs(dx)))
    
    def getNetCumDisp(self, startIndex = 0, endIndex = 0):
        """ Gets the total cumulative displacement between the start and start and end 
        indexes. By default the whole curve us used.
        """
        x = self.xy[:,0]
        dx = np.append(0, np.diff(self.xy[:,0]))
        
        if endIndex == 0:
            endIndex = self.Npoints
                   
        return np.sum(np.abs(dx[startIndex:endIndex]))
    
    def getCumArea(self):
        """ Gets the cumulative area under the curve for the entire curve
        """
        Area = self.area
        return np.cumsum(Area)
    
    def getNetArea(self, startIndex = 0, endIndex = 0):
        """
        Returns the net area between two indexes in the xy curve. The default 
        setting is to return the area for the whole cuve.

        """
        Area = self.area

        if endIndex == 0:
            endIndex = self.Npoints
                   
        return np.sum(Area[startIndex:endIndex])
           
    def setSlope(self):
        """
        Calcuates the slope of the curve at each point.
        The user can pass in a custom function that calculates the slope.
        """
        
        # Calculate end point slope
        xy = self.xy
        self.slope  = self.slopefunction(xy)
    
    def setPeaks(self, peakDist = 2, peakWidth = None, peakProminence = None):
        """
        Finds the indexes of max and min points, then stores them.
        """
        
        y = self.xy[:,1]
        peakIndexes = data.getCycleIndicies(y, peakDist, peakWidth, peakProminence)        
        self.peakIndexes = peakIndexes
        
        xy = self.xy
        if xy[peakIndexes[0],1] < xy[peakIndexes[1],1]:
            self.minIndexes = peakIndexes[0::2]
            self.maxIndexes = peakIndexes[1::2]
        else:
            self.minIndexes = peakIndexes[1::2]
            self.maxIndexes = peakIndexes[0::2]    
        
    def plot(self, plotCycles = False, plotPeaks = False, labelCycles = []):
        """
        Plots the base curve
        """        
        x = self.xy[:,0]
        y = self.xy[:,1]
                    
        return self.plotfunction(self, x ,y, plotCycles, plotPeaks, labelCycles)
                
    def plotVsIndex(self, plotCycles = False, plotPeaks = False, 
                     labelCycles = []):
        """
        Plots the base curve against index (as opposed to X values)
        """          
        
        x = np.arange(0,len(self.xy[:,0]))
        y = self.xy[:,0]
                    
        self.plotfunction(self, x ,y, plotCycles, plotPeaks, labelCycles)

    def plotLoadProtocol(self, comparisonProtocol = []):
        """
        Plots the peak x values for each cycle in acurve.
        """           
        plotCycles = False
        plotPeaks = False
        labelCycles = []
        y = self.loadProtocol
        x = np.arange(0,len(y))
                    
        self.plotfunction(self, x ,y, plotCycles, plotPeaks, labelCycles)
        
        if len(comparisonProtocol) != 0:
            plt.plot(comparisonProtocol)    
    
    def plotSlope(self,  plotCycles = False, plotPeaks = False, 
                  labelCycles = []):
        
        x = self.xy[:,0]
        y = self.slope

        self.plotfunction(self, x ,y, plotCycles, plotPeaks, labelCycles)
                
    def plotArea(self,  plotCycles = False, plotPeaks = False, labelCycles = []):
        
        x = self.xy[:,0]
        y = self.area

        self.plotfunction(self, x ,y, plotCycles, plotPeaks, labelCycles)  
                        
    def plotCumArea(self,  plotCycles = False, plotPeaks = False, labelCycles = []):
        
        # We get the cumulative displacement and area
        x = self.getCumDisp()
        y = self.getCumArea()

        self.plotfunction(self, x ,y, plotCycles, plotPeaks, labelCycles)  
             
    def initFig(self, xlims = [], ylims = []):
        return self.initializeFig(xlims, ylims)


# TODO:
    # Make the Hysteresis object take in the optional arguements as well. This
    # Curretnly will not work for non-basic funcitons.
    
    # This can potentially be fixed by having the user overwrite the default 
    # function

# =============================================================================
# 
# =============================================================================


class Hysteresis(CurveBase):
    """
    Hysteresis objects are those that have at least one reversal point in 
    the x direction of the data.
    
    The hysteresis object has a number of functions that help find the reversal
    points in the x data of the curve.
    
    The hysteresis object also stores each each half-cycle (where there is no
    change in direction) as a SimpleCycle object.
    
    """
    
    revDist = 2
    revWidth = None
    revProminence = None

    def __init__(self, XYData, revDist = 2, revWidth = None, revProminence = None,
                 setCycles = True, setArea = True, setSlope = True, **kwargs):
        CurveBase.__init__(self, XYData, **kwargs)

        #TODO Create warning if cycles don't make sense.
        if setCycles == True:
            self.setReversalIndexes(revDist, revWidth, revProminence)
            self.setCycles()
        
        if setArea ==True:
            self.setArea()
        if setSlope ==True:
            self.setSlope()
    
    def setReversalPropreties(self, revDist = 2, revWidth = None, 
                           revProminence = None):
        """
        Sets the propreties that are used to caculate where reversal points occur.
        These are used if we want to copy new classes using the same parameters.
        """
        self.revDist = revDist
        self.revWidth = revWidth
        self.revProminence = revProminence
        
        
    def setReversalIndexes(self, revDist = 2, revWidth = None, 
                           revProminence = None, **kwargs):
        """ Finds the location of the reversal points
        """
        
        # Deprication waring
        findPeakKwargs(**kwargs)
       
        self.setReversalPropreties(revDist, revWidth, revProminence)
        
        x = self.xy[:,0]
        self.reversalIndexes = data.getCycleIndicies(x, revDist, revWidth, revProminence)
        self.loadProtocol = x[self.reversalIndexes]

    def getReversalxy(self):
        """
        Gets the reversal xy indexes
        """
        return self.xy[self.reversalIndexes]
    
    def setCycles(self):
        """ Stores all simple cycle objects in the Hysteresis
        """
        xy = self.xy
        indices = self.reversalIndexes
        NIndex = len(indices) - 1
        
        Cycles = [None]*NIndex
        for ii in range(NIndex):
            # I forget why we overshoot the cycles here by one
            Cycles[ii] = SimpleCycle(xy[indices[ii]:(indices[ii+1]+1), :])
                       
        self.cycles = Cycles
        self.NCycles = NIndex
        self.NCycles = len(Cycles)
    
    def getCycles(self, Indicies):
        """ Returns a list of cycles given a list of indicies"""
        Cycles = [self.cycles[index] for index in Indicies]
        return Cycles      
    
    def getCycle(self, Index):
        """ Returns a list of cycles given a input index"""
        return self.cycles[Index]

    def setCycleNetAreas(self):
        """ Calculates the net area under each cycle."""
        areas = np.zeros(self.NCycles)
        for ii, vector in enumerate(self.cycles):
            # Skip the last point to avoid counting it twice!
            areas[ii] = vector.getNetArea(endIndex = -1)
            
        self.CycleAreas = areas

    def setNetArea(self):
        """ Sets the net area of the whole Hysteresis """
        self.NetArea = np.sum(self.area)

    def plotCycle(self, Index, plotPeaks = False):
        """ Plots a specific cycle."""
        Cycle = self.cycles[Index]
        return Cycle.plot(plotPeaks = plotPeaks)

    def plotCycles(self, Cycles = [], plotCycles = False, plotPeaks = False, 
                    labelCycles = []):
        """ Plots several cycles on the same figure """
        xyHys = self.xy
        Vectors = self.cycles
        # fig, ax = initializeFig(xlim, ylim)
        
        self.showCycles(self, xyHys[:,0], xyHys[:,1], plotCycles, plotPeaks, labelCycles, Cycles)
        
        colorDict = self.colorDict
        
        # If the list is empty, plot everything
        if len(Cycles) == 0:
            for ii, vector in enumerate(Vectors):
                c = colorDict[int(np.floor((ii + 1)/2) % 3)]
                c = colorDict[int(np.floor((ii + 1)/2) % 2)]
                # c = colorDict[int( ii % 2)]
                plt.plot(vector.xy[:,0], vector.xy[:,1], c=c)
                # plt.plot(vector.xy[:,0], vector.xy[:,1])

        else:
            for ii, vector in enumerate(Vectors):
                if ii in Cycles:
                    # c = colorDict[int(np.floor((ii + 1)/2) % 3)]
                    # plt.plot(vector.xy[:,0], vector.xy[:,1], c=c)
                    plt.plot(vector.xy[:,0], vector.xy[:,1])
            
        # return fig, ax    
    
       
    def recalculateCycles(self, revDist = 2, revWidth = None, revProminence = None, **kwargs):
        """
        Calcualtes the cycles again, using the input parameters for distance,
        width, and prominence. Peaks are calculated using scipy's find_peaks function.
        
        Parameters
        ----------
            
        revDist : number, optional
            The minimum minimal numbr of indexese (>= 1) in samples between
            neighbouring peaks. Smaller peaks are removed first until the condition
            is fulfilled for all remaining peaks.
        revProminence : number or ndarray or sequence, optional
            Required prominence of peaks. Either a number, ``None``, an array
            matching `x` or a 2-element sequence of the former. The first
            element is always interpreted as the  minimal and the second, if
            supplied, as the maximal required prominence.
        revWidth : number or ndarray or sequence, optional
            Required width of peaks in samples. Either a number, ``None``, an array
            matching `x` or a 2-element sequence of the former. The first
            element is always interpreted as the  minimal and the second, if
            supplied, as the maximal required width.
        
        
        Returns
        -------
        None.

        """
        
        # Deprication waring, remove later
        findPeakKwargs(**kwargs)
        
        self.setReversalIndexes(revDist, revWidth, revProminence)
        self.setCycles()
        self.setArea()
        
        
    def recalculateCycles_like(self, sampleHysteresis):
        """
        Recalulates the peaks of one hysteresis using another the reversal
        propreties from another hysteresis. Peaks are calculated using scipy's 
        find_peaks function.
        
        Parameters
        ----------
            
        sampleHysteresis : Hysteresis, optional
            The hysteresis to be be used when recalculating the cycle points.

        
        
        Returns
        -------
        None.

        """        
        revDist = sampleHysteresis.revDist
        revWidth = sampleHysteresis.revWidth
        revProminence = sampleHysteresis.revProminence
       
        self.setReversalIndexes(revDist, revWidth, revProminence)
        self.setCycles()
        self.setArea()        
    

    def RemoveCycles():
        pass

class SimpleCycle(CurveBase):
    """ A curve that doesn't change direction on the X axis, but can change
    Y direction.
    """
    
    def __init__(self, XYData, findPeaks = False, setSlope = False, setArea = False,
                 peakDist = 2, peakWidth = None, peakProminence = None):
        CurveBase.__init__(self, XYData)
        
        self._setDirection()
            
        if setArea == True:
            self.setArea()       
        
        if findPeaks == True:
            self.setPeaks(peakDist, peakWidth, peakProminence)
            self.setSubCycles()
    
        if setSlope == True:
            self.setSlope()

       
    def _setDirection(self):
        """
         1 = left to right. -1 = to is right to left

        """
        xdata = self.xy[:,0]
        if xdata[0] <= xdata[-1]:
            self.direction =  1
        else:
            self.direction = -1
           
                
    def setSubCycles(self):
        """
        Peaks must be set before subcyles can be set.

        """
        # TODO
        # Try to set peaks, then try to set MonotonicCurves.

        xy = self.xy
        indices = self.peakIndexes
        NIndex = len(indices) - 1
        
        SubCycles = [None]*NIndex
        for ii in range(NIndex):
            SubCycles[ii] = MonotonicCurve(xy[indices[ii]:(indices[ii+1]+1), :])
                       
        self.subCycles = SubCycles
        self.NsubCycles = len(SubCycles)
        
        
    def setSubCyclesArea(self):
        """
        Sets the net area for all SubCycles
        """
        try:
            SubCycles = self.subCycles
        except:
            raise Exception('No SubCycles not yet set')
            
        for subCycle in SubCycles:
            subCycle._setNetArea        

    def setSubCyclesSlope(self):
        """
        Sets the net area for all MonotonicCurves
        """
        try:
            SubCycles = self.subCycles
        except:
            raise Exception('SubCycles not yet set')
            
        for SubCycle in SubCycles:
            SubCycle.setSlope()       
      
    def getSubCycles(self, Indicies):
        SubCycles = [self.subCycles[index] for index in Indicies]
        return SubCycles      
    
    def getSubCycle(self, Index):
        return self.subCycles[Index]
     
    def plotSubCycles(self, SubCyclesIndicies = [], plotCycles = False, plotPeaks = False):
        
        xyMono = self.xy
        Vectors = self.subCycles
        
        self.showCycles(self, xyMono[:,0], xyMono[:,1], plotCycles, plotPeaks)
        
        colorDict = self.colorDict
        if len(SubCyclesIndicies) == 0:
            for ii, vector in enumerate(Vectors):
                c = colorDict[ii%2]
                plt.plot(vector.xy[:,0], vector.xy[:,1], c = c)

        else:
            for ii, vector in enumerate(self.SimpleCycles):
                if ii in SubCyclesIndicies:
                    c = colorDict[ii%2]
                    plt.plot(vector.xy[:,0], vector.xy[:,1], c = c)
            
            
    def recalculatePeaks(self, peakDist = 2, peakWidth = None, peakProminence = None):
        """
        Peaks are calculated using scipy's find_peaks function
        
        Parameters
        ----------
            
        distance : number, optional
            Required minimal horizontal distance (>= 1) in samples between
            neighbouring peaks. Smaller peaks are removed first until the condition
            is fulfilled for all remaining peaks.
        prominence : number or ndarray or sequence, optional
            Required prominence of peaks. Either a number, ``None``, an array
            matching `x` or a 2-element sequence of the former. The first
            element is always interpreted as the  minimal and the second, if
            supplied, as the maximal required prominence.
        width : number or ndarray or sequence, optional
            Required width of peaks in samples. Either a number, ``None``, an array
            matching `x` or a 2-element sequence of the former. The first
            element is always interpreted as the  minimal and the second, if
            supplied, as the maximal required width.
        
        
        Returns
        -------
        None.

        """
        self.setPeaks(peakDist, peakWidth, peakProminence)
        self.setSubCycles()
        self.setArea()  

class MonotonicCurve(CurveBase):
    def __init__(self, XYData):
        CurveBase.__init__(self, XYData)
        
        self._setDirection()
            
    def _setDirection(self):
        """
         1 = neg to pos. -1 = pos to neg
        """
        ydata = self.xy[:,1]
        if ydata[0] <= ydata[-1]:
            self.direction =  1
        else:
            self.direction = -1


# =============================================================================
# Deprication warnings
# =============================================================================

def findPeakKwargs(**kwargs):
    if 'peakDist' in kwargs.keys():
        raise Exception('Use of "peakDist" has been depricated. Instead use "revDist".')
    if 'peakDist' in kwargs.keys():
        print('Use of "peakWidth" has been depricated. Instead use "revWidth".')
    if 'peakProminence' in kwargs.keys():
        print('Use of "peakProminence" has been depricated. Instead use "revProminence".')    
    
    # pass