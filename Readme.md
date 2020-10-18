<h1 align = "Middle">~~==Currently in beta==~~</h1>
Currently in beta testing - comments welcome.
Beta testing means the package is working and stable but my test suite isn't totally complete, and I don't my examples or documentation finished.


<h1 align = "Left">Hysteresis: Tools for Non-functional curves.</h1>


Hysteresis is a library of tools for non-functional curves, with a emphasis on force-deformation hysteresis curves.
While functions only have one direction, non functional curves change direction, making analyzing them difficult.
Some key features of the library include:

* Finding peaks or reversal points in data.
* Numerically finding the slope or area of a curve.
* Resampling curves.
* Comparing Hysteresis made with simialar load protocols.

## Contents

* [Demo](https://github.com/cslotboom/Hysteresis#demo)
* [Install](https://github.com/cslotboom/Hysteresis#install)
* [Features](https://github.com/cslotboom/Hysteresis#features)
* [Tutorials](https://github.com/cslotboom/Hysteresis#tutorials)
* [Terminology/gottca](https://github.com/cslotboom/Hysteresis#Terminology)

## Basic Demo

A basic demo of the hystresis object. 
Hysteresis can split up a non-function into a number of cycles that are functions.
This allows them to be analyzed more easily or compared with other hystereses.

![Hysteresis demo 1](doc/images/feat/demo.gif)


## Install

Hysteresis is pip installable via:

`pip install hysteresis`



## Features

Using Hysteresis, it's possible to:

Find peaks
![Hysteresis demo 1](doc/images/feat/demo2.gif)

Find cycles:
![Hysteresis demo 2](doc/images/feat/demo3.png)

Find energy in a hysteresis:
![Hysteresis demo 3](doc/images/feat/CumulativeArea_base.png)

Down sample a hysteresis:
![Hysteresis demo 3](doc/images/feat/demo4.png)


![Hysteresis demo 4](doc/images/feat/compare.png)


## Terminology

A SimpleCycle is Curve that is a function, that is, each x value is paired with a single y value.
The term "Cycle" is a little nebulus, as it implies that we return to where we started.

A MonotonicCurve is a Curve that only increases or decreases


