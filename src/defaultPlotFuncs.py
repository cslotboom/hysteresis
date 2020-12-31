import numpy as np
import matplotlib.pyplot as plt


def initializeFig(xlim, ylim):


    fig, ax = plt.subplots()

    if len(xlim) != 0 :
        ax.set_xlim(xlim[0], xlim[1])

    if len(ylim) != 0 :
        ax.set_ylim(ylim[0], ylim[1])
               
    return fig, ax

def defaultShowCycles(self, x, y, plotCycles, plotPeaks, labelCycles = [], Cycles = []):
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
            reversalIndexes = self.reversalIndexes        
        except:
            raise Exception("Object has no Cycles to display. Try setting cycles.")
        # TODO: update marker based on direction?
        
        # if only certain cycles have been asked for we remove all indexes other indexes
        if Cycles != []:
            markerIndexes = reversalIndexes[Cycles]
            # only label Cycles that are in the cycles asked for
            labelCycles = np.array([label for label in labelCycles if label in Cycles])
        else:
            # Otherwise we plot all
            markerIndexes = reversalIndexes
        
        # Indexes = Indexes[]
        markerX = x[markerIndexes]
        markerY = y[markerIndexes]         

        # Plot the desired indexes
        line2  = plt.plot(markerX, markerY, "x")        

        # If the cycles need to be labeled,
        # if labelCycles is 'all':
        if labelCycles == 'all':
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
            
            
            # Annotate = plt.annotate(int(ii), xy=(ReversalX[ii], ReversalY[ii]),xytext=(-10, 10), arrowprops=dict(arrowstyle="->"))
            # Annotate = plt.annotate(int(Cycle), xy=(ReversalX[ii], ReversalY[ii]), xytext=(-1, 5), textcoords = 'offset points', fontsize=12)
            # Annotate = plt.annotate(int(ii), xy=(ReversalX[ii], ReversalY[ii]))

def defaultPlotFunction(self, x, y, plotCycles, plotPeaks, xlim = [], ylim = [], labelCycles = []):
    #TODO: right now it is not possible to have overlap between functions using this method
    fig, ax = initializeFig(xlim, ylim)
          
    line1 = plt.plot(x, y)
       
    defaultShowCycles(self, x, y, plotCycles, plotPeaks, labelCycles)

    return fig, ax



    

