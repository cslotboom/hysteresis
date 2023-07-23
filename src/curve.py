import numpy as np
from hysteresis import data
import hysteresis.env as env
import matplotlib.pyplot as plt


class CurvePlotter:
    """
    The Curve plotter class is used to define plotting behaviour that is common 
    to all types of curves. It is generally ment to be inherited from and not
    used directly. 
    """
    
    
    def plot(self, showReversals = False, showPeaks = False, labelReversals = None,
             **kwargs):
        """
        Used the plot function to make a xy plot of the curve. The default 
        plot function uses matplotlib for plotting, and returns the plotted
        line.
        
        Parameters
        ----------
        showReversals : bool
            A switch that specifics if cycle reversal points should be plotted.
        showPeaks : bool
            A switch that specifics if the detected peak values should be plotted.
        labelReversals : list or 'all', optional
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
        
        if labelReversals is None:
            labelReversals = []

        return self.plotFunction(self.xy, showReversals, showPeaks, self.peakIndexes, 
                                 self.reversalIndexes, labelReversals,
                                 **kwargs)
                
    def plotVsIndex(self, showReversals = False, showPeaks = False, 
                     labelReversals = None, **kwargs):
        """
        Used the plot function to make a plot of each x point vs. it's index.
        This can be useful for understanding how x values change over time.
        The default plot function uses matplotlib for plotting, and returns 
        the plotted line.
        
        Parameters
        ----------
        showReversals : bool
            A switch that specifics if cycle reversal points should be plotted.
        showPeaks : bool
            A switch that specifics if the detected peak values should be plotted.
        labelReversals : list or 'all', optional
            A list of the cycles to be labled. 
            A value of 'all' can also be specified, in which case all cucles will be plotted.
            The default is [], which labels no cycles     
        kwargs : list, optional
            Any additional keyword arguements will be passed to the matplotlib
            plot function. This can be used to custize char appearance.
            
        """           
        
        if labelReversals is None:
            labelReversals = []
                
        x = np.arange(0,len(self.xy[:,0]))
        y = self.xy[:,0]
        
        xy = np.column_stack([x,y])
                    
        return self.plotFunction(xy, showReversals, showPeaks, self.peakIndexes, 
                                 self.reversalIndexes, labelReversals, **kwargs)

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
        showReversals = False
        showPeaks = False
        labelCycles = []
        y = self.loadProtocol
        x = np.arange(0,len(y))
        xy = np.column_stack([x,y])
        
        line = self.plotFunction(xy, showReversals, showPeaks, labelCycles, **kwargs)
        
        if len(comparisonProtocol) != 0:
            line2 = plt.plot(comparisonProtocol)
            return [line, line2]

        return line
    
    def plotSlope(self,  showReversals = False, showPeaks = False, 
                  labelReversals = None, **kwargs):
        """
        Used the plot function to make a xy plot of the slope at each point of 
        the curve. The slope is calcualted using the slope function, which
        uses a centeral finite difference scheme by default.
        plot function uses matplotlib for plotting, and returns the plotted
        line.
        
        Parameters
        ----------
        showReversals : bool
            A switch that specifics if cycle reversal points should be plotted.
        showPeaks : bool
            A switch that specifics if the detected peak values should be plotted.

        labelReversals : list or 'all', optional
            A list of the cycles to be labled. 
            A value of 'all' can also be specified, in which case all cucles will be plotted.
            The default is [], which labels no cycles  
        kwargs : list, optional
            Any additional keyword arguements will be passed to the matplotlib
            plot function. This can be used to custize char appearance.
        """          
        
        xy = np.column_stack([self.xy[:,0], self.slope])
        
        if labelReversals is None:
            labelReversals = []
    
        return self.plotFunction(xy, showReversals, showPeaks, self.peakIndexes, 
                                 self.reversalIndexes, labelReversals,
                                 **kwargs)    
    
    def plotArea(self,  showReversals = False, showPeaks = False, 
                 labelReversals = None, **kwargs):
        """
        Used the plot function to make a xy plot of the area under each point of 
        the curve. The area is calculated using the area function, which
        uses the midpoint rule by default.
        The plot function uses matplotlib for plotting, and returns the plotted
        line.
        
        Parameters
        ----------
        showReversals : bool
            A switch that specifics if cycle reversal points should be plotted.
        showPeaks : bool
            A switch that specifics if the detected peak values should be plotted.

        labelReversals : list or 'all', optional
            A list of the cycles to be labled. 
            A value of 'all' can also be specified, in which case all cucles 
            will be plotted.
            The default is [], which labels no cycles
        kwargs : list, optional
            Any additional keyword arguements will be passed to the matplotlib
            plot function. This can be used to custize char appearance.            
            
        """       
        
        if labelReversals is None:
            labelReversals = []
            
        xy = np.column_stack([self.xy[:,0], self.area])

        return self.plotFunction(xy, showReversals, showPeaks, self.peakIndexes, 
                                 self.reversalIndexes, labelReversals,
                                 **kwargs)    
                        
    def plotCumArea(self,  showReversals = False, showPeaks = False, 
                    labelReversals = None, cumulativeDisp = True, **kwargs):
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
        showReversals : bool
            A switch that specifics if cycle reversal points should be plotted.
        showPeaks : bool
            A switch that specifics if the detected peak values should be plotted.
        labelReversals : list or 'all', optional
            A list of the cycles to be labled. 
            A value of 'all' can also be specified, in which case all cucles will be plotted.
            The default is [], which labels no cycles
        kwargs : list, optional
            Any additional keyword arguements will be passed to the matplotlib
            plot function. This can be used to custize char appearance.
        
        """   
        
        if labelReversals is None:
            labelReversals = []
            
        # We get the cumulative displacement and area
        if cumulativeDisp:
            x = self.getCumDisp()
        else:
            x = self.xy[:,0]
        y = self.getCumArea()
        xy = np.column_stack([x,y])

        return self.plotFunction(xy, showReversals, showPeaks, self.peakIndexes, 
                                 self.reversalIndexes, labelReversals,
                                 **kwargs)    
             
    def initFig(self, xlims = None, ylims = None):
        """       
        Initializes the plot using the default rules.
        """
        
        if xlims is None:
            xlims = []
        
        if ylims is None:
            ylims = []
            
        return self.initializeFig(xlims, ylims)


    def _plot_curves(self, curves, curveInds, colorCycles, **kwargs):
        """
        Used by plotCycles and plotSubCycles
        """
        Ncolor = len(colorCycles) 
        lines = []
        # If the list has content, get the cycles to plot, otherwise plot everything
        if curveInds is not None:
            curves = [curves[ii] for ii in curveInds]
            
        for ii, curve in enumerate(curves):
            c = colorCycles[int(ii % Ncolor)]
            line, = plt.plot(curve.xy[:,0], curve.xy[:,1], c=c, **kwargs)
            lines.append(line)
        return lines     

class CurveOperations:
    
    """
    The Curve operations class is used to define operations that all curves
    will have. This includes features such iteration, mathematical operations
    like addition or multiplaction, and setting/getting items.
    """
    
    __array_ufunc__ = None

    
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
    
    colorCycles = ['C0', 'C0', 'C1', 'C1']
    reversalIndexes = np.array([0,-1])
    
    
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
        peakIndexes = data.getCycleIndexes(y, peakDist, peakWidth, peakProminence)        
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
        self.cycles:list[SimpleCurve] = None
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
        """ 
        Finds the location of the reversal points
        """
       
        self.setReversalPropreties(revDist, revWidth, revProminence)
        
        x = self.xy[:,0]
        self.reversalIndexes = data.getCycleIndexes(x, revDist, revWidth, revProminence)
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
            Cycles[ii] = SimpleCurve(xy[indices[ii]:(indices[ii+1]+1), :])
                       
        self.cycles:list[SimpleCurve] = Cycles
        self.NCycles = NIndex
        self.NCycles = len(Cycles)
    
    def getCycles(self, Indexes):
        """ Returns a list of cycles given a list of indexes"""
        Cycles = [self.cycles[index] for index in Indexes]
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

    def plotCycle(self, Index, showPeaks = False, **kwargs):
        
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
        return Cycle.plot(showPeaks = showPeaks, **kwargs)

    def plotCycles(self, cycleIndexes:list = None, showReversals = False, showPeaks = False, 
                    labelReversals:list = None, colorCycles:list = None, **kwargs):
        """
        Plots the xy values of a several cycles on the same figure.
        If no list is provided, every cycle will be plotted.
        
        Parameters
        ----------
        cycleIndexes : list of int
            A list of the cycles to be plotted. By default everything is plotted.
        showReversals : bool
            A switch that specifics if cycle reversal points should be plotted.            
        showPeaks : bool
            A switch that specifics if the detected peak values should be plotted.
        labelReversals : list of int, or 'all'
            A list of the integers which can be used to label certain reversal points
            on the graph. If no lis is provided then no reversal points are labeled.
            If 'all' is provided, then all points will be labeled
        colorCycles : list of str
            A list of matplotlib color labels to use for the cycle color. The cycles
            will follow the colours used, the wrap back to the start of the list if there
            are more cycles than entries provided in the color Cycles.            
        kwargs : list, optional
            Any additional keyword arguements will be passed to the matplotlib
            plot function. This can be used to custize char appearance.            
        """        
        
        xyHys = self.xy
        
        if not colorCycles:
            colorCycles = self.colorCycles
        
        self.showCycles(xyHys, showReversals, showPeaks, self.peakIndexes, 
                        self.reversalIndexes, labelReversals, cycleIndexes)
                    
        return self._plot_curves(self.cycles, cycleIndexes, colorCycles, **kwargs)
    
     
    

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
                        
        self.reversalIndexes = data.getMaxIndexes(dxy, revDist, revWidth, revProminence)
        self.loadProtocol = self.xy[self.reversalIndexes,0]
        
        self.setCycles()
        self.setArea()           

class SimpleCurve(Curve):
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
    
    colorCycles = ['C0', 'C1'] # applies to subcycles here
    
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
        if self.peakIndexes is None:
            self.setPeaks(peakDist, peakWidth, peakProminence)
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
      
    def getSubCycles(self, indexes):
        """
        returns a list of subcycles with the input indexes.

        Parameters
        ----------
        Index : list of int
            The integer index of the sub-cycle you want to return.

        Returns
        -------
        Subcycle
            The output subcycle.

        """        
        
        SubCycles = [self.subCycles[index] for index in indexes]
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
    
    def plotSubCycles(self, subCyclesIndexes:list = None, showReversals = False, showPeaks = False,
                      colorCycles:list = None, **kwargs):
        """
        Plots the xy values of a several subcycles on the same figure.
        If no list is provided, every subcycle will be plotted.
        
        Parameters
        ----------
        subCyclesIndexes : list of int
            A list of the subcycles to be plotted.
        showReversals : bool
            A switch that specifics if subcycle reversal points should be plotted.
            It's expected that there are no reveral points in each subcycles'            
        showPeaks : bool
            A switch that specifics if the detected peak values should be plotted.
            
        kwargs : list, optional
            Any additional keyword arguements will be passed to the matplotlib
            plot function. This can be used to custize char appearance.            
        """  
        
        xyMono = self.xy
        
        if not colorCycles:
            colorCycles = self.colorCycles
        
        self.showCycles(xyMono, showReversals, showPeaks, self.peakIndexes, 
                        self.reversalIndexes, None, subCyclesIndexes)
    
        return self._plot_curves(self.subCycles, subCyclesIndexes, colorCycles, **kwargs)
    
    
        
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



