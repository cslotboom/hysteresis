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
import openseespyvis
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
    
    def initAnimation(self):
        self.isPlaying = True
        
        fig, ax = init_Animation()
        self.fig = fig
        self.ax = ax
        
    def connectWidgets(self):
        plt.subplots_adjust(bottom=0.25)
        # Connect clicking
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.fig.canvas.mpl_connect('key_press_event', self.on_press)
        
        self.Sax = plt.axes([0.20, 0.1, 0.7, 0.03])
        self.slide = Slider(self.Sax, "Index", 0, self.Nframes, valinit=0,
                           valstep = 1, valfmt = "%i",  color="green")   
        self.fig.canvas.draw()
        
        self.slide.on_changed(self.update_line_slider)
        
        
        # self.canvas.draw_idle()
    def on_press(self, event):
        print(event.key)

    def togglePlay(self):
        self.isPlaying = self.isPlaying == False

    # def toggle_pause(self, event, *args, **kwargs):
    def toggle(self, event):
        if self.isPlaying == True:
            # self.ani.pause()
            self.ani.event_source.stop()
            self.fig.canvas.draw_idle()
        else:
            # self.ani.resume()
            self.ani.event_source.start()
        self.togglePlay()

    def on_click(self, event):
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
        # Check where the click happened
        (xm,ym),(xM,yM) = self.slide.label.clipbox.get_points()
        if xm < event.x < xM and ym < event.y < yM:
            # Event happened within the slider, ignore since it is handled in update_slider
            return
        else:
            self.toggle(event)
    
    # Define the update function
    def update_line_slider(self, currentFrame):
        # self.update(currentFrame)
        # self.update_line_slider(currentFrame)
        self.aniArtists = self.update(currentFrame)
        self.fig.canvas.draw_idle() 
    
    def update_widget(self, frame):
       
        # Find the close timeStep and plot that
        # CurrentFrame = int(np.floor(plotSlider.val))

        # Find the close timeStep and plot that
        currentTime = self.slide.val
        currentFrame = int(currentTime)
        # CurrentFrame = (np.abs(timeSteps - CurrentTime)).argmin()

        # Manually code in the looping
        currentFrame += 1
        if currentFrame >= self.frames[-1]:
            currentFrame = 0
        print(currentFrame)
        # Update the slider
           
        self.slide.set_val(currentFrame) 

        
        # for art in aniArtists:
        #     art.set_animated(False)
        # self.fig.canvas.draw_idle()
        # self.aniArtists = aniArtists
        # Update the slider
        # return self.update_line_slider(CurrentFrame)
        return self.aniArtists
    



# @dataclass
class Animation(AnimationBase):
        
    def __init__(self, Curve, pointsPerFrame = 1, skipFrames = 1, 
                 skipStart = 0, skipEnd = 0, interval = 50, widgets = True):
        
        self.Curve = Curve
        self.pointsPerFrame = pointsPerFrame        
        self.interval = interval        
        self.widgets = widgets
        self.xy = Curve.xy
        
        self.xyAni   = getAnixy(self.xy, skipFrames)
        self.Nframes = int(len(self.xyAni) / pointsPerFrame)
        self.frames  = np.arange(self.Nframes)

    
    def update(self, frame):
        
        # for ii in range()
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

    def animate(self):
        # self.ani = animation.FuncAnimation(self.fig, self.update, self.frames, self.initfunc, 
        #                     interval=self.interval, blit=True)
        
        self.initAnimation()
        if self.widgets == True:        
            self.connectWidgets()
            update = self.update_widget
        else:
            update = self.update
        
        self.ani = FuncAnimation(self.fig, update, self.frames,  
                                 interval=self.interval, blit=False)


class JointAnimation(AnimationBase):
    
    def __init__(self, Curves, pointsPerFrame = 1, skipFrames = 1, 
                 skipStart = 0, skipEnd = 0, interval = 50, widgets = True):
        
        super().__init__()
        
        self.pointsPerFrame = pointsPerFrame   
        self.skipFrames = skipFrames        
        self.skipStart  = skipStart        
        self.skipEnd    = skipEnd        
        self.interval   = interval
        self.widgets    = widgets

        self.Curves  = Curves
        self.Ncurves = len(Curves)
        
        xyAni = getAnixy(Curves[0].xy, skipFrames)
        self.Nframes = int(len(xyAni) / pointsPerFrame)
        self.frames  = np.arange(self.Nframes)        
                
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
    
    def Animate(self):
        self.initAnimation()
        if self.widgets == True:        
            self.connectWidgets()
            update = self.update_widget
        else:
            update = self.update  
        self.ani = FuncAnimation(self.fig, update, self.frames,
                                 interval=50, blit=False)   
    
    
    
    
    
    
 