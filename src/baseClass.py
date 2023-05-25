import numpy as np
from hysteresis import data
import hysteresis.env as env
import matplotlib.pyplot as plt



class CurvePlotter:
    def plot(self, plotCycles = False, plotPeaks = False, labelCycles = [],
             **kwargs):
        """
        Used the plot function to make a xy plot of the curve. The default 
        plot function uses matplotlib for plotting, and returns the plotted
        line.
        
        Parameters
        ----------
        plotCycles : bool
            A switch that specifics if cycle reversal points should be plotted.
        plotPeaks : bool
            A switch that specifics if the detected peak values should be plotted.
        labelCycles : list or 'all', optional
            A list of the cycles to be labled. 
            A value of 'all' can also be specified, in which case all cucles will be plotted.
            The default is [], which labels no cycles    
        kwargs : list, optional
            Any additional keyword arguements will be passed to the matplotlib
            plot function. This can be used to custize char appearance.            

        Outputs
        -------
        Matplotlib Line

        """        
        x = self.xy[:,0]
        y = self.xy[:,1]
                    
        return self.plotFunction(self, x ,y, plotCycles, plotPeaks, labelCycles,
                                 **kwargs)
                
    def plotVsIndex(self, plotCycles = False, plotPeaks = False, 
                     labelCycles = [], **kwargs):
        """
        Used the plot function to make a plot of each x point vs. it's index.
        This can be useful for understanding how x values change over time.
        The default plot function uses matplotlib for plotting, and returns 
        the plotted line.
        
        Parameters
        ----------
        plotCycles : bool
            A switch that specifics if cycle reversal points should be plotted.
        plotPeaks : bool
            A switch that specifics if the detected peak values should be plotted.

        labelCycles : list or 'all', optional
            A list of the cycles to be labled. 
            A value of 'all' can also be specified, in which case all cucles will be plotted.
            The default is [], which labels no cycles     
        kwargs : list, optional
            Any additional keyword arguements will be passed to the matplotlib
            plot function. This can be used to custize char appearance.
            
        """           
        
        x = np.arange(0,len(self.xy[:,0]))
        y = self.xy[:,0]
                    
        return self.plotFunction(self, x ,y, plotCycles, plotPeaks, labelCycles, **kwargs)

    def plotLoadProtocol(self, comparisonProtocol = [], **kwargs):
        """
        Plots the peak x values for each cycle in a curve.
        An additional load protocol can be provided, so the user can comapare the
        curves peak x points against an expected load protocol.
        
        The default plot function uses matplotlib for plotting, and returns 
        the plotted line.
        
        Parameters
        ----------
        comparisonProtocol : array
            A load protocol that will be plotted on the same figure. Useful
            for comparing the curves load protcol to the input protocol.
        kwargs : list, optional
            Any additional keyword arguements will be passed to the matplotlib
            plot function. This can be used to custize char appearance.
        """           
        plotCycles = False
        plotPeaks = False
        labelCycles = []
        y = self.loadProtocol
        x = np.arange(0,len(y))
                
        line = self.plotFunction(self, x ,y, plotCycles, plotPeaks, labelCycles, **kwargs)
        
        if len(comparisonProtocol) != 0:
            line2 = plt.plot(comparisonProtocol)
            return [line, line2]

        return line
    
    def plotSlope(self,  plotCycles = False, plotPeaks = False, 
                  labelCycles = [], **kwargs):
        """
        Used the plot function to make a xy plot of the slope at each point of 
        the curve. The slope is calcualted using the slope function, which
        uses a centeral finite difference scheme by default.
        plot function uses matplotlib for plotting, and returns the plotted
        line.
        
        Parameters
        ----------
        plotCycles : bool
            A switch that specifics if cycle reversal points should be plotted.
        plotPeaks : bool
            A switch that specifics if the detected peak values should be plotted.

        labelCycles : list or 'all', optional
            A list of the cycles to be labled. 
            A value of 'all' can also be specified, in which case all cucles will be plotted.
            The default is [], which labels no cycles  
        kwargs : list, optional
            Any additional keyword arguements will be passed to the matplotlib
            plot function. This can be used to custize char appearance.
        """          
        
        x = self.xy[:,0]
        y = self.slope

        return self.plotFunction(self, x ,y, plotCycles, plotPeaks, labelCycles, **kwargs)
                
    def plotArea(self,  plotCycles = False, plotPeaks = False, labelCycles = [], **kwargs):
        """
        Used the plot function to make a xy plot of the area under each point of 
        the curve. The area is calculated using the area function, which
        uses the midpoint rule by default.
        The plot function uses matplotlib for plotting, and returns the plotted
        line.
        
        Parameters
        ----------
        plotCycles : bool
            A switch that specifics if cycle reversal points should be plotted.
        plotPeaks : bool
            A switch that specifics if the detected peak values should be plotted.

        labelCycles : list or 'all', optional
            A list of the cycles to be labled. 
            A value of 'all' can also be specified, in which case all cucles will be plotted.
            The default is [], which labels no cycles
        kwargs : list, optional
            Any additional keyword arguements will be passed to the matplotlib
            plot function. This can be used to custize char appearance.            
            
        """       
        
        x = self.xy[:,0]
        y = self.area

        return self.plotFunction(self, x ,y, plotCycles, plotPeaks, labelCycles, **kwargs)  
                        
    def plotCumArea(self,  plotCycles = False, plotPeaks = False, labelCycles = [], 
                    cumulativeDisp = True, **kwargs):
        """
        Used the plot function to make a xy plot of cumulative area at each
        point of the curve. The cumulative area is a summation of the areas up
        to the point in question.
        The area is calculated using the area function, which uses the midpoint 
        rule by default.
        The plot function uses matplotlib for plotting, and returns the plotted
        line.
        
        Parameters
        ----------
        plotCycles : bool
            A switch that specifics if cycle reversal points should be plotted.
        plotPeaks : bool
            A switch that specifics if the detected peak values should be plotted.
        labelCycles : list or 'all', optional
            A list of the cycles to be labled. 
            A value of 'all' can also be specified, in which case all cucles will be plotted.
            The default is [], which labels no cycles
        kwargs : list, optional
            Any additional keyword arguements will be passed to the matplotlib
            plot function. This can be used to custize char appearance.
        
        """   
        
        # We get the cumulative displacement and area
        if cumulativeDisp:
            x = self.getCumDisp()
        else:
            x = self.xy[:,0]
        y = self.getCumArea()

        self.plotFunction(self, x ,y, plotCycles, plotPeaks, labelCycles, **kwargs)  
             
    def initFig(self, xlims = [], ylims = []):
        """       
        Initializes the plot using the default rules.
        """        
        
        return self.initializeFig(xlims, ylims)



class CurveOperations:   
    
    @property
    def y(self):
        return self.xy[:,1]
    
    @property
    def x(self):
        return self.xy[:,0]    
    
    def _parseXY(self, xy):
        if isinstance(xy, list):
            xy = np.column_stack(xy)
        return xy
    
    def __len__(self):
        return len(self.xy[:,0])

    def __iter__(self):
        return iter(self.xy)
    
    def __getitem__(self, ind):
        return self.xy[ind]
    
    def __setitem__(self, ind, val):
        self.xy[ind] = val

    def _getInstance(self):
        return type(self)
    
    def _convertToCurve(self, other):
        """
        Converts non-hysteresis datatypes 
        """
        if isinstance(other, np.ndarray):
            return Curve(other)

    def __add__(self, other):
        """ Enables addition of curve x values"""
        Instance = self._getInstance()
        operand = _getOperand(other)
        x = self.xy[:,0]
        y = self.xy[:,1]+operand        
        
        return Instance(np.column_stack([x,y]))
    
    def __sub__(self, other):
        Instance = self._getInstance()
        operand = _getOperand(other)
        x = self.xy[:,0]
        y = self.xy[:,1] - operand        
        
        return Instance(np.column_stack([x,y]))
    
    def __rsub__(self, other):
        Instance = self._getInstance()
        operand = _getOperand(other)
        x = self.xy[:,0]
        y = operand - self.xy[:,1]   
        
        return Instance(np.column_stack([x,y]))

    def __neg__(self):
        Instance = self._getInstance()
        x =  self.xy[:,0]
        y = -self.xy[:,1]           
        return Instance(np.column_stack([x,y]))
    
    def __mul__(self, other):
        """
        It would be useful of having a hystresis base state, then copying that over.
        """
        # Get the current instance of curve
        Instance = self._getInstance()
        operand = _getOperand(other)
        x = self.xy[:,0]
        y = self.xy[:,1]*operand
        
        return Instance(np.column_stack([x,y]))

    def __truediv__(self, other):
        # Get the current instance of curve
        Instance = self._getInstance()
        operand = _getOperand(other)
        x = self.xy[:,0]
        y = self.xy[:,1] / operand
        
        return Instance(np.column_stack([x,y]))

    def __rtruediv__(self, other):
        # Get the current instance of curve
        Instance = self._getInstance()
        operand = _getOperand(other)    
        x = self.xy[:,0]
        y = operand / self.xy[:,1]
        
        return Instance(np.column_stack([x,y]))

class Curve(CurveOperations, CurvePlotter):
    
    """
    The curve base object represents a generic xy curve with no limitations.
    
    All other curves inherit from the CurveBase class. It has access to methods
    all other curves should have access to. This uncludes plotting 
    functionality, slope functions, area functions, and displacement functions.
    
    """
    __array_ufunc__ = None
    
    colorCycles = ['C0', 'C0', 'C1', 'C1']
    def __init__(self, XYData, xunit = '', yunit = ''):
        """
        Parameters
        ----------
        XYData : array
            The input array of XY date for the curve. A list [x,y] can also be 
            passed into the function.
        xunit : str, optional
            The units on the x axis. The default is ''.
        yunit : str, optional
            The units on the y axis. The default is ''.

        """
        
        self.xy = self._parseXY(XYData)
        self.Npoints = len(self.xy[:,0])
        
        # The function to be used to calcualte area. These can be overwritten
        self.areaFunction = env.environment.fArea
        self.slopeFunction = env.environment.fslope
        self.lengthFunction = env.environment.flength
        self.plotFunction = env.environment.fplot
        
        self.initializeFig = env.environment.finit
        self.showCycles = env.environment.fcycles
        
        self.xunit = xunit
        self.yunit = yunit
        
        self.peakIndexes = None
        
    def setArea(self):
        """ sets the area under each point of the curve using the area function"""
        self.area = self.areaFunction(self.xy)
        return self.area
    
    def getCumDisp(self):
        """ 
        Gets the absolute value of cumulative displacement of the curve at each data point.
        """
        dx = np.diff(self.xy[:,0])
        return np.append(0, np.cumsum(np.abs(dx)))
    
    def getNetCumDisp(self, startIndex = 0, endIndex = 0):
        """ Gets the total cumulative displacement between the start and start and end 
        indexes. By default the whole curve us used.
        """
        dx = np.append(0, np.diff(self.xy[:,0]))
        
        if endIndex == 0:
            endIndex = self.Npoints
                   
        return np.sum(np.abs(dx[startIndex:endIndex]))
    
    def getCumArea(self):
        """ 
        Gets the cumulative area under the curve for the entire curve.
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
        
        By default, uses the basic slope funciton. Custom behaviour can be
        specified by modifying the environment slope function.        
        """
        
        # Calculate end point slope
        xy = self.xy
        self.slope  = self.slopeFunction(xy)

    def setLength(self):
        """
        Calcuates the length of the curve, that is, the distance from each 
        point to the next point. 
        Starts at point 0, and ther are there are N-1 length values for the N 
        data points.
        
        By default, uses the basic length funciton. Custom behaviour can be
        specified by modifying the environment length function.

        """
        
        # Calculate end point slope
        xy = self.xy
        self.length  = self.lengthFunction(xy)

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
            
    def getPeakxy(self,):
        
        if self.peakIndexes is not None:
            return self.xy[self.peakIndexes]
        else:
            raise Exception('No peaks have been set')
        
    

def _getOperand(curve):
    """
    Gets the operand (what data the function acts on) for operation functions
    (+,-,*,/)
    The data used in these functions depends on the input given.
    
    """
    if not hasattr(curve, '__len__'): # assume scalar if no length
        operand = curve
    elif hasattr(curve, 'xy'): # use the xy if it's a curve from the hysteresis module.
        operand = curve.xy[:,1]
    elif isinstance(curve, np.ndarray): # If a numpy array, do stuff depending on array dimension.
        if 1 == len(curve.shape):
            operand = curve
        elif 2 == len(curve.shape) and curve.shape[-1] == 2: # if 2D array
            operand = curve[:,1]
        else: # if 1D array
            raise Exception(f'{curve.shape[-1]}D curve give, only 1 or 2D supported')
    return operand

class Hysteresis(Curve):
    """
    Hysteresis objects are those that have at least one reversal point in 
    their data. Reversal points are those where the x axis changes direction.
    
    The hysteresis object has a number of functions that help find the reversal
    points in the x data of the curve.
    
    The hysteresis object also stores each each half-cycle (where there is no
    change in direction) as a SimpleCycle object.
    
    
    Parameters
    ----------
    XYData : array
        The input array of XY date for the curve. A list [x,y] can also be 
        passed into the function.
    revDist : int, optional
        Used to filter reversal points based on the minimal horizontal distance 
        (>= 1) between neighbouring peaks in the x axis. Smaller peaks are 
        removed first until the condition is fulfilled for all remaining peaks.
        The default is 2.
    revWidth : int, optional
        Used to filter reversal points using the approximate width in number of 
        samples of each peak at half it's prominence. Peaks that occur very 
        abruptly have a small width, while those that occur gradually have 
        a big width.
        The default is None, which results in no filtering.  
    revProminence : number, optional
        Used to filter reversal points that aren't sufficently high. Prominence 
        is the desired difference in height between peaks and their 
        neighbouring peaks. 
        The default is None, which results in no filtering.     
    setCycles : Boolean, optional
        Used to turn on or off setting the cycle revesal points. 
        Can be turned off for performance reasons.
    setArea : Boolean, optional
        Used to turn on or off setting the Area by default. 
        Can be turned off for performance reasons.
    setSlope : Boolean, optional
        Used to turn on or off setting the slopeby default. 
        Can be turned off for performance reasons.    
        
    """
    
    def __init__(self, XYData, revDist = 2, revWidth = None, revProminence = None,
                 setCycles = True, setArea = True, setSlope = True, **kwargs):
 
        Curve.__init__(self, XYData, **kwargs)
        # self.setReversalPropreties(revDist, revWidth, revProminence)
        self._setStatePropreties(revDist, revWidth, revProminence,
                                 setCycles, setArea, setSlope)
        
        #TODO Create warning if cycles don't make sense.
        self.cycles:list[SimpleCycle] = None
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
    
    def _setStatePropreties(self, revDist, revWidth, revProminence,
                                 setCycles, setArea, setSlope):
        """
        Sets the propreties that are used to caculate where reversal points occur.
        These are used if we want to copy new classes using the same parameters.
        """
        self.revDist = revDist
        self.revWidth = revWidth
        self.revProminence = revProminence           
        
        self._setCycles = setCycles
        self._setArea = setArea
        self._setSlope = setSlope   
        
    def _getStatePropreties(self):
        """
        Sets the propreties that are used to caculate where reversal points occur.
        These are used if we want to copy new classes using the same parameters.
        """
        
        return [self.revDist, self.revWidth, self.revProminence,
                self._setCycles, self._setArea, self._setSlope]
        
        
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

    def plotCycle(self, Index, plotPeaks = False, **kwargs):
        
        """
        Plots the xy values of a single cycle.
        
        Parameters
        ----------
        Index : int
            The cycle to be plotted.
        plotPeaks : bool
            A switch that specifics if the detected peak values should be plotted.
        kwargs : list, optional
            Any additional keyword arguements will be passed to the matplotlib
            plot function. This can be used to custize char appearance.            
        """
        
        Cycle = self.cycles[Index]
        return Cycle.plot(plotPeaks = plotPeaks, **kwargs)

    def plotCycles(self, cycleIndexes = [], plotCycles = False, plotPeaks = False, 
                    labelCycles = [], colorCycles:list=None, **kwargs):
        """
        Plots the xy values of a several cycles on the same figure.
        If no list is provided, every cycle will be plotted.
        
        Parameters
        ----------
        cycleIndexes : list of int
            A list of the cycles to be plotted.
        plotCycles : bool
            A switch that specifics if cycle reversal points should be plotted.            
        plotPeaks : bool
            A switch that specifics if the detected peak values should be plotted.
        kwargs : list, optional
            Any additional keyword arguements will be passed to the matplotlib
            plot function. This can be used to custize char appearance.            
        """        
        
        xyHys = self.xy
        Vectors = self.cycles
        
        if not colorCycles:
            colorCycles = self.colorCycles
        Ncolor = len(colorCycles)
        
        self.showCycles(self, xyHys[:,0], xyHys[:,1], plotCycles, plotPeaks, labelCycles, cycleIndexes)
                
        lines = []
        # If the list is empty, plot everything
        if len(cycleIndexes) == 0:
            Vectors = self.cycles
        else:
            Vectors = [self.cycles[ii] for ii in cycleIndexes]
            # np.array(self.cycles, dtype=object)[cycleIndexes]
        
        for ii, vector in enumerate(Vectors):
            c = colorCycles[int(ii % Ncolor)]
            line, = plt.plot(vector.xy[:,0], vector.xy[:,1], c=c, **kwargs)
            lines.append(line)
        

    def recalculateCycles(self, revDist = 2, revWidth = None, revProminence = None, **kwargs):
        """
        Calcualtes the cycles again, using the input parameters for distance 
        (number of indexes), width (distance on the x axis), and prominence
        (distance in the y axis).
        
        Peaks are calculated using scipy's find_peaks function.
        
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
        Recalulates the cycles of one hysteresis using another the reversal
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
        
    def recalculateCycles_dist(self, revDist = 2, revWidth = None, 
                               revProminence = None, **kwargs):
        """
        Calcualtes the cycles again, using the input parameters for distance 
        (number of indexes), width (distance on the x axis), and prominence
        (distance in the y axis).
        
        The instead of the xy curve, the secant length between each point on 
        the curve is used to find revesal indexes. 
        Peaks are calculated using scipy's find_peaks function.
        
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
        
        
        try:
            dxy = self.length
        except:
            raise Exception('Length not set yet, set length using .setLength')
                        
        self.reversalIndexes = data.getMaxIndicies(dxy, revDist, revWidth, revProminence)
        self.loadProtocol = self.xy[self.reversalIndexes,0]
        
        self.setCycles()
        self.setArea()           

    def RemoveCycles():
        pass

# TODO: change name to CycleCurve?
class SimpleCycle(Curve):
    """ 
    A simple cycle is a curve that doesn't change direction on the X axis, but 
    can change direction in it's Y wzis. The data has a number of peaks, each 
    of which is the largest y value in relation to other points on the curve. 
    This point canbe 
    
    
    Parameters
    ----------
    XYData : array
        The input array of XY date for the curve. A list [x,y] can also be 
        passed into the function.
    peakDist : int, optional
        Used to filter peaks based on the minimal horizontal distance in number 
        of samples (>= 1) between neighbouring peaks in the y axis. 
        Smaller peaks are removed first until the condition is fulfilled for 
        all remaining peaks.
        The default is 2.
    peakWidth : int, optional
        Used to filter peaks points using the approximate width in number of 
        samples of each peak at half it's prominence. Peaks that occur very 
        abruptly have a small width, while those that occur gradually have 
        a big width.
        The default is None, which results in no filtering.  
    peakProminence : number, optional
        Used to filter peaks points that aren't sufficently high. Prominence 
        is the desired difference in height between peaks and their 
        neighbouring peaks. 
        The default is None, which results in no filtering.        
    findPeaks : Boolean, optional
        Used to turn on or off setting the cycle peak points. 
        Can be turned off for performance reasons.
    setArea : Boolean, optional
        Used to turn on or off setting the Area by default. 
        Can be turned off for performance reasons.
    setSlope : Boolean, optional
        Used to turn on or off setting the slopeby default. 
        Can be turned off for performance reasons.   
    
    """
    
    def __init__(self, XYData, findPeaks = False, setSlope = False, setArea = False,
                 peakDist = 2, peakWidth = None, peakProminence = None, **kwargs):
        Curve.__init__(self, XYData, **kwargs)
        
        self._setDirection()
        self._setStatePropreties(findPeaks, setSlope, setArea, 
                                 peakDist, peakWidth, peakProminence)
               
        self.subCycles = None
        if findPeaks == True:
            self.setPeaks()
            self.setSubCycles()
    
        if setSlope == True:
            self.setSlope()
        if setArea == True:
            self.setArea()      

    
    def _setStatePropreties(self, findPeaks, setSlope, setArea, 
                                  peakDist, peakWidth, peakProminence):
        """
        Sets the varabiles that are used to caculate what propreties of the curve
        are run. Used when copying the simple cycle object
        """
        self._findPeaks = findPeaks
        self._setSlope = setSlope
        self._setArea = setArea
        
        self.peakDist = peakDist
        self.peakWidth = peakWidth
        self.peakProminence = peakProminence        

    def _getStatePropreties(self):
        """
        Sets the propreties that are used to caculate where reversal points occur.
        These are used if we want to copy new classes using the same parameters.
        """
        return [self._findPeaks,self._setSlope,self._setArea,
                self.peakDist, self.peakWidth, self.peakProminence]



    def _setDirection(self):
        """
         1 = left to right. -1 = to is right to left

        """
        xdata = self.xy[:,0]
        if xdata[0] <= xdata[-1]:
            self.direction =  1
        else:
            self.direction = -1
           
                
    def setSubCycles(self, peakDist = 2, peakWidth = None, peakProminence = None):
        """
        Finds monotonic "sub-sycles" within each cycle.
        Peaks must be set before subcyles can be set.

        """

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
        Sets the net area for all SubCycles.
        """
        try:
            SubCycles = self.subCycles
        except:
            raise Exception('No SubCycles not yet set')
            
        for subCycle in SubCycles:
            subCycle._setNetArea        

    def setSubCyclesSlope(self):
        """
        Sets the net slope for all MonotonicCurves.
        """
        try:
            SubCycles = self.subCycles
        except:
            raise Exception('SubCycles not yet set')
            
        for SubCycle in SubCycles:
            SubCycle.setSlope()       
      
    def getSubCycles(self, indicies):
        """
        returns a list of subcycles with the input indicies.

        Parameters
        ----------
        Index : list of int
            The integer index of the sub-cycle you want to return.

        Returns
        -------
        Subcycle
            The output subcycle.

        """        
        
        SubCycles = [self.subCycles[index] for index in indicies]
        return SubCycles      
    
    def getSubCycle(self, index):
        """
        Gets the subcycle with a partcular index.

        Parameters
        ----------
        Index : int
            The integer index of the sub-cycle you want to return.

        Returns
        -------
        Subcycle
            The output subcycle.

        """
        return self.subCycles[index]
    
    # TODO: update this, change name from subcycle to Monotonic curve.
    def plotSubCycles(self, SubCyclesIndicies = [], plotCycles = False, plotPeaks = False,
                      colorCycles:list = None):
        
        xyMono = self.xy
        Vectors = self.subCycles
        
        if not colorCycles:
            colorCycles = self.colorCycles
        Ncolor = len(colorCycles)        
        
        self.showCycles(self, xyMono[:,0], xyMono[:,1], plotCycles, plotPeaks)
        
        if len(SubCyclesIndicies) == 0:
            for ii, vector in enumerate(Vectors):
                c = colorCycles[ii%Ncolor]
                plt.plot(vector.xy[:,0], vector.xy[:,1], c = c)

        else:
            for ii, vector in enumerate(self.SimpleCycles):
                if ii in SubCyclesIndicies:
                    c = colorCycles[ii%Ncolor]
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

class MonotonicCurve(Curve):
    """
    A curve that has no changes in it's x axis direction, as well as no changes
    in it's y axis direction.
    """   
    def __init__(self, XYData, **kwargs):
        Curve.__init__(self, XYData, **kwargs)
        
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
    

