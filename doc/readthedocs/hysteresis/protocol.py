import numpy as np

# from .baseClass import Hysteresis, SimpleCycle, MonotonicCurve
from .baseFuncs import concatenateHys, getReturnCycle

    
def exandHysTrace(hysteresis, loadProtocolNcycles, skipStart = 0, 
                  skipEnd = 0, FinalCyclePos = True):
    """
    This function expands the trace of a hysteresis, where the trace has only
    one reversal point.
    For example, if for a cycle N = 2, we go from:
        + -----> +
        + <----- +
    To:
        + -----> +
        + <----- +
        + -----> +
        + <----- +

        
    We do all of the hysteresis cycles, but not necessarily all of the 
    load protocol cycles.
    
    
    Parameters
    ----------
    hysteresis : Hystresis
        The input hysteresis to be expanded.
    loadProtocolNcycles : list
        The number of cycles for each reversal point.
        [N1, N2, N3, ... , N4]
    skipStart : int, optional
        Skip this many cycles at the start. The default is 0, which skips no steps.
    skipEnd : int, optional
        Skip this many cycles at the end. The default is 0, which skips no steps.
    FinalCyclePos : TYPE, optional
        If the final cycle (the failure cycle) doesn't have a revesal point,
        Then this is set to true. The default is True.



    Returns
    -------
    Hysteresis
        The output hysteresis with the expanded load protocol.

    """
    
    # !!!: the final cycle is added back if we skip failure!


    # TODO: Consider making a copy, this may be unsafe.
    Cycles = hysteresis.Cycles
    NcyclesHys = len(Cycles)
    
    # The start steps to be skipped.
    if skipStart != 0:
        loadProtocolNcycles = loadProtocolNcycles[skipStart:]
    
    # The end steps to be skipped.
    if skipEnd != 0:
        loadProtocolNcycles = loadProtocolNcycles[:-skipEnd]  
    
    
    NcyclesList = len(loadProtocolNcycles)
    
    # We multiply by two because for each full cycle there are two half cycles.    
    xyList = [None]*int(np.sum(loadProtocolNcycles*2))
    
    # If specified, we don't expand the trace failure cycle.
    if FinalCyclePos == True:
        Check = (NcyclesHys - 1) - (2*NcyclesList)
        xyList = [None]*int(np.sum(loadProtocolNcycles*2) + 1)
        # Cycles
        # loadProtocolNcycles[:-1]

    if Check != 0:
        print(NcyclesHys,  2*NcyclesList)
        raise Exception('Input Hysteresis is not compatible with the cycle list.'
                        ' The number of full cycles must be equal to half the' 
                        ' number of Simple cycles, or half the number of cycles')
    

    
    nn = 0    
    for ii, Ncycles in enumerate(loadProtocolNcycles):
        CyclePosEnter = Cycles[2*ii] 
        CycleNeg = Cycles[2*ii + 1]

        # print('Group ' + str(ii))
        # print(CyclePosEnter.xy[0,0],CyclePosEnter.xy[-1,0])
        # print(CycleNeg.xy[0,0],CycleNeg.xy[-1,0])

        if ii + 1 == NcyclesList:
            a=1
            pass
        # For every cycle except the final cycle, interpolate from the transiton cycle.
        # if int(ii + 1) != NcyclesList:
        CyclePosExit = Cycles[2*ii + 2]
        CyclePos = getReturnCycle(CycleNeg, CyclePosExit)
        
        
        # The start cycle, This is alwyas added
        xyList[nn]      =   CyclePosEnter
        nn += 1
        
        # The middle cycles
        # This is only needed if  Ncycles >2
        for jj in range(int(Ncycles) - 1):
            xyList[nn]      =   CycleNeg
            xyList[nn + 1]  =   CyclePos
            nn += 2        
        
        
        # The exit cycle This is alwyas added
        xyList[nn]      =   CycleNeg
        nn += 1

    # add the final Cycle
    if FinalCyclePos == True:
        # Cycles
        xyList[nn] = Cycles[-1]           
        nn += 1
        
    # add the end Cycles we have skipped
    # if skipFailure == True:
    #     xyList.append(Cycles[-2])
    #     xyList.append(Cycles[-1])

    return concatenateHys(*xyList)

def createProtocol(MonotonicProtocol, loadProtocolNcycles, Nsteps=0):
    """
    Creates a reverse cyclic load protocol using a monotonic load protocol.
    

    Parameters
    ----------
    MonotonicProtocol : list
        The load protocol amplitude values.
    loadProtocolNcycles : list
        The number of cycles for each reversal point.
        [N1, N2, N3, ... , N4]
    Nsteps : TYPE, optional
        This variable doesn't do anything right now, but I must have had a good reason to
        add it so it stays. The default is 0.


    Returns
    -------
    outputProtocol : array
        A np array of the input load protocol.

    """
    
    Ncycle = np.sum(loadProtocolNcycles*2)
    
    if len(MonotonicProtocol) != len(loadProtocolNcycles):
        raise Exception("The number of cycles isn't specified for each cycle in the monotonic load Protocol.")
    
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
