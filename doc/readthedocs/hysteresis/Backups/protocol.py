import numpy as np

from .baseClass import SimpleCycle
from .baseFuncs import concatenateHys
    # We do all of the hysteresis cycles, but not necessarily all of the 
    # load protocol cycles.


def getReturnCycle(cycleStart, cycleReturn):
    """
    This function finds the return cycle that closes a hystresis Full cycle

    """
    
    
    xy1 = cycleStart.xy
    # Get the and the max value
    x1 = cycleStart.xy
    x1max = x1[0,0]
    
    xy2 = cycleReturn.xy
    x2 = xy2[:,0]
    TransitonIndex = np.argmax(x2 < x1max)
    TransitonIndex = np.argmin(x2 < x1max)
    
    xyOut = np.zeros([TransitonIndex + 1, 2])
    xyOut[:TransitonIndex,:] = xy2[:TransitonIndex,:]
    xyOut[-1,:] = xy1[0,:]
    
    return SimpleCycle(xyOut)




def exandHysTrace(hysteresis, loadProtocolNcycles, skipStart = 1, 
                  skipEnd = 1):
    """
    
    The first cycle is assumed to be in the right direction.
    
    
    This function expands the trace of a hysteresis, where the trace has only
    one cycle per displacement in the load protocol.
    For example, if for a cycle N = 2, we go from:
       | . <-- .
       | . -----> .
       | . <----- .
       |     .--> .
    To:
       |     .<-- .
       | . -----> .
       | . <----- .
       | . -----> .
       | . <----- .
       |     .--> .
       
    We assume that the trace has a start cycle, and a end cycle. These start
    and end cycles are not expanded. The final/failure cycle can occur in the 
    expansion or return direction. To ensure they are not expanded, the user
    must skip the final cycles.
    
    
   
    Where cycles don't form a closed loop, the loop will be artificially closed
    by finding the closet point to the end of the cycle
   
    
    Parameters
    ----------
    hysteresis : Hystresis
        The input hysteresis to be expanded.
    loadProtocolNcycles : list
        The number of cycles for each reversal point. Has N/2 - 1 values in it.
        Each value of the list is the number of repeats in the output hysteresis.
        [n1, n2, n3, ... , n4]
    skipStart : int, optional
        Skip this many cycles at the start. The default is 0, which skips no steps.
    skipEnd : int, optional
        Skip this many cycles at the end. The default is 1, which skips no steps.
    FinalCyclePos : Bool, optional
        If the final cycle (the failure cycle) doesn't have a revesal point,
        Then this is set to true. The default is True.



    Returns
    -------
    Hysteresis
        The output hysteresis with the expanded load protocol.

    """
    
    # !!!: the final cycle is added back if we skip failure!

    # TODO: Consider making a copy, this may be unsafe.
    # Get the cycles to be expanded
    cycles = hysteresis.cycles
    # NcyclesHys = len(cycles)
    
    # Skip the requested start and end cycles.
    toExpand = cycles[skipStart:]
    if skipEnd != 0 :
        toExpand = toExpand[:-skipEnd]
    
    # # Skip the requested start and end cycles.
    # loadProtocolNcycles = loadProtocolNcycles[skipStart:-skipEnd]
    
    # Find the number of cycles that can be expanded
    # NcyclesList = len(loadProtocolNcycles)
    NExpand = len(toExpand)
    NExpandIn = len(loadProtocolNcycles)
    
    Check = NExpand - 2*NExpandIn
    
    if Check != 0:
        print(NExpand,  2*NExpandIn)
        raise Exception('The number of entries in the load protocl does not match the '
                        'number half Cycles cycles to be expanded.')
        
        
    # Get the lenth of the output array
    xyList = [None]*int(np.sum(loadProtocolNcycles*2) + skipStart + skipEnd)


    # Create the output list of cycles to concatenate to a new Hysterersis.
    # nn corresponds to the original list, mm corresponds to the output list
    nn = 0
    mm = 0
    # The first cycles are unchanged
    xyList[:skipStart] = cycles[:skipStart]
    
    nn += skipStart
    mm += skipStart
    # All other cycles are expanded
    for Ncycles in loadProtocolNcycles:
        # Get the negative, positive, and positive exit cycles
        CycleNeg = cycles[nn]
        CyclePosExit = cycles[nn + 1]
        CyclePos = getReturnCycle(CycleNeg, CyclePosExit)

        # get the secondary cycles
        for ii in range(Ncycles):
            # The first cycle is always a Negative standard cycle
            xyList[mm] = CycleNeg
            
            # The second cycle my be a exit cycle. It it isn't, it's a truncated
            # positive cycle
            if ii != Ncycles - 1:
                xyList[mm + 1] = CyclePos
            else:
                xyList[mm + 1] = CyclePosExit
            mm += 2
        
        nn += 2
    
    if skipEnd != 0 :
        xyList[-skipEnd:] = cycles[-skipEnd:]

    return concatenateHys(*xyList)

def _checkNcycles(MonotonicProtocol, loadProtocolNcycles):
    
    if isinstance(loadProtocolNcycles, int):
        return np.ones_like(MonotonicProtocol, int) * loadProtocolNcycles
    
    elif isinstance(loadProtocolNcycles, list) or isinstance(loadProtocolNcycles, np.ndarray):
        return np.array(loadProtocolNcycles, int)
        
    else:
        raise Exception('The input loadProtocolNcycles must be a integer, list, or numpy array')

def _getCyclePoints(P1, P2, Nsteps):
    np.linspace(P1, P1)


def createProtocol(MonotonicProtocol, loadProtocolNcycles):
    """
    Creates a reverse cyclic load protocol using a monotonic load protocol.
    

    Parameters
    ----------
    MonotonicProtocol : list
        The load protocol amplitude values.
    loadProtocolNcycles : list, or int
        The number of cycles for each reversal point.
        if an integer all cycles will be expanded by the input integer.
        
        If it's a list, each monotonic cycle 'x' will be expanded by Nx
        [N1, N2, N3, ... , N4]

    Returns
    -------
    outputProtocol : array
        A np array of the input load protocol.

    """
    
    """
    Nsteps : int, optional
        The number of steps in the between each input point. Must be two or greater.
        The default is 2.    
    """
    
    # Check the number of expansions to use per cycle
    loadProtocolNcycles = _checkNcycles(MonotonicProtocol, loadProtocolNcycles)
    
    Ncycle = np.sum(loadProtocolNcycles)
    
    if len(MonotonicProtocol) != len(loadProtocolNcycles):
        raise Exception("The number of cycles isn't specified for each cycle in the monotonic load Protocol.")
    
    # The total number of points is equal to the number of cycles
    # Npoints = (Ncycle*2  + 1) * (Nsteps - 1)
    
    outputProtocol = np.zeros(Ncycle*2 + 1)
    nn = 1
    for ii in range(len(MonotonicProtocol)):
        posPeak = MonotonicProtocol[ii]
        negPeak = -posPeak
        
        for jj in range(loadProtocolNcycles[ii]):
            outputProtocol[nn] = posPeak
            outputProtocol[nn + 1] = negPeak
            nn += 2
            
        
    return outputProtocol
