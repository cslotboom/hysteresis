
import hysteresis as hys
import numpy as np
import matplotlib.pyplot as plt




def test_1():
    loadProtocol = [1,2,3]
    ncycle = 2
    protocol = hys.createProtocol(loadProtocol, ncycle)
    answer = np.array([0,1,-1,1,-1,2,-2,2,-2,3,-3,3,-3])
    assert(np.all(protocol == answer) == True)

def test_2():
    loadProtocol = np.array([0.035 ,0.05, 0.075 ,0.1, 0.15, 0.2, 0.3, 0.4, 0.6, 
                           0.9   ,1.35, 2.0,   3.0, 4.0])*4.1/100
    Indexes = np.ones_like(loadProtocol, dtype=int) * 3
    
    protocol = hys.createProtocol(loadProtocol, Indexes)
    
    answer = np.array([ 0.      ,  0.001435, -0.001435,  0.001435, -0.001435,  0.001435,
                        -0.001435,  0.00205 , -0.00205 ,  0.00205 , -0.00205 ,  0.00205 ,
                        -0.00205 ,  0.003075, -0.003075,  0.003075, -0.003075,  0.003075,
                        -0.003075,  0.0041  , -0.0041  ,  0.0041  , -0.0041  ,  0.0041  ,
                        -0.0041  ,  0.00615 , -0.00615 ,  0.00615 , -0.00615 ,  0.00615 ,
                        -0.00615 ,  0.0082  , -0.0082  ,  0.0082  , -0.0082  ,  0.0082  ,
                        -0.0082  ,  0.0123  , -0.0123  ,  0.0123  , -0.0123  ,  0.0123  ,
                        -0.0123  ,  0.0164  , -0.0164  ,  0.0164  , -0.0164  ,  0.0164  ,
                        -0.0164  ,  0.0246  , -0.0246  ,  0.0246  , -0.0246  ,  0.0246  ,
                        -0.0246  ,  0.0369  , -0.0369  ,  0.0369  , -0.0369  ,  0.0369  ,
                        -0.0369  ,  0.05535 , -0.05535 ,  0.05535 , -0.05535 ,  0.05535 ,
                        -0.05535 ,  0.082   , -0.082   ,  0.082   , -0.082   ,  0.082   ,
                        -0.082   ,  0.123   , -0.123   ,  0.123   , -0.123   ,  0.123   ,
                        -0.123   ,  0.164   , -0.164   ,  0.164   , -0.164   ,  0.164   ,
                        -0.164   ])
    diff = np.sum(np.abs(protocol - answer))
    
    assert(np.all(diff < 10**-8) == True)


def test_3():
    loadProtocol = [1,2,3]
    ncycle = 2
    protocol = hys.createProtocol(loadProtocol, ncycle, True)
    answer = np.array([0,1,0,1,0,2,0,2,0,3,0,3,0])
    assert(np.all(protocol == answer) == True)
    
