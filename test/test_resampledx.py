import numpy as np
import hysteresis as hys

t = np.linspace(0,4,100)*np.pi
x = np.sin(t)
y = np.cos(t)*t
xy = np.column_stack([x,y])
ty = np.column_stack([t ,y])
tyReversed = np.column_stack([t[::-1] ,y[::-1]+y])

# myHys = hys.Hysteresis(xy)
# resampled = hys.resampledx(myHys, 10)

dx = 0.1
cycle = hys.SimpleCycle(ty, findPeaks=True)
resampledCycle = hys.resampleDx(cycle, dx)

# resampledCycles.plot()
# hys.resample(curve, Nsamples, kwargs)


# cycle1 = hys.SimpleCycle(ty, findPeaks=True)
# cycle2 = hys.SimpleCycle(tyReversed, findPeaks=True)
# curves = [cycle1, cycle2]

# hysWithReversals = hys.concatenate(curves)

def test_resampledx():
    """ Tests if a resampled hysteresis has the correct number of cycles. """
    
    error1 = abs(abs(resampledCycle[10][0]-resampledCycle[11][0])/dx - 1)
    error2 = abs(abs(resampledCycle[-10][0]-resampledCycle[-11][0])/dx - 1)
    assert (error1 < 0.02) and  (error2 < 0.02)

# test_resampledx()


