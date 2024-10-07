# -*- coding: utf-8 -*-
"""
Created on Fri May  7 20:15:19 2021

@author: Christian
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button

import numpy as np

# Add this function to somewhere else
def init_Animation():
    fig, ax = plt.subplots()
    
    return fig, ax
    


def getAnixy(rawFrames, skipFrames):
    xyAni = rawFrames[::skipFrames,:]
    
    return xyAni

def getAniFrames(x, targetdx):
    """
    Returns a frame every target dx. Can be useful for pre-processing data
    if input data has a variable timestep.
    
    No linearl inerpolatin is used for intermediate frames.
    """
    NFrames = len(x)   
    NframesOut = []
    
    jj = 0
    for ii in range(NFrames):
        
        while jj*targetdx < x[ii]:
            NframesOut.append(x[ii])
            jj+=1

    return np.array(NframesOut)

class AnimationBase:    
    
    def __init__(self):
        self.play = True
        
        # Replace with imported function
        fig, ax = init_Animation()
    
        # Connect clicking
        # fig.canvas.mpl_connect('button_press_event', self.on_click)
        fig.canvas.mpl_connect('button_press_event', self.toggle_pause)
        
        self.fig = fig
        self.ax = ax            
    
    
    
    
    def togglePlay(self):
        self.play = self.play == False
        
        
    def on_click(self, event):
        xclick = event.x
        yclick = event.y
        
        return xclick, yclick
        # print(xclick, yclick)
    
    # To be overwritten
    def toggle_pause(self,event, *args, **kwargs):
        pass
        
   #      # Check where the click happened
   #      (xm,ym),(xM,yM) = plotSlider.label.clipbox.get_points()
   #      if xm < event.x < xM and ym < event.y < yM:
   #          # Event happened within the slider, ignore since it is handled in update_slider
   #          return
   #      else:
   #          # Toggle on off based on clicking
   #          global is_paused
   #          if is_paused == True:
   #              is_paused=False
   #          elif is_paused == False:
   #              is_paused=True



# class FrameHelper():
    
#     def __init__(self, pointsPerFrame = 1, skipFrames = 1, skipStart = 0, skipEnd = 0):
    
#         self.pointsPerFrame = pointsPerFrame        




class Animation(AnimationBase):
    
    def __init__(self, Curve, pointsPerFrame = 1, skipFrames = 1, skipStart = 0, skipEnd = 0, interval = 50):
        
        super().__init__()
        
        self.Curve = Curve
        self.xy = Curve.xy
        
        self.pointsPerFrame = pointsPerFrame        
        self.interval = interval
        
        xyAni = getAnixy(Curve.xy, skipFrames)
        
        self.xyAni = xyAni
        # self.xyAni = self.xy 
        self.Nframes = int(len(self.xyAni) / pointsPerFrame)
        self.frames = np.arange(self.Nframes)
        
        self.lines = []
        
        
        # self.fig.canvas.mpl_connect('button_press_event', self.toggle_pause)


    # def setAniXY()
    def initfunc(self):
        line = plt.plot(self.xyAni[:,0], self.xyAni[:,1])[0]
        self.lines.append(line)    # def initAnimation(self):
        
        return line,
    
    def update(self, frame):
        
        # for ii in range()
        points = int(frame*self.pointsPerFrame)
        
        newXY = self.xyAni[:points,:]
        line = self.lines[0]
        line.set_data(newXY[:,0], newXY[:,1])
        
        return line,
    
    def Animate(self):
        self.ani = animation.FuncAnimation(self.fig, self.update, self.frames, self.initfunc, 
                            interval=self.interval, blit=True)


    # def toggle_pause(self, *args, **kwargs):
    #     self.togglePlay()
        
    #     if self.play:
    #         self.ani.resume()
    #     else:
    #         self.ani.pause()   
    
class JointAnimation(AnimationBase):
    
    def __init__(self, Curves, pointsPerFrame = 1, skipFrames = 1, skipStart = 0, skipEnd = 0, interval = 50):
        
        super().__init__()
        
        self.pointsPerFrame = pointsPerFrame        
        self.interval = interval
        
        self.Curves = Curves
        self.Ncurves = len(Curves)
        
        xyAni = getAnixy(Curves[0].xy, skipFrames)
        self.Nframes = int(len(xyAni) / pointsPerFrame)
        self.frames = np.arange(self.Nframes)        
        
        
        self.xyCurves = [None]*self.Ncurves
        self.lines = []
        
        for ii in range(self.Ncurves):
            curve = self.Curves[ii]
            xy = curve.xy
        
            xyAni = getAnixy(xy, skipFrames)
            self.xyCurves[ii] = xyAni
        
            # self.xyAni = xyAni

        
        # self.fig.canvas.mpl_connect('button_press_event', self.toggle_pause)


    # def setAniXY()
    def initfunc(self):
        
        for ii in range(self.Ncurves):
            tempXY = self.xyCurves[ii]
            line = plt.plot(tempXY[:,0], tempXY[:,1])[0]
            self.lines.append(line)    # def initAnimation(self):
        
        return self.lines
    
    def update(self, frame):
        
        # print(frame)
        points = int(frame*self.pointsPerFrame)
        # print(points)
        lines = [None]*self.Ncurves
        for ii in range(self.Ncurves):

            tempXY = self.xyCurves[ii]
            # print()
            
            newXY = tempXY[:points,:]
            line = self.lines[ii]
            line.set_data(newXY[:,0], newXY[:,1])
            lines[ii] = line
            
            
            # lines[ii] = line
        # lines = self.lines
        return lines
    
    def Animate(self):
        self.ani = animation.FuncAnimation(self.fig, self.update, self.frames, self.initfunc, 
                            interval=50, blit=True)   
    
    
    
    
    
    
    
 
        
    # axSlider = plt.axes([0.25, .03, 0.50, 0.02])
    # plotSlider = Slider(axSlider, 'Time', framesTime[FrameStart], framesTime[FrameEnd], valinit=framesTime[FrameStart])        
        
        
        
   # # Slider Location and size relative to plot
   #  # [x, y, xsize, ysize]
   #  axSlider = plt.axes([0.25, .03, 0.50, 0.02])
   #  plotSlider = Slider(axSlider, 'Time', framesTime[FrameStart], framesTime[FrameEnd], valinit=framesTime[FrameStart])
    
   #  # Animation controls
   #  global is_paused
   #  is_paused = False # True if user has taken control of the animation   
    
   #  def on_click(event):
   #      # Check where the click happened
   #      (xm,ym),(xM,yM) = plotSlider.label.clipbox.get_points()
   #      if xm < event.x < xM and ym < event.y < yM:
   #          # Event happened within the slider, ignore since it is handled in update_slider
   #          return
   #      else:
   #          # Toggle on off based on clicking
   #          global is_paused
   #          if is_paused == True:
   #              is_paused=False
   #          elif is_paused == False:
   #              is_paused=True
                
   #  def animate2D_slider(Time):
   #      """
   #      The slider value is liked with the plot - we update the plot by updating
   #      the slider.
   #      """
   #      global is_paused
   #      is_paused=True
   #      # Convert time to frame
   #      TimeStep = (np.abs(framesTime - Time)).argmin()
               
   #      # The current node coordinants in (x,y) or (x,y,z)
   #      CurrentNodeCoords =  nodes[:,1:] + Disp[TimeStep,:,:]
   #      # Update Plots
        
   #      # update node locations
   #      EqfigNodes.set_xdata(CurrentNodeCoords[:,0]) 
   #      EqfigNodes.set_ydata(CurrentNodeCoords[:,1])
           
   #      # Get new node mapping
   #      # I don't like doing this loop every time - there has to be a faster way
   #      xy_labels = {}
   #      for jj in range(Nnodes):
   #          xy_labels[nodeLabels[jj]] = CurrentNodeCoords[jj,:]
        
   #      # Define the surface
   #      SurfCounter = 0
        
   #      # update element locations
   #      for jj in range(Nele):
   #          # Get the node number for the first and second node connected by the element
   #          TempNodes = elements[jj][1:]
   #          # This is the xy coordinates of each node in the group
   #          TempNodeCoords = [xy_labels[node] for node in TempNodes] 
   #          coords_x = [xy[0] for xy in TempNodeCoords]
   #          coords_y = [xy[1] for xy in TempNodeCoords]
            
   #          # Update element lines    
   #          EqfigLines[jj].set_xdata(coords_x)
   #          EqfigLines[jj].set_ydata(coords_y)
   #          # print('loop start')
   #          # Update the surface if necessary
   #          if 2 < len(TempNodes):
   #              tempxy = np.column_stack([coords_x, coords_y])
   #              EqfigSurfaces[SurfCounter].xy = tempxy
   #              SurfCounter += 1
       
   #      # update time Text
   #      # time_text.set_text("Time= "+'%.2f' % time[TimeStep]+ " s")
        
   #      # redraw canvas while idle
   #      fig.canvas.draw_idle()    
            
   #      return EqfigNodes, EqfigLines, EqfigSurfaces, EqfigText        
        
        
        
	# Saving
    # if Movie != "none":
    #     MovefileName = Movie + '.mp4'
    #     ODBdir = Model+"_ODB"		# ODB Dir name
    #     Movfile = os.path.join(ODBdir, LoadCase, MovefileName)
    #     print("Saving the animation movie as "+MovefileName+" in "+ODBdir+"->"+LoadCase+" folder")
    #     ani.save(Movfile, writer='ffmpeg')             
        
def init_gui():
    fig, ax = plt.subplots()
    
    return fig, ax        



class GUIBase:
    

    def __init__(self):
        fig, ax = init_gui()
        self.fig = fig
        self.ax = ax
        
        
    def addNextBtns(self):
        
        self.axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
        self.axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
        self.bnext = Button(self.axnext, 'Next')
        self.bnext.on_clicked(self.plotNext)
        self.bprev = Button(self.axprev, 'Previous')
        self.bprev.on_clicked(self.plotPrev)
        






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


class CycleViewerCum(GUIBase):

    plotMethods = {}
    
    def __init__(self, hysteresis, plotMethod = 0):
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
        
        # Chhose the plot method
        self.plotMethod = plotMethod 
        plotMethods = [self.getSingleXy, self.getCumXy]
        self.getPlotXY = plotMethods[plotMethod]
        
        # Store the data.
        self.hysteresis = hysteresis
        self.curves = np.array(hysteresis.Cycles)
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
        
        
