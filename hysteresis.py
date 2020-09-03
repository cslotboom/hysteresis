import numpy as np
from numpy import trapz

from scipy.interpolate import interp1d
from openseespytools import data

import matplotlib.pyplot as plt

       


"""
I'm not sure if I want to store the xy data at both levels, i.e. in the Cycle
AND in the 
"""



"""
Should resample make a new curve, or modify the old one?
Making a copy is probably quite slow, but it is "safer".

Could we store a base XY curve, and a sample xy curve?
"""



"""
The termonology of reversal indixes is vague

However, we don't necessarily always want to have these peaks, I'm not sure
it makes sense to calcuale them by default
"""

"""
TODO:
    Create function that get's peak times and values'
"""

"""
TODO:
    For Monotonic curves:
    Find and time between peaks is optional.
    Find interesections
    FInd area nearest to current peak
"""


"""
TODO:
    Seperate functions from base classes
"""


"""
TODO:
    Allow for custom headings:
    Perhaps a style object?
"""




def defaultSlopeFunction(xy):
    """
    The standard slope function. The slope is indefined for reversal indexes.
    
    For middle points, a centeral finite difference scheme is used, which is 
    O(h**2) accurate for constant steps h.
    
    The slope is equal to the left difference for the end, and
    right difference for the start.

    xy : the input xy data
    
    TODO: Try to replace with numpy.gradient
    """
    npoint = len(xy[:,0])
    if 3 < npoint:
        xyp = xy[2:, :]
        xyn = xy[:-2, :]
        
        dxMid = (xyp[:,0] - xyn[:,0])
        unDefinedIndex = np.array(np.where(dxMid == 0))
        dxMid[unDefinedIndex] = np.max(np.abs(dxMid))
        
        # slopeMid = ((xyp[:,1] - xyn[:,1]) / (xyp[:,0] - xyn[:,0]))
        slopeMid = ((xyp[:,1] - xyn[:,1]) / dxMid)
        slopeMid[unDefinedIndex] = slopeMid[unDefinedIndex - 1]
    
    # TODO: why would the slope equal = 0 here???
    # else:
    #     slopeMid = []
    
    Startdx = xy[1,0] - xy[0,0]
    Enddx = xy[1,0] - xy[0,0]
    
    if Startdx == 0:
        a = 1
        pass
    
    slopeStart = (xy[1,1] - xy[0,1]) / Startdx
    slopeEnd = (xy[-1,1] - xy[-2,1]) / Enddx
    
    return np.concatenate([[slopeStart], slopeMid, [slopeEnd]])  
   
def defaultAreaFunction(xy):
    """
    The standard area function. This is an implementation of the midpoint rule.
    
    Parametere
    ----------
    xy : the input xy data
        DESCRIPTION.

    Returns
    -------
    None.

    """
    
    
    dx = np.diff(xy[:,0])    
    yMid = xy[0:-1,1] + np.diff(xy[:,1])/2
    
    areaMid = dx*yMid
    
    areap = areaMid[1:]
    arean = areaMid[:-1]
    
    AreaCenter = ((areap + arean) / 2)
    AreaStart = (areaMid[0]) / 2
    AreaEnd = (areaMid[-1]) / 2   
    
    
    return np.concatenate([[AreaStart], AreaCenter, [AreaEnd]])

def initializeFig(xlim, ylim):


    fig, ax = plt.subplots()

    if len(xlim) != 0 :
        ax.set_xlim(xlim[0],xlim[1])

    if len(ylim) != 0 :
        ax.set_ylim(ylim[0], ylim[1])
               
    return fig, ax

def defaultShowCycles(self, x, y, plotCycles, plotPeaks, labelCycles = []):
    """Plots the location of the peaks and CycleReversals"""
    
    # Plot cycles as x only
    if plotPeaks == True:
        try:
            Indexes = self.peakIndexes
        except:
            raise Exception('No peaks have been set')
        PeakX = x[Indexes]
        PeakY = y[Indexes]

        line2  = plt.plot(PeakX, PeakY, "+")
        # plt.title('Peak Index y values')    # Plot cycles as x only
        
    if plotCycles == True:
        try:
            Indexes = self.reversalIndexes        
        except:
            raise Exception("Can't display cycles because object is not a Hysteresis.")
        # TODO: update marker based on direction?
        # minIndexes = self.
        # minIndexes = 
        ReversalX = x[Indexes]
        ReversalY = y[Indexes]        

        line2  = plt.plot(ReversalX, ReversalY, "x")
                
        for ii in labelCycles:
                # Annotate = plt.annotate(int(ii), xy=(ReversalX[ii], ReversalY[ii]),xytext=(-10, 10), arrowprops=dict(arrowstyle="->"))
                Annotate = plt.annotate(int(ii), xy=(ReversalX[ii], ReversalY[ii]), xytext=(5, 5),textcoords = 'offset points')
                # Annotate = plt.annotate(int(ii), xy=(ReversalX[ii], ReversalY[ii]))


def defaultPlotFunction(self, x, y, plotCycles, plotPeaks, xlim = [], ylim = [], labelCycles = []):
    #TODO: right now it is not possible to have overlap between functions using this method
    fig, ax = initializeFig(xlim, ylim)
          
    line1 = plt.plot(x, y)
       
    defaultShowCycles(self, x, y, plotCycles, plotPeaks, labelCycles)

    return fig, ax


class CurveBase:
    """
    Stuff that every curve should have, like plot
    """
    
    def __init__(self, XYData, AreaFunction = defaultAreaFunction, 
                 slopefunction = defaultSlopeFunction, 
                 plotfunction = defaultPlotFunction, xunit = '', yunit = ''):
        self.xy = XYData
        self.Npoints = len(XYData[:,0])
        self.AreaFunction = defaultAreaFunction
        self.slopefunction = defaultSlopeFunction
        self.plotfunction = defaultPlotFunction
        
        self.colorDict = {0:'C0', 1:'C1', 2:'C3'}
        
        self.xunit = xunit
        self.yunit = yunit
        
    def __len__(self):
        return len(self.xy[:,0])

    # def __mul__(self,x):
    #     print(x)

    def setArea(self):
        self.Area = self.AreaFunction(self.xy)
        return self.Area
    
    def getCumArea(self):
        Area = self.Area
        return np.cumsum(Area)
    
    def getNetArea(self, StartIndex = 0, EndIndex = 0):
        """
        Returns the area between two indexes in the xy curve. The default 
        setting is to return the area for the whole cuve.

        """
        Area = self.Area

        if EndIndex == 0:
            EndIndex = self.Npoints
                   
        return np.sum(Area[StartIndex:EndIndex])
           
    def setSlope(self):
        """
        The user can pass in a custom function that calculates the slope.
        """
        
        # Calculate end point slope
        xy = self.xy
        self.Slope  = self.slopefunction(xy)
    
    def setPeaks(self, peakDist = 2, peakWidth = None, peakProminence = None):
        "Finds the max and min indexes"
        
        y = self.xy[:,1]
        peakIndexes = data.GetCycleIndicies(y, peakDist, peakWidth, peakProminence)        
        self.peakIndexes = peakIndexes
        
        xy = self.xy
        if xy[peakIndexes[0],1] < xy[peakIndexes[1],1]:
            self.minIndexes = peakIndexes[0::2]
            self.maxIndexes = peakIndexes[1::2]
        else:
            self.minIndexes = peakIndexes[1::2]
            self.maxIndexes = peakIndexes[0::2]    
    
    def plot(self, plotCycles = False, plotPeaks = False, 
             xlim = [], ylim = [], labelCycles = []):
        """
        TODO: Make Lamda function, then specialize for slope, area, etc.
        """
        
        x = self.xy[:,0]
        y = self.xy[:,1]
                    
        fig, ax = self.plotfunction(self, x ,y, plotCycles, plotPeaks, 
                                    xlim, ylim, labelCycles)
        
        # plt.show()        
        
        return fig, ax

    def plotVsIndex(self, plotCycles = False, plotPeaks = False, 
                    xlim = [], ylim = [], labelCycles = []):
          
        x = np.arange(0,len(self.xy[:,0]))
        y = self.xy[:,0]
                    
        fig, ax = self.plotfunction(self, x ,y, plotCycles, plotPeaks, 
                                    xlim, ylim, labelCycles)
        
        # plt.show()        
        
        return fig, ax

    def plotLoadProtocol(self, xlim = [], ylim = [], comparisonProtocol = []):
        plotCycles = False
        plotPeaks = False
        labelCycles = []
        y = self.loadProtocol
        x = np.arange(0,len(y))
                    
        fig, ax = self.plotfunction(self, x ,y, plotCycles, plotPeaks, 
                                    xlim, ylim, labelCycles)
        
        if len(comparisonProtocol) != 0:
            plt.plot(comparisonProtocol)
        # plt.show()        
        return fig, ax
    
    
    def plotSlope(self,  plotCycles = False, plotPeaks = False, 
                  xlim = [], ylim = [], labelCycles = []):
        
        x = self.xy[:,0]
        y = self.Slope

        fig, ax = self.plotfunction(self, x ,y, plotCycles, plotPeaks, 
                                    xlim, ylim, labelCycles)


        # plt.show()
        
        return fig, ax
        
    def plotArea(self,  plotCycles = False, plotPeaks = False, 
                 xlim = [], ylim = [], labelCycles = []):
        
        x = self.xy[:,0]
        y = self.Area

        fig, ax = self.plotfunction(self, x ,y, plotCycles, plotPeaks, 
                                    xlim, ylim, labelCycles)  
        
        # plt.show()       
        
        return fig, ax        
    
    def plotCumArea(self,  plotCycles = False, plotPeaks = False, 
                    xlim = [], ylim = [], labelCycles = []):
        
        # We get the cumulative displacement and area
        x = np.cumsum(np.abs(self.xy[:,0]))
        y = self.getCumArea()

        fig, ax = self.plotfunction(self, x ,y, plotCycles, plotPeaks, 
                                    xlim, ylim, labelCycles)  
        
        # plt.show()       
        
        return fig, ax   



class Hysteresis(CurveBase):
    
    def __init__(self, XYData, setCycles = True, setArea = True, setSlope =True):
        CurveBase.__init__(self, XYData)

        #TODO Create warning if cycles don't make sense.
        if setCycles == True:
            self.setReversalIndexes()
            self.setCycles()
        
        #TODO: Evaluate how long this takes, then potentiall ymake optional
        if setArea ==True:
            self.setArea()
        if setSlope ==True:
            self.setSlope()
            
    def setReversalIndexes(self, peakDist = 2, peakWidth = None, 
                           peakProminence = None):
        x = self.xy[:,0]
        self.reversalIndexes = data.GetCycleIndicies(x, peakDist, peakWidth, peakProminence)
        self.loadProtocol = x[self.reversalIndexes]
    
    
    def setCycles(self):
        xy = self.xy
        indices = self.reversalIndexes
        NIndex = len(indices) - 1
        
        Cycles = [None]*NIndex
        for ii in range(NIndex):
            Cycles[ii] = SimpleCycle(xy[indices[ii]:(indices[ii+1]+1), :])
                       
        self.Cycles = Cycles
        self.NCycles = NIndex
        self.NCycles = len(Cycles)
    
    def getCycles(self, Indicies):
        Cycles = [self.Cycles[index] for index in Indicies]
        return Cycles      
    
    def getCycle(self, Index):
        return self.Cycles[Index]

    def setCycleNetAreas(self):
        areas = np.zeros(self.NCycles)
        for ii, vector in enumerate(self.Cycles):
            # Skip the last point to avoid counting it twice!
            areas[ii] = vector.getNetArea(EndIndex = -1)
            
        self.CycleAreas = areas

    def setNetArea(self):
        self.NetArea = np.sum(self.area)

    def plotCycle(self, Index, plotPeaks = False, xlim = [], ylim = []):       
        Cycle = self.Cycles[Index]
        return Cycle.plot(plotPeaks = plotPeaks, xlim = xlim, ylim = ylim)

    def plotCycles(self, Cycles = [], plotCycles = False, plotPeaks = False, 
                   xlim = [], ylim = [], labelCycles = []):
        
        xyHys = self.xy
        Vectors = self.Cycles
        fig, ax = initializeFig(xlim, ylim)
        
        defaultShowCycles(self, xyHys[:,0], xyHys[:,1], plotCycles, plotPeaks, labelCycles)
        
        colorDict = self.colorDict
        
        # If the list is empty, plot everything
        if len(Cycles) == 0:
            for ii, vector in enumerate(Vectors):
                # c = colorDict[int(np.floor((ii + 1)/2) % 3)]
                # plt.plot(vector.xy[:,0], vector.xy[:,1], c=c)
                plt.plot(vector.xy[:,0], vector.xy[:,1])

        else:
            for ii, vector in enumerate(Vectors):
                if ii in Cycles:
                    # c = colorDict[int(np.floor((ii + 1)/2) % 3)]
                    # plt.plot(vector.xy[:,0], vector.xy[:,1], c=c)
                    plt.plot(vector.xy[:,0], vector.xy[:,1])
            
        return fig, ax    
    
       
    def recalculateCycles(self, peakDist = 2, peakWidth = None, peakProminence = None):
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
        self.setReversalIndexes(peakDist, peakWidth, peakProminence)
        self.setCycles()
        self.setArea()    

    def RemoveCycles():
        pass

class SimpleCycle(CurveBase):
    """ A curve that doesn't change direction on the X axis, but can change
    Y direction.
    """
    
    def __init__(self, XYData, FindPeaks = False, setSlope = False, setArea = False,
                 peakDist = 2, peakWidth = None, peakProminence = None):
        CurveBase.__init__(self, XYData)
        
        self._setDirection()
            
        if setArea == True:
            self.setArea()       
        
        if FindPeaks == True:
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
                       
        self.SubCycles = SubCycles
        self.NsubCycles = len(SubCycles)
        
        
    def setSubCyclesArea(self):
        """
        Sets the net area for all SubCycles
        """
        try:
            SubCycles = self.SubCycles
        except:
            raise Exception('No SubCycles not yet set')
            
        for subCycle in SubCycles:
            subCycle._setNetArea        

    def setSubCyclesSlope(self):
        """
        Sets the net area for all MonotonicCurves
        """
        try:
            SubCycles = self.SubCycles
        except:
            raise Exception('SubCycles not yet set')
            
        for SubCycle in SubCycles:
            SubCycle.setSlope()       
      
    def getSubCycles(self, Indicies):
        SubCycles = [self.SubCycles[index] for index in Indicies]
        return SubCycles      
    
    def getSubCycle(self, Index):
        return self.SubCycles[Index]
     
    def plotSubCycles(self, SubCyclesIndicies = [], plotCycles = False, plotPeaks = False, 
                   xlim = [], ylim = []):
        
        xyMono = self.xy
        Vectors = self.SubCycles
        fig, ax = initializeFig(xlim, ylim)
        
        defaultShowCycles(self, xyMono[:,0], xyMono[:,1], plotCycles, plotPeaks)
        
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
            
        return fig, ax    
            
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
            
            
            

def concatenateHys(*argv):
    """
    This function creates a hystesis from a series of monotonic curves, or xy 
    curves   
    
    # TODO: enhance hysteresis functionality
    I would expect that the new curve has all the propreties of the old curves.
    Here that won't be the case, which is akward.
    

    Parameters
    ----------
    *argv : SimpleCycle objects, or XY data
        A number of monotonic cycle objects to be combined into a hysteresis.
        These curves should be 

    Returns
    -------
    hysteresis : Hysteresis Object
        DESCRIPTION.

    """
    
    
    
    xyList = [None]*len(argv)   
           
    for ii, vector in enumerate(argv):
        # Try to read the xy data from a monotonic curve object
        try:
            tempxy = vector.xy
        except:
            tempxy = vector
            
        # for curves after the first curve, we skip the first value
        # I think we want to do this for all curves?
        if ii >= 1:
            xyList[ii] = tempxy[1:,:]
        else:
            xyList[ii] = tempxy
    
    # Create new hysteresis, then add objects to the list    
    xy = np.concatenate(xyList)
    hysteresis = Hysteresis(xy)
    
    return hysteresis
        


def _LinInterpolate(x,y, Nsamples):
    f = interp1d(x, y)
    
    outputx = np.linspace(x[0],x[-1], Nsamples)
    outputy = f(outputx)
    outputxy = np.column_stack((outputx, outputy))    
    return outputxy

def reSample(Curve, Nsamples):
    """
    Creates a new Hysteresis or Monotonic Curve object that has a different 
    number of sample points. 
    
    Linear interpolation is used for intermediate points

    Parameters
    ----------
    Curve : Hysteresis, Monotonic Cycle, or numpy array
        DESCRIPTION.

    Returns
    -------
    TYPE
        An object of the input type.

    """  
        
    # if the curve is a SimpleCycle
    if isinstance(Curve, SimpleCycle):
    
        x = Curve.xy[:,0]
        y = Curve.xy[:,1]
        Output = SimpleCycle(_LinInterpolate(x,y, Nsamples))    
       
    # if the curve is a hysteresis, we recursively create a series of monotonic
    # Objects
    elif isinstance(Curve, Hysteresis):
        outputCycles = [None]*Curve.NCycles
        for ii, Cycle in enumerate(Curve.Cycles):
            outputCycles[ii] = reSample(Cycle, Nsamples)
        Output = concatenateHys(*outputCycles)    # If Curve

    # if the curve is a Monotonic Cycle
    elif isinstance(Curve, MonotonicCurve):
    
        x = Curve.xy[:,0]
        y = Curve.xy[:,1]
        
        Output = MonotonicCurve(_LinInterpolate(x,y, Nsamples))  
    
    # if it is a np array
    elif isinstance(Curve, np.ndarray):
        x = Curve[:,0]
        y = Curve[:,1]
        Output = _LinInterpolate(x,y, Nsamples)  
        
    return Output


def _getNsamples(Targetdx, dxNet):
    if Targetdx >= abs(dxNet/2):
        print('Targetdx is larger than dxNet/2, no intermediate points made for the target dx = ' +str(dxNet))
        Nsamples = 2
    else:
        Nsamples = int(round(abs(dxNet/Targetdx))) + 1
    return Nsamples
    
def reSampledx(Curve, Targetdx):


    if isinstance(Curve, SimpleCycle):
        x = Curve.xy[:,0]
        dxNet = x[-1] - x[0]
        
        Nsamples = _getNsamples(Targetdx, dxNet)
        
        Output = reSample(Curve, Nsamples)    
        
        
    elif isinstance(Curve, Hysteresis):

        outputCycles = [None]*Curve.NCycles
        for ii, Cycle in enumerate(Curve.Cycles):
            outputCycles[ii] = reSampledx(Cycle, Targetdx)
        Output = concatenateHys(*outputCycles)    # If Curve
       
    # if the curve is a MonotonicCurve Cycle
    elif isinstance(Curve, MonotonicCurve):
    
        x = Curve.xy[:,0]
        dxNet = x[-1] - x[0]
        
        Nsamples = _getNsamples(Targetdx, dxNet)
        
        Output = reSample(Curve, Nsamples)  
    
    # if it is a np array
    elif isinstance(Curve, np.ndarray):
        x = Curve[:,0]
        dxNet = x[-1] - x[0]
        
        Nsamples = _getNsamples(Targetdx, dxNet)        
        Output = reSample(Curve, Nsamples)
        
    return Output


# =============================================================================
# Compare
# =============================================================================


def defaultSampleFunction(xy1, xy2):
    
    # The average euler sum for each point
    
    x1 = xy1[:,0]
    x2 = xy2[:,0]
    y1 = xy1[:,1]
    y2 = xy2[:,1]
    
    diff = ((x1 - x2)**2 + (y1 - y2)**2)**(0.5)
    
    return np.sum(diff)/len(x1)

def defaultCombineDiff(diffs):
    
    # The average difference for each curve
    diffNet = np.sum(diffs)/len(diffs)
    
    return diffNet

def CompareCycle(Curve1, Curve2):
    
    if Curve1.Npoints != Curve1.Npoints:
        raise Exception("Curves don't have a similar number of points.")
    
    xy1 = Curve1.xy
    xy2 = Curve2.xy
    
    diff = defaultSampleFunction(xy1, xy2)

    return diff


def CompareHys(Hys1, Hys2):
    
    if Hys1.NCycles != Hys2.NCycles:
        raise Exception("Hysteresis don't have a similar number of Cycles.")    
    # Check both hystesis have the same number of reversals
    
    Cycles1 = Hys1.Cycles
    Cycles2 = Hys2.Cycles
    
    NCycles = Hys1.NCycles
    
    CycleDiffs = [None]*NCycles
    for ii in range(NCycles):
        CycleDiffs[ii]= CompareCycle(Cycles1[ii], Cycles2[ii])
        
    netdiff = defaultCombineDiff(CycleDiffs)

    return netdiff, CycleDiffs
    
