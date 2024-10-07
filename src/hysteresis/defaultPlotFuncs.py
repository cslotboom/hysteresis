import numpy as np
import matplotlib.pyplot as plt


def initializeFig(xlim = [], ylim= []):
    """
    A default function that initializes a figure based on a set of incoming
    x and y limits

    Parameters
    ----------
    xlim : list
        The x limits in [xmin, xmax].
    ylim : list
        The y limits in [xmin, xmax].

    """

    fig, ax = plt.subplots()

    if len(xlim) != 0 :
        ax.set_xlim(xlim[0], xlim[1])

    if len(ylim) != 0 :
        ax.set_ylim(ylim[0], ylim[1])
               
    return fig, ax

def defaultShowCycles(xy, showReversals, showPeaks, peakIndexes = None, 
                      reversalIndexes=None,  labelCycles = None, cycleIndicies = None):
    """
    A function that plots the location of the reversal points and peaks for a
    curve object.

    Parameters
    ----------
    x : array
        The input x values as an numpy array.
    y : array
        The input y values as an numpy array.
    plotCycles : bool
        A switch that specifics if cycle reversal points should be plotted.
    plotPeaks : bool
        A switch that specifics if peak values should be plotted.
    labelCycles : list or 'all', optional
        A list of the cycles to be labled. 
        A value of 'all' can also be specified, in which case all cucles will be plotted.
        The default is [], which labels no cycles
    Cycles : kist, optional
        A list of the cycles to be plotted. If not specified, all values will 
        be plotted. The default is NOne, which plots no labels cycles.

    """
    
    x = xy[:,0]
    y = xy[:,1]
    
    if labelCycles is None:
        labelCycles = []
    
    if cycleIndicies is None:
        cycleIndicies = []    
        
    # Plot cycles as x only
    if showPeaks == True:
        
        inds = peakIndexes
        if peakIndexes is None:
            raise Exception('No peaks have been set')
            
        PeakX = x[inds]
        PeakY = y[inds]

        line2  = plt.plot(PeakX, PeakY, "+")
        # plt.title('Peak Index y values')    # Plot cycles as x only
        
    if showReversals == True:
        
        if reversalIndexes is None:
            raise Exception('No peaks have been set')
        # TODO: update marker based on direction?
        
        # if only certain cycles have been asked for we remove all indexes other indexes
        if cycleIndicies != []:
            markerIndexes = reversalIndexes[cycleIndicies]
            # only label Cycles that are in the cycles asked for
            labelCycles = np.array([label for label in labelCycles if label in cycleIndicies])
        else:
            # Otherwise we plot all
            markerIndexes = reversalIndexes
        
        # Indexes = Indexes[]
        markerX = x[markerIndexes]
        markerY = y[markerIndexes]         

        # Plot the desired indexes
        line2  = plt.plot(markerX, markerY, "x")        

        # If the cycles need to be labeled,
        if str(labelCycles) == 'all':
            # skip the first and last cycles
            labelIndexes = np.arange(0,len(markerIndexes))
            labelX = x[reversalIndexes]
            labelY = y[reversalIndexes]
        else:
            labelIndexes = labelCycles
            labelX = x[reversalIndexes[labelCycles]]
            labelY = y[reversalIndexes[labelCycles]] 

            
        for ii in range(len(labelIndexes)):
            Annotate = plt.annotate(labelIndexes[ii], [labelX[ii],labelY[ii]], xytext=(-1, 5), textcoords = 'offset points')


def defaultPlotFunction(xy, showReversals, showPeaks, peakIndexes = None, 
                      reversalIndexes=None, labelCycles = None, **kwargs):
    """
    Parameters
    ----------
    xy : 2D array [Npoints, 2]
        The input x/y values as an numpy array, in order x,y and shape [Npoints, 2].
        e.g. x = xy[:,0]
    y : array
        The input y values as an numpy array.
    plotCycles : bool
        A switch that specifics if cycle reversal points should be plotted.
    plotPeaks : bool
        A switch that specifics if peak values should be plotted.
    labelCycles : list or 'all', optional
        A list of the cycles to be labled. 
        A value of 'all' can also be specified, in which case all cucles will be plotted.
        The default is [], which labels no cycles
    Cycles : kist, optional
        A list of the cycles to be plotted. If not specified, all values will 
        be plotted. The default is [], which plots all cycles.
    """
    
    x = xy[:,0]
    y = xy[:,1]
          
    line, = plt.plot(x, y, **kwargs)
       
    defaultShowCycles(xy, showReversals, showPeaks, peakIndexes, reversalIndexes, labelCycles)
    
    return line
    



    

