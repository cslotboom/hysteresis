

from .defaultDataFuncs import defaultSampleFunction, defaultCombineDiff
from .resample import resample


# =============================================================================
# Compare
# =============================================================================

def compareCycle(Curve1, Curve2, sampleFunction = defaultSampleFunction):
    
    if Curve1.Npoints != Curve1.Npoints:
        raise Exception("Curves don't have a similar number of points.")
    
    xy1 = Curve1.xy
    xy2 = Curve2.xy
    
    xy1 = resample(xy1, 10)
    xy2 = resample(xy2, 10)
    
    
    diff = sampleFunction(xy1, xy2)

    return diff

def compareHys(Hys1, Hys2, combineDiff = defaultCombineDiff):
    
    if Hys1.NCycles != Hys2.NCycles:
        raise Exception("Hysteresis don't have a similar number of Cycles.")    
    # Check both hystesis have the same number of reversals
    
    Cycles1 = Hys1.Cycles
    Cycles2 = Hys2.Cycles
    
    NCycles = Hys1.NCycles
    
    CycleDiffs = [None]*NCycles
    for ii in range(NCycles):
        CycleDiffs[ii]= compareCycle(Cycles1[ii], Cycles2[ii])
        
    netdiff = combineDiff(CycleDiffs)

    return netdiff, CycleDiffs
    



