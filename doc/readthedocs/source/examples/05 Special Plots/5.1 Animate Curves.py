# -*- coding: utf-8 -*-
"""
Overview:
The Hysteresis module provides animation tools that can be used to view data 
quickly. There are two main animation types - basic and joint animations.
The basic animation plots a single curve, while joint animations animate several
curves on the same plot
The following example demonstrates how to use both animation functions to view
data.

Note, depending on your IDE, it can be useful to force a different back-end for
animations.
For example, using the spyder IDE, it's possible to force matpltlib plots to 
appear in a seperate window using the command "%matplotlib qt"

"""


import numpy as np
import hysteresis as hys
import hysteresis.plotSpecial.animate as ani


"""
First we will create some arbitrary curves that we wish to animate.
"""
x = np.linspace(0, 1, 101)*10
x2 = np.linspace(0, 1, 201)*10
y1 = np.sin(x)
y2 = np.cos(x)
y3 = np.cos(x2) + x2
sinXY = np.column_stack((x, y1))
cosXY = np.column_stack((x, y2))
cosLineXY = np.column_stack((x2, y3))

sinCurve = hys.Hysteresis(sinXY)
cosCurve = hys.Hysteresis(cosXY)
cosLineCurve = hys.Hysteresis(cosLineXY)

"""
We can make a basic animation object using the animation command. The animate
command can then be used to start the animation.

By default widgets have been turned on. You can use the nav-bar at the bottom
to cycle through the animation. Clicking on the image will also stop/start the
animation.
"""
basicAnimation = ani.Animation(sinCurve)
basicAnimation.animate()

"""
It's possible to filter the input data being passed to the animation.
For example we can only draw every other frame by using the "skipFrames" keyword.
We could also remove points from the start or end of the animation.

"""

reducedAnimation = ani.Animation(sinCurve, skipFrames =2, skipStart = 10)
reducedAnimation.animate()


"""
The joint animation function allows for two or more curves to be animated on 
the same plot. For the animation to work, both plots need the same number of xy
points.

"""
curves = [sinCurve, cosCurve]
jointAnimation = ani.JointAnimation(curves,1,1,5)
jointAnimation.animate()

"""
In practice, many of our curves will not have the same number of xy points.
To get around this, we can use tools such as the resample curve function.

Here the "cosLineCurve" has a different number of points than sinCurve/cosCurve.
We'll re'
"""

Npoint = len(sinCurve)
cosLineCurveSmall = hys.resample(cosLineCurve, Npoint)
curves = [sinCurve, cosCurve, cosLineCurveSmall]

myAnimation = ani.JointAnimation(curves,1,1,5)
myAnimation = myAnimation.animate()

