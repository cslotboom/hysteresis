
import hysteresis.env as env
# from .defaultDataFuncs import defaultSampleFunction, defaultCombineDiff
from .resample import resample


# =============================================================================
# Compare
# =============================================================================
# TODO: consider storing the sample function within the class itself.

def compareCycle(Curve1, Curve2, Nsample = 10):
    """
    Compares two Curve objects by resampling them using linear interplation,
    then comparing the distance between both cycles in a comon domain.

    Parameters
    ----------
    Curve1 : Curve
        The first curve, must be non-Hysteresis.
    Curve2 : Curve
        The second curve, must be non-Hysteresis.
    Nsample : int
        The number of samples that the comparison curves will have.
    sampleFunction : function, optional
        The sample function to be used to compare the curves. 
        The default function is "defaultSampleFunction".

    Returns
    -------
    diff : float
        The net difference between each curve.

    """
    sampleFunction = env.environment.fSample
    
    
    if Curve1.Npoints != Curve1.Npoints:
        raise Exception("Curves don't have a similar number of points.")
    
    xy1 = Curve1.xy
    xy2 = Curve2.xy
    
    xy1 = resample(xy1, Nsample)
    xy2 = resample(xy2, Nsample)
    
    
    diff = sampleFunction(xy1, xy2)

    return diff

def compareHys(Hys1, Hys2):
    """
    

    Parameters
    ----------
    Hys1 : Hysteresis Object
        The first Hysteresis object.
    Hys2 : Hysteresis Object
        The second Hysteresis object.
    combineDiff : function, optional
        The function used to combine the differences for each cycle into a 
        single value. The default is defaultCombineDiff.


    Returns
    -------
    netdiff : float
        The average difference between both curves for the entire object.
    CycleDiffs : array
        The average difference between both curves for each cycle.

    """
    
    combineDiff = env.environment.fCombineDiff

    
    
    if Hys1.NCycles != Hys2.NCycles:
        raise Exception("Hysteresis don't have a similar number of Cycles.")    
    # Check both hystesis have the same number of reversals
    
    Cycles1 = Hys1.cycles
    Cycles2 = Hys2.cycles
    
    NCycles = Hys1.NCycles
    
    cycleDiffs = [None]*NCycles
    for ii in range(NCycles):
        cycleDiffs[ii]= compareCycle(Cycles1[ii], Cycles2[ii])
        
    netdiff = combineDiff(cycleDiffs)

    return netdiff, cycleDiffs
    



