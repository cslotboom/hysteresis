# -*- coding: utf-8 -*-
"""
@author: Christian

Curves in the hysteresis module are compatible with basic operations, i.e.
addition, subtraction, multiplication, and 


"""

import numpy as np
import hysteresis as hys

x = np.linspace(0,4,1001)
y = x**3 - 3*x**2 + 3

xy = np.column_stack([x,y])
dataHys = hys.Hysteresis(xy)


"""
The it's possible to perform standard operations using scalars, numpy arrays 
of equal size, and other hysteresis curves to each hysteresis.
These operations are applied to the y data of the curve respectivly.

"""
examples = []
examples.append( dataHys + 1 )
examples.append( dataHys + 2*x )
examples.append( 2 - dataHys/2 + 2*x )
examples.append( dataHys * dataHys / (y+50) )

dataHys.plot()
for curve in examples:
    curve.plot(linewidth = 2)


"""
Hystersis objects also support iteration and object retreval!
"""

dataHys[4] = [0,0]
print(dataHys[4])

for xy in dataHys:
    print(xy)



