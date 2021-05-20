# -*- coding: utf-8 -*-
"""
Created on Fri May  7 20:15:19 2021

@author: Christian
"""

import matplotlib.pyplot as plt
from matplotlib.widgets import Button

# from matplotlib.animation import FuncAnimation
import numpy as np

def init_gui():
    fig, ax = plt.subplots()
    
    return fig, ax        



class GUIBase:
    

    def __init__(self):
        fig, ax = init_gui()
        self.fig = fig
        self.ax = ax
        pass
        
    def addNextBtns(self):
        
        self.axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
        self.axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
        self.bnext = Button(self.axnext, 'Next')
        self.bnext.on_clicked(self.plotNext)
        self.bprev = Button(self.axprev, 'Previous')
        self.bprev.on_clicked(self.plotPrev)
        
    def setlims(self, xlims,ylims):
        if xlims != []:
            self.ax.set_xlim(*xlims)
        if ylims != []:
            self.ax.set_xlim(*ylims)            

class CycleViewer(GUIBase):

    
    
    def __init__(self, hysteresis, showCumulative = False):
        
        super().__init__()
        
        self.showCumulative = showCumulative 
        
        
        self.hysteresis = hysteresis
        self.curves = np.array(hysteresis.Cycles)
        
        self.ind = 0
        self.Ncurves = hysteresis.NCycles
        # xyAni = getAnixy(Curve.xy, skipFrames)
        
        # add line
        self.line = self.curves[-1].plot()
        
        # a list of active curves
        # self.activeLines =  [self.line]
        
        
        # adjsut plot and add buttons
        plt.subplots_adjust(bottom=0.2)
        self.addNextBtns()
        
        plt.show()
    
    # def getActiveCurves    
    
    
    
    # def initAnimation(self):
    def updateplt(self, ind):
        # print('pressed')
        
        # xy = []
        # for ii in range(ind):
        #     xy.append(self.curves[ind].xy)
        
        # xy = np.concatenate(xy)
        xy = self.curves[ind].xy
        self.line.set_xdata(xy[:,0])
        self.line.set_ydata(xy[:,1])
        plt.draw()
        
    # def updatepltCumulative
        
    def plotNext(self, event):
        self.ind = (self.ind + 1) % self.Ncurves
        self.updateplt(self.ind)

        
    def plotPrev(self, event):
        self.ind = (self.ind - 1) % self.Ncurves
        self.updateplt(self.ind)


class CycleViewer(GUIBase):

    plotMethods = {}
    
    def __init__(self, hysteresis, plotMethod = 0, xlims=[],ylims = []):
        """
        An interactive  figures to be plotted 
        
        
        Plots must use a qt backend for the GUI elements to work
        correctly. %matplotlib qt
        

        Parameters
        ----------
        hysteresis : TYPE
            DESCRIPTION.
        plotMethod : TYPE, optional
            DESCRIPTION. The default is 'single'.

        Returns
        -------
        None.

        """
        
        
        
        super().__init__()
        self.setlims(xlims,ylims)
        
        
        # Chhose the plot method
        self.plotMethod = plotMethod 
        plotMethods = [self.getSingleXy, self.getCumXy]
        self.getPlotXY = plotMethods[plotMethod]
        
        # Store the data.
        self.hysteresis = hysteresis
        self.curves = np.array(hysteresis.cycles)
        # print(self.curves)
        
        # self.ind = np.array([0],dtype=int)
        self.ind = 0
        self.Ncurves = hysteresis.NCycles
        # xyAni = getAnixy(Curve.xy, skipFrames)
        
        # add initial lines and text
        self.line = self.curves[-1].plot()
        self.annot = self.ax.annotate(self.ind,(0.05,0.05), xycoords='axes fraction')        
        
        # adjsut plot and add buttons
        plt.subplots_adjust(bottom=0.2)
        self.addNextBtns()
        
        # start plot
        plt.show()
        # self.updateplt(0)   
    
    
    def getSingleXy(self, ind):
        curve = self.curves[ind]
            
        return curve.xy

    
    def getCumXy(self,ind):
        curves = self.curves[:ind+1]
        xy = np.array([])
        xy.shape = (0,2)

        for curve in curves:
            
            tempxy = curve.xy
            xy = np.concatenate([xy,tempxy])
            
        return xy
    
    def updateplt(self, ind):

        xy = self.getCumXy(ind)

        self.line.set_xdata(xy[:,0])
        self.line.set_ydata(xy[:,1])
        
        text = f'Cycle {self.ind}'

        self.annot.set_text(text)
        
        
        plt.draw()
        
        
    def plotNext(self, event):
        self.ind = (self.ind + 1) % self.Ncurves
        self.updateplt(self.ind)

        
    def plotPrev(self, event):
        self.ind = (self.ind - 1) % self.Ncurves
        self.updateplt(self.ind)

    # def plot():
    #     plt.show()

    # def CyclePlot()
    
            # def initAnimation(self):
# def updateplt(self, ind):
#     print('pressed')
#     xy = self.curves[ind].xy
#     self.line.set_xdata(xy[:,0])
#     self.line.set_ydata(xy[:,1])
#     plt.draw()
    
# def plotNext(self, event):
#     print('pressed')
#     self.ind = (self.ind + 1) % self.Ncurves
#     self.updateplt(self.ind)

    
# def plotPrev(self, event):
#     self.ind = (self.ind - 1) % self.Ncurves
#     self.updateplt(self.ind)
        
        
