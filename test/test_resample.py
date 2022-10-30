import numpy as np
import hysteresis as hys


t = np.linspace(0,4,100)*np.pi
x = np.sin(t)
y = np.cos(t)*t
xy = np.column_stack([x,y])
ty = np.column_stack([t ,y])
tyReversed = np.column_stack([t[::-1] ,y[::-1]+y])

myHys = hys.Hysteresis(xy)
resampled = hys.resample(myHys, 10)

cycles = hys.SimpleCycle(ty, findPeaks=True)
resampledCycles = hys.resample(cycles, 5)

cycle1 = hys.SimpleCycle(ty, findPeaks=True)
cycle2 = hys.SimpleCycle(tyReversed, findPeaks=True)
curves = [cycle1, cycle2]

hysWithReversals = hys.concatenate(curves)

def test_Hysteresis_lengths():
    """ Tests if a resampled hysteresis has the correct number of cycles. """
    assert len(resampled.cycles[0]) == 10 and len(resampled.cycles[2]) == 10

def test_SimpleCycle_lengths():
    """ Tests if a resampled SimpleCycle has the correct number of cycles. """
    assert len(resampledCycles.subCycles[0]) == 5 and len(resampledCycles.subCycles[2]) == 5


def test_compare_basic():
    
    # myHys.plot(plotCycles = True)
    smallHys = hys.resample(myHys, 10)
    
    out = hys.compareHys(smallHys,myHys)
    
    assert out[0] == 0
    

def test_combined_length():
    output = hys.resample(hysWithReversals, 10)
    Nout = [len(curve) for curve in output.cycles]
    check2 = sum(Nout) == 20
    assert (len(output) == 19) and check2
    

