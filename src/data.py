# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 15:13:13 2019
@author: Christian
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.interpolate import interp1d



def getCycleSubVector(VectorX, VectorY, Index1, Index2, Nsample):
    """
      
    
    This function takes a input x y curve, then returns a linearlized curve
    between two indicies
    
    

    Parameters
    ----------
    VectorX : Array
        The input X vector.
    VectorY : Array
        The input Y vector.
    Index1 : int
        The first index we want to calculate values between.
    Index2 : int
        The second index we want to calculate values between.
    Nsample : int
        The desired number of data points between the two vectors.

    Returns
    -------
    xSample : TYPE
        The x points of the sample curve.
    ySample : TYPE
        The y points of the sample curve.

    """
    #TODO consider renaming to interpolate subvector! Right now this samples
    # the vector by default    
    
    x1 = VectorX[Index1]
    x2 = VectorX[Index2]
    
    
    TempDataX = VectorX[Index1:(Index2+1)]
    TempDataY = VectorY[Index1:(Index2+1)]
    xSample = np.linspace(x1,x2,Nsample)
    
    InterpFunction = interp1d(TempDataX, TempDataY)
    ySample = InterpFunction(xSample)
          
    return xSample,ySample


def getMaxIndexes(VectorX, peakDist = 2, peakWidth = None, 
                     peakProminence = None, **kwargs):
    MaxIndexes,_ = find_peaks(VectorX, height = (None, None), distance = peakDist, 
                            width = peakWidth, prominence = peakProminence, **kwargs)

    Nindex = len(MaxIndexes) + 2
    Indexes = np.zeros(Nindex, dtype = int)
    Indexes[0] = 0
    Indexes[-1] = len(VectorX) - 1
    
    Indexes[1:-1] = MaxIndexes

    return Indexes




def _findOrder(L1, L2, MinIndexes, MaxIndexes):
    # We check the order, starting with the minimum number of possibilities
    # if there are no minimus, order doesn't matter
    # If the first index is a minimum, order = 1, otherwise order = 2
    if L1 == 0 and L2 == 0: # Edge case 1: Curve is monotonic - order doesn't matter
        order = 1
    elif L1 == 0: # Edge case 2: There are no intermediate min points and one intermediate max
        order = 2
    elif L2 == 0: # Edge case 3: There are no intermediate maxi points and one intermediate min
        order = 1
    elif MinIndexes[0] < MaxIndexes[0]: 
        order = 1
    else:
        order = 2
    return order



def getCycleIndexes(VectorX, peakDist = 2, peakWidth = None, 
                     peakProminence = None, **kwargs):
    """
    This function finds the index where there is areversal in the XY data. 
    You may need to adjust the find peaks factor to get satisfactory results.
    Built on the scipy find peaks funciton
    

    Parameters
    ----------
    VectorX : 1D array
        Input X Vector.
    VectorY : 1D array
        Input Y Vector. This is only used if we want to plot the values.
    CreatePlot : Boolean
        This switch specifies whether or not to display the output.plot
    peakDist : int, optional
        Required minimal horizontal distance (>= 1) in samples between
        neighbouring peaks. Smaller peaks are removed first until the condition
        is fulfilled for all remaining peaks.
        The default is 2.
    peakWidth : int, optional
        The approximate width in number of samples of the peak at half it's prominence.
        Peaks that occur very abruptly have a small width, while those that occur
        gradually have a big width.
    peakProminence : number, optional
        Used to filter out peaks that aren't sufficently high. Prominence is 
        the desired difference in height between peaks and their neighbouring peaks. 
        The default is None, which results in no filtering.

    Returns
    -------
    Indexes : Arrays
        Returns the arrays at which reversals occur.

    """
       
    # We find the intermediate peak values
    # We use height = 0 to select only positive or negative peaks.
    MaxIndexes,_ = find_peaks(VectorX, height = (None, None), distance = peakDist, 
    # MaxIndexes,_ = find_peaks(VectorX, height = (0, None), distance = peakDist, 
                            width = peakWidth, prominence = peakProminence)
    
    MinIndexes,_ = find_peaks(-VectorX, height = (None, None), distance = peakDist, 
                            width = peakWidth, prominence = peakProminence)    
        
    # We store define an array that will later be used to store the
    # the max and min values in an array of indexes
    Nindex = len(MaxIndexes) + len(MinIndexes) + 2
    Indexes = np.zeros(Nindex, dtype = int)
       
    # Define first and last point
    Indexes[0] = 0
    Indexes[-1] = len(VectorX) - 1
    
    # if only one point exists   
    L1 = len(MinIndexes)
    L2 = len(MaxIndexes)
    
    if abs(L1 - L2) > 1:
        raise Exception('There are', L1, 'minimums which is more than one than ', L2, ' maximums. There are likely repeated peaks.')
    
    # 1 means min first, 2 means max first
    order = _findOrder(L1, L2, MinIndexes, MaxIndexes)
    
    if order == 1:
        Indexes[1:-1:2] = MinIndexes
        if L2 !=0:
            Indexes[2:-1:2] = MaxIndexes
    else:
        Indexes[1:-1:2] = MaxIndexes
        if L1 !=0:
            Indexes[2:-1:2] = MinIndexes      
 
    
    return Indexes


def linearInterpolation(x1, x2, y1, y2, x):
    """
    A default linear interpolation functions for the value x between two points
    p1 = (x1,y1) and p2 = (x2,y2). 

    Parameters
    ----------
    x : float
        The input x value

    Returns
    -------
    y : float
        the output y value.

    """

    dx = (x2 - x1)
    if dx == 0:
        y = y1
    else:
        y = ((y2 - y1) / (dx))*(x - x1) + y1
    
    return y
   





def sampleData(ExperimentX, ExperimentY, AnalysisX, AnalysisY, Nsample = 10, 
               peakDist = 2, peakwidth = None, Norm = None):
    """
        
    This functions samples two data sets that undergo a cyclic, or monotonic 
    response. The function automatically detects reversals in the data. 
    Adjustments may be necessary to find peaks in the data 
    
    The Experiment and Analysis must have the same number of cycles

    Parameters
    ----------
    ExperimentX : Array
        The X values from the experiment dataset.
    ExperimentY : Array
        The Y values from the experiment dataset.
    AnalysisX : Array
        The X values from the analysis dataset.
    AnalysisY : Array
        The Y values from the analysis dataset.

    Raises
    ------
    Exception
        If the datasets don't have the same number of cycles, the sampling
        doesn't work

    Returns
    -------
    Rnet : float
        Returns a the sampled value 

    """
       
    # We get the indicies where the reversal happens.
    
    ExperimentIndicies = getCycleIndexes(ExperimentX, Nsample, peakDist, peakwidth, ExperimentY)
    AnalysisIndicies = getCycleIndexes(AnalysisX, Nsample, peakDist, peakwidth, AnalysisY)
    
    # We check that both curves have the same number of indicies
    NIndex = len(ExperimentIndicies) - 1
    NIndex_2 = len(AnalysisIndicies) - 1
    R= np.zeros(NIndex)
    
    # If they don't we create a error
    if NIndex!=NIndex_2:
        raise Exception('The experiment and Analysis have a different number of cycles')
        
    # For each index, we loop through 
    for ii in range(NIndex):
        # We get define the arrays for the x and y coordinants of the sub-vector
        Ex = np.zeros(NIndex)
        Ey = np.zeros(NIndex)
        Ax = np.zeros(NIndex)
        Ay = np.zeros(NIndex)
        
        # We get the subvector values between the indicies
        [Ex,Ey] = getCycleSubVector(ExperimentX , ExperimentY, ExperimentIndicies[ii], ExperimentIndicies[ii+1], Nsample)
        [Ax,Ay] = getCycleSubVector(AnalysisX , AnalysisY, AnalysisIndicies[ii], AnalysisIndicies[ii+1], Nsample)
        
        # We sample each point on the curve using the difference between the
        # two points
        if Norm == None:
            R[ii] = np.sum(((Ey-Ay)**2 + (Ex-Ax)**2)**0.5)
        else:
            R[ii] = Norm(Ex, Ey, Ay, Ax)
        
    Rnet = np.sum(R)
    
    return Rnet


def sampleMonotonicData(ExperimentX, ExperimentY, AnalysisX, AnalysisY,
                        Nsample = 10, Norm = None):
    """
    This functions works the same way as the cyclic data function
    
    This functions samples two data sets of data and returns a 
    
    The Experiment and Analysis must have the same number of cycles

    Parameters
    ----------
    ExperimentX : Array
        The X values from the experiment dataset.
    ExperimentY : Array
        The Y values from the experiment dataset.
    AnalysisX : Array
        The X values from the analysis dataset.
    AnalysisY : Array
        The Y values from the analysis dataset.

    Returns
    -------
    Rnet : float
        Returns a the sampled value 

    """
    
    Nindex = len(ExperimentX)
    R= np.zeros(Nsample)
    
    for ii in range(Nsample):
        Ex = np.zeros(Nsample)
        Ey = np.zeros(Nsample)
        Ax = np.zeros(Nsample)
        Ay = np.zeros(Nsample)
        
        
        [Ex,Ey] = getCycleSubVector(ExperimentX , ExperimentY, 0, Nindex, Nsample)
        [Ax,Ay] = getCycleSubVector(AnalysisX , AnalysisY, 0, Nindex, Nsample)
        
        R[ii] = np.sum(((Ey-Ay)**2 + (Ex-Ax)**2)**0.5)
        if Norm == None:
            R[ii] = np.sum(((Ey-Ay)**2 + (Ex-Ax)**2)**0.5)
        else:
            R[ii] = Norm(Ex, Ey, Ay, Ax)        
    Rnet = np.sum(R)
    
    return Rnet





# =============================================================================
# Unused and to be removed
# =============================================================================


def shiftDataFrame1(Samplex, Sampley, Targetx):
    """
    
    SciPy's ID interpolate baseically does what this does, it probably makes
    more sense to use that instead.
    
    This functions shifts x/y of a sample vector to a target x vector.
    Intermediate values are found using linearlizaton
    Both the input and putput data must be a function.
    
    The sample point MUST be within the bounds
    
              sample x/y data
              x1___x2____u1___x2_________x5_________x6
              y1___x2____x1___x2_________x5_________x6
    
              Targert x data
              x1_____x2___x3____x4___x5______x6__x7

    Returns:
              y1_____y2___y3____y4___y4______y5__y7
              
    # We will need to break if 
    Parameters
    ----------
    Samplex : Array 1d.
        The x values for the sample curves we want to shift into.
    Sampley : Array 1d.
        The y values for the sample curves we want to shift into.
    Targetx : Array 1d.
        The X vector we want to shift the target into.

    Returns
    -------
    Targety : Array 1d.
        The Y vector we shifted  the target into.

    """
    
        
    # 
    SampleRate = 1    
    
    # Get number of samples needed
    Nsamples = len(Targetx)
    Targety = np.zeros(Nsamples)
    
    MinData = np.min(Samplex)
    MaxData = np.max(Samplex)
    
    # Define indexes
    ii = 0
    jj = 1
    x1 = Samplex[0]
    y1 = Sampley[0]
    x2 = Samplex[jj]
    y2 = Sampley[jj]
    Currentmax = max(x1,x2)
    Currentmin = min(x1,x2)
    
    while (ii < Nsamples):
        
        #Get the target Point
        x = Targetx[ii]
        
        if x < MinData:
            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            print("Target is less than minimum bounds")
            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            #Targety = None
            break
        if x > MaxData:
            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            print("Target is greater than maximum bounds")
            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            #Targety = None
            break
        
        # We look to linearly interpolate between the two points
        
        # We check if x is within the range of the current sample points
        # if it isn't, we check the next data points
        while ((x < Currentmin) or (Currentmax < x)):
            jj += 1
            #print(jj)
            x1 = x2
            y1 = y2
            x2 = Samplex[jj]
            y2 = Sampley[jj]

            Currentmax = max(x1,x2)
            Currentmin = min(x1,x2)
               
        
        # Interpolate
        Targety[ii] = linearInterpolation(x1,x2,y1,y2,x)
        
        ii+=1
        
    return Targety


"""
TODO
    Consider removing ShiftDataFrame - I don't think this us used anymore
"""
