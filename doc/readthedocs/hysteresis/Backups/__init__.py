from .baseClass import Hysteresis, SimpleCycle, MonotonicCurve
from .baseFuncs import concatenateHys, removeNegative
from .resample import resample, resampleDx

from .compare import compareCycle, compareHys
from .protocol import exandHysTrace, createProtocol
from .climate import SeasonalCurve
from .envelope import getBackboneCurve, getAvgBackbone, fitEEEP

# from .env import HYSTERESIS_ENVIRONMENT
# environment = HYSTERESIS_ENVIRONMENT()

# from .env import environment
# environment.restart()
