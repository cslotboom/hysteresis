# -*- coding: utf-8 -*-
"""
Created on Fri May  7 20:15:19 2021

@author: Christian


TODO:
    Add arrow key functionality?
    Add bliting
    Make ABC and make update an abstract method.
"""

# import hysteresis as hys
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
# from dataclasses import dataclass
from matplotlib.widgets import Button, Slider
import numpy as np

# Add this function to somewhere else
def init_Animation():
    fig, ax = plt.subplots()
    
    return fig, ax
    


def getAnixy(rawFrames, skipFrames):
    xyAni = rawFrames[::skipFrames,:]
    
    return xyAni

def getAniFrames(x:list, targetdx:float):
    """
    given a input array of positive nu x, return a new array 
    
    Returns a frame every target dx. Can be useful for pre-processing data
    if input data has a variable timestep.
    
    No linearl inerpolatin is used for intermediate frames.
    
    Parameters
    ----------
    x : list
        DESCRIPTION.
    targetdx : float
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

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
    
    def initAnimation(self):
        self.isPlaying = True
        self.fig, self.ax = init_Animation()
        
    def connectWidgets(self):
        
        """
        Sets up the canvas for wigits. This includes the bottom slider, 
        as well as connecting press and click events.
        """
        plt.subplots_adjust(bottom=0.25)
        
        # Connect clicking
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.fig.canvas.mpl_connect('key_press_event', self.on_press)
        
        # set up the slider axisd
        self.Sax = plt.axes([0.20, 0.1, 0.7, 0.03])
        self.slide = Slider(self.Sax, "Index", 0, self.Nframes, valinit=0,
                           valstep = 1, valfmt = "%i",  color="green")   
        self.fig.canvas.draw()
        
        # connect the update function to run when the slider changes
        self.slide.on_changed(self.update_line_slider)
        
        # self.canvas.draw_idle()
    def on_press(self, event):
        print(event.key)

    def togglePlay(self):
        """ Turns on or off the animation """
        self.isPlaying = self.isPlaying == False

    # def toggle_pause(self, event, *args, **kwargs):
    def toggle(self, event):
        """
        Toggles playing on or off
        """
        if self.isPlaying == True:
            # self.ani.pause()
            self.ani.event_source.stop()
            self.fig.canvas.draw_idle()
        else:
            # self.ani.resume()
            self.ani.event_source.start()
        self.togglePlay()

    def getClickXY(self, event):
        xclick = event.x
        yclick = event.y
        return xclick, yclick
    
    def stepForward(self, event):
        pass        
    def stepBack(self, event):
        event.key
    def getFrame(self, x):
        pass

    def on_click(self, event):
        """
        Toggles on or off playing if a click event happened within the main
        graph.

        Parameters
        ----------
        event : matplotlib event
            The matplotlib click event class.
        """
        # Check where the click happened
        (xm,ym),(xM,yM) = self.slide.label.clipbox.get_points()
        if xm < event.x < xM and ym < event.y < yM:
            # Event happened within the slider, ignore since it is handled in update_slider
            return
        else:
            self.toggle(event)
    
    
    # Define the update function
    def update_line_slider(self, currentFrame):
        """
        Converts changes in the slider to a frame that can be passed to the 
        update function.
        """
        
        self.aniArtists = self.update(currentFrame)
        self.fig.canvas.draw_idle() 
    
    
    def _get_next_frame(self, currentFrame):
        currentFrame += 1
        if currentFrame >= self.frames[-1]:
            currentFrame = 0
        return currentFrame
    
    def update_slider_widget(self, frame):
       
        """
        Updates the plot based on the current value of the slider.
        Returns a set artists for the animations
        """

        # Find the close timeStep and plot that
        # CurrentFrame = int(np.floor(plotSlider.val))

        # convert the slider value to a time step
        currentTime = self.slide.val
        currentFrame = int(currentTime)
        # CurrentFrame = (np.abs(timeSteps - CurrentTime)).argmin()

        aniframe = self._get_next_frame(currentFrame)
           
        self.slide.set_val(aniframe)
        
    @staticmethod
    def update(self, frame):
        """updates the plot"""
        pass
    
    def animate(self):
        self.initAnimation()
        # set the update function
        if self.widgets == True:        
            self.connectWidgets()
            update = self.update_slider_widget
        else:
            update = self.update
        
        self.ani = FuncAnimation(self.fig, update, self.frames,  
                                 interval=self.interval, blit=False)


# @dataclass
class Animation(AnimationBase):
        
    def __init__(self, Curve, pointsPerFrame = 1, skipFrames = 1, 
                 skipStart = 0, skipEnd = 0, interval = 50, widgets = True):
        """
        Creates a animation of the input curve object

        Parameters
        ----------
        Curve : Hysteresis Curve
            The curve to animate.
        pointsPerFrame : int, optional
            The number of data points to draw per frame. The default is 1.
        skipFrames : TYPE, optional
            THe number of animation frames to skip per input. This reduces
            can be used to reduce the size of large data arrays. The default is
            1, which shows all frames.
        skipStart : int, optional
            Allows the user to skip this many frames at the start.
            Skipped frames are applied after the other frame filters are applied.
            The default is 0, which skips no start frames.
        skipEnd : TYPE, optional
            Allows the user to skip this many frames at the start. 
            Skipped frames are applied after the other frame filters are applied.
            The default is 0, which skips no start frames.
        interval : int, optional
            The target time in ms the frame will be dispalyed for. 
            The default is 50ms.
        widgets : Boolean, optional
            A toggle that allows the user to turn on or off widgets. 
            The default is True, which has the widgets on.

        """

        self.Curve = Curve
        self.pointsPerFrame = pointsPerFrame
        self.skipStart = skipStart
        self.skipEnd = skipEnd
        self.interval = interval        
        self.widgets = widgets
        self.xy = Curve.xy
        
        xyAni   = getAnixy(self.xy, skipFrames)
        self.xyAni = self.skipStartEnd(xyAni, skipStart, skipEnd)
        
        self.Nframes = int(len(self.xyAni) / pointsPerFrame)
        self.frames  = np.arange(self.Nframes)

    def validateData(self):
        pass

    def skipStartEnd(self,xyAni, skipStart, skipEnd):
        
        if skipEnd == 0:
            return xyAni[skipStart:, :]
        else: 
            skipEnd *= -1 
        return xyAni[skipStart:skipEnd, :]


    
    def update(self, frame):
        """
        Updates the canvas at the given frame.

        """
        points = int(frame*self.pointsPerFrame)
        newXY  = self.xyAni[:points,:]
        line   = self.lines[0]
        line.set_data(newXY[:,0], newXY[:,1])
        # self.fig.canvas.draw_idle() 
        return [line]
    
    def initAnimation(self):
        super().initAnimation()
        line = plt.plot(self.xyAni[:,0], self.xyAni[:,1])[0]
        self.lines = [line]


class JointAnimation(AnimationBase):
    
    def __init__(self, curves, pointsPerFrame = 1, skipFrames = 1, 
                 skipStart = 0, skipEnd = 0, interval = 50, widgets = True):
        """
        Animates several plots on the same graph. All input graphs must have
        the same number of data points.

        Parameters
        ----------
        Curves : list
            The list of hysteresis curves to animate.
        pointsPerFrame : int, optional
            The number of data points to draw per frame. The default is 1.
        skipFrames : TYPE, optional
            THe number of animation frames to skip per input. This reduces
            can be used to reduce the size of large data arrays. The default is
            1, which shows all frames.
        skipStart : int, optional
            Allows the user to skip this many frames at the start.
            Skipped frames are applied after the other frame filters are applied.
            The default is 0, which skips no start frames.
        skipEnd : TYPE, optional
            Allows the user to skip this many frames at the start. 
            Skipped frames are applied after the other frame filters are applied.
            The default is 0, which skips no start frames.
        interval : int, optional
            The target time in ms the frame will be dispalyed for. 
            The default is 50ms.
        widgets : Boolean, optional
            A toggle that allows the user to turn on or off widgets. 
            The default is True, which has the widgets on.

        Returns
        -------
        None.

        """


        super().__init__()
        
        
        self._validateCurves(curves)
        
        self.pointsPerFrame = pointsPerFrame   
        self.skipFrames = skipFrames        
        self.skipStart  = skipStart        
        self.skipEnd    = skipEnd        
        self.interval   = interval
        self.widgets    = widgets

        self.Curves  = curves
        self.Ncurves = len(curves)
        
        xyAni = getAnixy(curves[0].xy, skipFrames)
        self.Nframes = int(len(xyAni) / pointsPerFrame)
        self.frames  = np.arange(self.Nframes)        
    
    def _validateCurves(self, curves):
        Lcurve = len(curves[0])
        ii = 1
        for curve in curves[1:]:
            if len(curve) != Lcurve:
                raise Exception('Curves must all have the same number of datapoints.') 
            ii +=1
    
    
    def initAnimation(self):
        super().initAnimation()

        self.lines = []
        self.xyCurves = [None]*self.Ncurves
        for ii in range(self.Ncurves):
            xy    = self.Curves[ii].xy
            xyAni = getAnixy(xy, self.skipFrames)
            
            self.xyCurves[ii] = xyAni
            line = plt.plot(xyAni[:,0], xyAni[:,1])[0]
            self.lines.append(line)    # def initAnimation(self):        
            
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
        
        self.aniArtists = lines
        # self.aniArtists
            # lines[ii] = line
        # lines = self.lines
        
        # return lines
        return self.aniArtists
    
    # def animate(self):
    #     self.initAnimation()
    #     if self.widgets == True:        
    #         self.connectWidgets()
    #         update = self.update_slider_widget
    #     else:
    #         update = self.update  
    #     self.ani = FuncAnimation(self.fig, update, self.frames,
    #                              interval=50, blit=False)   
    
    
    
    
    
    
 