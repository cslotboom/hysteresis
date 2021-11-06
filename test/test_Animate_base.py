# -*- coding: utf-8 -*-
"""
Created on Sat May  1 23:49:09 2021

@author: Christian

IT's diffcult to test the GUI functions 


"""


import numpy as np
import hysteresis.plotSpecial.animate as ani

testBase = ani.AnimationBase()
testBase.isPlaying = True
testBase.frames = np.arange(20)

    
def test_Toggle():
    testBase.togglePlay()
    assert testBase.isPlaying == False
    
def test_get_next_frame_incriment():
    frame = testBase._get_next_frame(5)
    assert frame == 6

def test_get_next_frame_loop():
    frame = testBase._get_next_frame(21)
    assert frame == 0




