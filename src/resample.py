import numpy as np
from .curve import Hysteresis, SimpleCurve, MonotonicCurve
from .baseFuncs import (concatenateHys, concatenate, _linInterp, 
                        _linInterpSample, _getNsamples)
       
# =============================================================================
# concatenate and resample
# =============================================================================
           
def resample(curve, Nsamples, **kwargs):
    """
    Creates a new curve object that has a different number of sample points 
    between the start and end of each Cycle object.
    The curve resampled will be one level down, i.e. Hystereses will their
    simpleCycles resampled, and SimpleCycles will have their Monotonic Curves
    resampled
    
    The number of points is specified by the user, and intermediate points will
    be evenly spaced between the cycles start and end points.
    Linear interpolation is used to find the y value of intermediate points.
    In the case of a Hysteresis, every SimpleCycle curve will be resampled with
    an amount of points equal to Nsamples.
    
    In the case of a SimpleCycle, Monotonic curves are resampled if they are set.

    Parameters
    ----------
    curve : Hysteresis, Monotonic Cycle, or numpy array
        The curve to be resampled. If a numpy array is provided, it must be 
        increasing to be resampled properly.
    Nsamples : 
        The number of samples for the new curve.
        
    Returns
    -------
    curve : Hysteresis, SimpleCycle, 
        An object of the input type with a number of points equal to Nsamples

    """  
        
    # We recursively resample by calling the function again for sub-cycle objects
    
    # if the curve is a SimpleCycle
    if isinstance(curve, SimpleCurve):
        x = curve.xy[:,0]
        y = curve.xy[:,1]
        
        # If the simple cycle has subcycles, resample at the level of those.
        if curve.subCycles:
            outputSubcycles = [None]*curve.NsubCycles
            for ii, subcycle in enumerate(curve.subCycles):
                outputSubcycles[ii] = resample(subcycle, Nsamples)    
                
            tmpOut      =  concatenate(outputSubcycles, outputClass = SimpleCurve)
            tmpProps    = curve._getStatePropreties()
            Output      = SimpleCurve(tmpOut.xy, *tmpProps)
                        
        # Otherwise, resample the curve directly
        else:
            Output = SimpleCurve(_linInterp(x,y, Nsamples))    
       
    # if the curve is a hysteresis, we recursively create a series of Cycles
    elif isinstance(curve, Hysteresis):
        outputCycles = [None]*curve.NCycles
        for ii, cycle in enumerate(curve.cycles):
            outputCycles[ii] = resample(cycle, Nsamples)
        Output = concatenateHys(outputCycles)    # If curve
        
        
        tmpOut = concatenateHys(outputCycles)    # If curve
        tmpProps = curve._getStatePropreties()
        Output = Hysteresis(tmpOut.xy,*tmpProps)
                
        
    # if the curve is a Monotonic Cycle
    elif isinstance(curve, MonotonicCurve):
        x = curve.xy[:,0]
        y = curve.xy[:,1]
        Output = MonotonicCurve(_linInterp(x,y, Nsamples))  
    
    # if it is a np array
    elif isinstance(curve, np.ndarray):
        x = curve[:,0]
        y = curve[:,1]
        Output = _linInterp(x,y, Nsamples)  
        
    else:
        Output = None
        
    return Output
   
def resampleDx(curve, Targetdx):
    """
    Creates a new curve object where the distance between sample points
    is approximately dx. The number of samples betweent the start and 
    end point of each cycle is calculated so that the is as close to dx 
    as possible. Note that distance isn't precisely dx.
    

    For each curve, a number of points will be chosen based on some target
    displacement value in the x direction. If the value overshoots, 
    the last point will instead be used.
    For example, if the start = 2.5, end = 7.5 and dx = 2, points will be 
    placed at 2.5, 4.5, 6.5, 7.5 
    
    Linear interpolation is used to find the y value of intermediate points.
    In the case of a Hysteresis, every SimpleCurve will be resampled with
    an amount of points equal to Nsamples.
    In the case of a SimpleCurve, each monotonicCurve will be resampled.

    Parameters
    ----------
    curve : Hysteresis, Monotonic Cycle, or numpy array
        The curve to be resampled.

    Targetdx : float
        The target distance to use for sample points.
        
    Returns
    -------
    curve :
        An object of the input type, with points approximately at Targetdx.

    """  


    # the logic in these functions is getting a little nasty, in the future
    # consider pulling these out into class methods.
    if isinstance(curve, SimpleCurve):
               
        if curve.subCycles: # if subsycles are set, resample those
            outputSubcycles = [None]*curve.NsubCycles
            for ii, subcycle in enumerate(curve.subCycles):
                outputSubcycles[ii] = resampleDx(subcycle, Targetdx)
            # Output = concatenate(*outputSubcycles, outputClass = SimpleCurve)    # If curve        
        
            tmpOut      =  concatenate(outputSubcycles, outputClass = SimpleCurve)
            tmpProps    = curve._getStatePropreties()
            Output      = SimpleCurve(tmpOut.xy, *tmpProps)        
        
        else: # if subsycles aren't set, resample those
            x = curve.xy[:,0]
            dxNet = x[-1] - x[0]
            Nsamples = _getNsamples(Targetdx, dxNet)
            Output = resample(curve, Nsamples)    
        
        
    elif isinstance(curve, Hysteresis):
        outputCycles = [None]*curve.NCycles
        for ii, cycle in enumerate(curve.cycles):
            outputCycles[ii] = resampleDx(cycle, Targetdx)       
        tmpOut = concatenateHys(outputCycles)    # If curve
        tmpProps = curve._getStatePropreties()
        Output = Hysteresis(tmpOut.xy,*tmpProps)       
       
    # if the curve is a MonotonicCurve Cycle
    elif isinstance(curve, MonotonicCurve):
        x = curve.xy[:,0]
        dxNet = x[-1] - x[0]
        Nsamples = _getNsamples(Targetdx, dxNet)
        Output = resample(curve, Nsamples)  
    
    # if it is a np array
    elif isinstance(curve, np.ndarray):
        x = curve[:,0]
        dxNet = x[-1] - x[0]
        Nsamples = _getNsamples(Targetdx, dxNet)        
        Output = resample(curve, Nsamples)
        
    return Output




def _parseRegions(regions):
    """
    Ensures each region either has only two items, and
    is specified in a list of lists.
    """
    if len(regions) == 2 and isinstance(regions[0], float):
        regions = [regions]
    
    for item in regions:
        if len(item) !=2:
            raise Exception
    return regions

def _getBreakPoints(regions):
    breakPoints = set()
    for region in regions:
        breakPoints.update(set(region))
    return list(breakPoints)


def _getOutsideRegions(regions):
    """
    Gets the regions outside of the specified region
    """
    xmin = 0
    xmax = 1
    
    breakPoints = _getBreakPoints(regions)    
    
    outsideRegions = []
    isInside = []
    if xmin < breakPoints[0]:
        outsideRegions.append([xmin, breakPoints[0]])
        isInside.append(False)
    
    Nregions = len(regions)
    for ii in range(Nregions):
        outsideRegions.append(regions[ii])
        isInside.append(True)
        if ii != Nregions - 1: # check if we aren't out of bounds.
            outsideRegions.append([regions[ii][1], regions[ii+1][0]])
            isInside.append(False)
            
    if  breakPoints[-1] < xmax:
        outsideRegions.append([breakPoints[-1], xmax])        
        isInside.append(False)
        
    return outsideRegions, isInside


def resampleRegion(curve, Nsamples, regions = [[0, 0.1], [0.9, 1]]):
    """
    Resamples only parts of an input a curve. The part of the
    curve that is resampled is defined using the regions variable.
    The regions is a list of lists, defining a start and end point
    of the curve in terms of a parameter varying between 0 and 1.
    
    Each region is resampled using Nsamples

    Parameters
    ----------
    curve : Hysteresis Curve, or numpy array
        The input curve to be resampled. Can be either a hystersis curve,
        or a numpy array. If a numpy array is provided, it must not change
        direction to be resampled properly.
    region : list of lists, or list
        A lists of regions, written in terms of a parameter that ranges
        from 0 at the start of the curve to 1 at the end of the curve.
        Regions are either lists of lists, or a single list if the number 
        of regions is equal to one.
        
        Regions must be sorted from left to right and have no overlaps, i.e. 
        [[0, 0.2], [0.1, 0.2]] is invalid
        [[0, 0.1], [0.8, 0.9], [0.4, 0.5]] is invalid
        
    Nsample : int
        The number of sample to use for each region.

    Returns
    -------
    None.

    """
    
    
    regions = _parseRegions(regions) # these get interpolated
    allRegions, isInside = _getOutsideRegions(regions) # these get left alone  
    
    
    if isinstance(curve, SimpleCurve):

        if curve.subCycles: # if subsycles are set, resample those
            outputSubcycles = [None]*curve.NsubCycles
            for ii, subcycle in enumerate(curve.subCycles):
                outputSubcycles[ii] = resampleRegion(subcycle, Nsamples, regions)
                
            tmpOut      =  concatenate(outputSubcycles, outputClass = SimpleCurve)
            tmpProps    = curve._getStatePropreties()
            output      = SimpleCurve(tmpOut.xy, *tmpProps)        
        
        else: # if subsycles aren't set, resample at level of xy
        
            x = curve.xy[:,0]
            y = curve.xy[:,1]
            xy = np.column_stack([x, y])
            output = SimpleCurve(resampleRegion(xy, Nsamples, regions))        
    
    elif isinstance(curve, Hysteresis):
        outputCycles = [None]*curve.NCycles
        for ii, cycle in enumerate(curve.cycles):
            outputCycles[ii] = resampleRegion(cycle, Nsamples, regions)
        tmpOut = concatenateHys(outputCycles)
        tmpProps = curve._getStatePropreties()
        output = Hysteresis(tmpOut.xy,*tmpProps)    
    
    
    elif isinstance(curve, MonotonicCurve):
        x = curve.xy[:,0]
        y = curve.xy[:,1]
        xy = np.column_stack([x, y])
        output = MonotonicCurve(resampleRegion(xy, Nsamples, regions))  
    
    # if it is a np array
    elif isinstance(curve, np.ndarray):
        x = curve[:,0]
        y = curve[:,1] 

        xSamples = []
        ySamples = []
        
        allRegions = np.array(allRegions)*(x[-1] - x[0]) + x[0]
        
        if x[0] <= x[-1]:
            isLeftRight = True
        else:
            isLeftRight = False
        
        for ii, region in enumerate(allRegions):
            if isInside[ii]:
                xtmp = np.linspace(region[0], region[1], Nsamples)
                ytmp = _linInterpSample(x, y, xtmp)[:,1]
        
            else:
                if isLeftRight:
                    inds = np.where((region[0] < x) *  (x < region[1]))
                else:
                    inds = np.where((x < region[0]) *  (region[1] < x))

                xtmp = x[inds]
                ytmp = y[inds]
            
            xSamples.append(xtmp)
            ySamples.append(ytmp)
            
        xSamples = np.concatenate(xSamples)
        ySamples = np.concatenate(ySamples)
        output = np.column_stack([xSamples, ySamples])
        
    return output
