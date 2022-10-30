
import hysteresis as hys
import numpy as np
import matplotlib.pyplot as plt



x = np.linspace(0,1,101)
xy = np.column_stack([x,x])

hys.Hysteresis(xy)


out = hys.concatenateHys((xy,-xy))


halfCycle = True

loadProtocol = [0.001547,  0.00221, 0.003315, 0.00442, 0.00663, 0.00884, 0.01326,
                0.01768,   0.02652, 0.03978,  0.05967, 0.0884,  0.1326,  0.1768, 0.221, 
                0.3315,    0.4199,  0.4862]


Nrepeat     = 3*np.ones_like(loadProtocol, int)


protocol = hys.createProtocol(loadProtocol, Nrepeat) 
Npoint = len(protocol)
Npoint = np.arange(Npoint)
    
xy = np.column_stack((Npoint, protocol))

hys.SimpleCycle(xy)

# def _expandProtcol(protcol, halfCycle, Nrepeats):
    
#     # Check if Nrepeats matches protcol
    
    
#     if halfCycle:
        
#     output = [None]*np.sum()
#     for item in loadProtocol:
        


# outputProtcol