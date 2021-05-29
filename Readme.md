<h1 align = "Left">Hysteresis: Tools for Non-functional Curves.</h1>

Hysteresis is a Python library made non-functional curves, with an emphasis on force-deformation hystereses.
While functions only have one direction, non-functional curves change direction, and each x can be is mapped to more than one y. 
Hysteresis breaks up these curves into a number of functions that can be easily analyzed. 


A overview of the functions currently availible to users can be found here: https://hysteresis.readthedocs.io/en/latest/ <br>
Examples can be found here: https://github.com/cslotboom/hysteresis/tree/master/examples


## Contents
* [Basic Demo](https://github.com/cslotboom/Hysteresis#demo)
* [Install](https://github.com/cslotboom/Hysteresis#install)
* [Features](https://github.com/cslotboom/Hysteresis#features)
* [Tutorials](https://github.com/cslotboom/Hysteresis#tutorials)
* [Terminology](https://github.com/cslotboom/Hysteresis#Terminology)

***

## Basic Demo

Hysteresis objects are created by passing a xy curve to one of the base classes.
The resulting object has many useful methods that help with analyzing the data. Here we plot the data, seeing the the reversal poitns have been detected.

![Hysteresis demo 1](doc/images/feat/demo.gif)
```python
import numpy as np
import hysteresis as hys

t = np.linspace(0,4,1000)*np.pi
x = np.sin(t)
y = np.cos(t)*t
xy = np.column_stack([x,y])

myHys = hys.Hysteresis(xy)
myHys.plot(plotCycles = True)
```


## Install

Hysteresis is pip installable via:

```python
pip install hysteresis
```

***



## Features

Using Hysteresis, it's possible to:

### Find peaks or reversal points in data:
Using a Hysteresis object, it's possible to find the reversal points in your data, and break curves up into a series of "SimpleCycles" that are all functions.
Experimental data is often messy, and the Hysteresis package comes with a number of ways to filter the peaks of data.

Filtering peaks in data:
![Hysteresis demo 1](doc/images/feat/demo2.gif)

Finding reversal points in data ([Ex. 2.1](https://github.com/cslotboom/hysteresis/blob/master/examples/02%20Basic%20Usage/2.1%20Basic%20Seismic%20Damper/2.1%20Basic%20Seismic%20Damper.py)):
![Hysteresis demo 2](doc/images/feat/demo3.png)

### Easily display data
All Hysteresis objects come with built in plotting functionality, built off matplotlib. It's possible to plot a variatety of features about the curve, and make publication ready plots.

```
fig, ax = plt.subplots()
line = myHys.plot(plotCycles=True)
ax.set_xlabel('Actuator Displacement (mm)')
ax.set_ylabel('Applied Force (kN)')
```

### Find the area or slope of a hysteresis:
If the area or slope has been set it's possible to return the slope or area of a curve. Assuming your units are correct, the area under each hysteresis curve is the energy contained by the curve!

```
area = myHys.area
netArea = myHys.getNetArea()
cumulativeArea = myHys.getCumArea()
slope = DamperHys.slope
```

![Hysteresis demo 3](doc/images/feat/CumulativeArea_base.png)

### Down sample a hysteresis:
It's also possible to reduce the number of points in a curve, using the resample funcitons. These functions use linear interpolation to make a new curve with less data points than the original.
![Hysteresis demo 3](doc/images/feat/demo4.png)

### Compare two hystereses:
If two hystereses have the same load protocol, the hysteresis package allows you to "comapre" the curves. This operation will take two hystereses, resample them, then find the average "difference" between each point on the curve. 
![Hysteresis demo 4](doc/images/feat/compare.png)


***
## Tutorials
Youtube tutorials coming soon.

***
## Terminology

Hysteresis objects are curves that change directions in both the x axis and y axis, i.e. the change from left-right to right left. They are made up of a number of "SimpleCycle" objects, which only go one direction.

The use of the term "Cycle" in this package is a little nebulus, as it implies that we return to where we started.
In this package, a cycle is a curve that goes between two extreme values in the x axis and (roughly) does not change direction, i.e. they only go left-right or right-left. The SimpleCycle object is used to represent these curves. 
Note that changes in direction left or right that are not detected as peaks are still allowed.

MonotonicCurve is a "SimpleCycle" object that is, you guessed it, monotonic. Similar to  Small jitters up or down that are not considered peaks are still allowed.

