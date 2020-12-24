import numpy as np
import hysteresis.hys as hys


def test_comapre_basic():
    t = np.linspace(0,4,1000)*np.pi
    x = np.sin(t)
    y = np.cos(t)*t
    
    xy = np.column_stack([x,y])
    
    
    
    myHys = hys.Hysteresis(xy)
    myHys.plot(plotCycles = True)
    smallHys = hys.reSample(myHys, 10)
    # samllHys.plot()
    
    out = hys.CompareHys(smallHys,myHys)
    
    assert out[0] == 0




# t = np.linspace(0,4,1000)*np.pi
# x = np.sin(t)
# y = np.cos(t)*t

# xy = np.column_stack([x,y])



# myHys = hys.Hysteresis(xy)
# myHys.plot(plotCycles = True)
# smallHys = hys.reSample(myHys, 10) 
# smallHys.xy[:,1] = smallHys.xy[:,1] / 4
# smallHys = hys.Hysteresis(smallHys.xy)


# smallHys.plot()
# # smallHys.xy[:,1] = smallHys.xy[:,1]/2


# out = hys.CompareHys(smallHys,myHys)