.. Hysteresis documentation master file, created by
   sphinx-quickstart on Sat Oct 10 17:07:34 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Hysteresis Documentation
======================================
Hysteresis is a library of tools for non-functional curves, with a emphasis on force-deformation hysteresis curves.


Install using:

::

	pip install hysteresis

A simple script is shown below:

::

	# import numpy and hysteresis
	import numpy as np
	import hysteresis as hys

	# Create a simple non-functional curve
	t = np.linspace(0,4,1000)*np.pi
	x = np.sin(t)
	y = np.cos(t)*t
	xy = np.column_stack([x,y])

	# Create a hysteresis object and 
	myHys = hys.Hysteresis(xy)
	myHys.plot(plotCycles = True)


.. toctree::
   :maxdepth: 2
   :caption: Contents:
   hys
   data



=============
 Developed by
=============

*Christian Slotboom* `<https://github.com/cslotboom/Hysteresis>`_.

| M.A.Sc. Structural Engineering
| Engineer in Training 



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
