import numpy as np

# from .baseClass import Hysteresis, SimpleCycle, MonotonicCurve
from .baseFuncs import concatenateHys, getReturnCycle

    
def exandHysTrace(hysteresis, loadProtocolNcycles, skipStart = 0, 
                  skipEnd = 0, FinalCyclePos = True):
    
    """
    Exands the trace of a hystresis.
    Each Cycle is a
    
    We do all of the hysteresis cycles, but not necessarily all of the 
    load protocol cycles
    
    
    !!!: the final cycle is added back if we skip failure!
    
    CycleList
    """

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
