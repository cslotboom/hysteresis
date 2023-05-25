"""
In this example, plots from section 3.2 of "Hysteresis - A Python Library 
for Analysing Structural Data" from WTCE 2023 are showcased.

In this model, the nonlinear material propreties for a siesmic damper are chosen
to match a set of test data. The test data is stored in two files.

The example makes use of OpenSeesPy for the damper analysis, and the hysteresis
package for comparing output xy curves.

The example requires two additionsl packages installed to work:
    - OpenseesPy (https://openseespydoc.readthedocs.io/en/latest/index.html)
    - naturalize (https://github.com/cslotboom/Naturalize) 

"""

import naturalize as nat
import numpy as np
import os
import hysteresis as hys

import matplotlib.pyplot as plt
import openseespy.opensees as op

def testIndividual(individual):
    """
    Runs a nonlinear analysis on the damper and returns the output damper 
    hysteresis
    
    """
    
    [Fu, k, b, R0, cR1, cR2] = individual.genotype[0]
    gen = str(individual.gen)
    name = str(individual.name)
    print(name)    
    
    
    # Make a folder for the file.
    genName = 'gen' + str(int(gen))
    
    if not os.path.isdir(genName):
        os.mkdir(genName)

    op.wipe()
    op.model('Basic' , '-ndm',  2,  '-ndf' , 3 )
    
    
    ## Analysis Parameters material(s) 
    ## ------------------
    LoadProtocol = np.array([0.0017, 0.005, 0.0075, 0.012, 0.018, 0.027, 
                             0.04, 0.054, 0.068, 0.072,0.])

    # Step size
    dx = 0.0001
        
    op.uniaxialMaterial( 'Steel02', 1,  Fu,  k, b, R0, cR1, cR2, 0.,  1.,  0.,  1.)
    
    ERelease = 1.
    op.uniaxialMaterial( 'Elastic' ,  2,  ERelease,  0.0 )
    
    ## Define geometric transformation(s) 
    ## ---------------------------------- 
    #geomTransf('Linear',1) 
    op.geomTransf('PDelta',1)
    op.beamIntegration('Lobatto',1,1,3)
    
    # Define geometry 
    # ---------------
    op.node(1,  0., 0.,  '-ndf', 3)
    op.node(2,  0., 0.,  '-ndf', 3)
    op.fix(1,1,1,1)
    
    # Define element(s) 
    # ----------------- 
    op.element("zeroLength" , 1  , 1, 2, '-mat', 1,2,2,'-dir', 1,2,3, '-orient', 1., 0., 0., 0., 1., 0.)
    
    # Define Recorder(s) 
    # ----------------- 
    op.recorder( 'Node' , '-file' , 'gen' + gen + '\\' + name + ' ' + 'RFrc.out' , '-time' ,  '-nodeRange', 1,1, '-dof', 1 , 'reaction')
    op.recorder( 'Node' , '-file' , 'gen' + gen + '\\' + name + ' ' + 'Disp.out' , '-time' ,  '-nodeRange', 2,2, '-dof', 1 , 'disp')
    
    
    # Define Analysis Parameters
    # ----------------- 
    op.timeSeries('Linear',1,'-factor' ,1.0)  
    op.pattern  ('Plain',1, 1,  '-fact', 1.) 
    op.load(2, 1.,  0.0, 0.0)
    
     
    # op.initialize() 
    op.constraints("Plain")
    op.numberer("Plain")
    # System of Equations 
    op.system("UmfPack", '-lvalueFact', 10)
    # Convergence Test 
    op.test('NormDispIncr',  1.*10**-8, 25, 0 , 2)
    # Solution Algorithm 
    op.algorithm('Newton')
    # Integrator 
    op.integrator('DisplacementControl', 2, 1, dx)
    # Analysis Type 
    op.analysis('Static')
    
    ControlNode = 2
    ControlNodeDof = 1
    
    op.record()
    
    ok = 0
    # Define Analysis 
    for x in LoadProtocol:
        for ii in range(0,1):
            
            # op.
            op.integrator('DisplacementControl', ControlNode, ControlNodeDof, dx)
            while (op.nodeDisp(2,1) < x):
                ok = op.analyze(1)
                if ok != 0:
                    print('Ending analysis')
                    op.wipe()
                    return np.array([0,0])
                
            op.integrator('DisplacementControl', ControlNode, ControlNodeDof, -dx)
            while (op.nodeDisp(2,1) > -x):
                ok = op.analyze(1)
                if ok != 0:
                    print('Ending analysis')
                    op.wipe()
                    return np.array([0,0])                  
                
    op.wipe()    
    
    # read the outputs from the recorder.
    fileDispName = os.path.join('gen' + str(gen), str(name) + ' Disp.out')
    fileForceName = os.path.join('gen' + str(gen), str(name) + ' RFrc.out')
    
    disp = np.loadtxt(fileDispName)
    RFrc = np.loadtxt(fileForceName)
    
    # save the displacement and force data
    x = disp[:,1]
    y = -RFrc[:,1]
    
    xy = np.column_stack([x,y])
    return xy

def ftest(individual, env):
    """
    In this case, the test function is sperate from ftest. While not strictly
    necessary, in many cases the function being used in the optimization 
    analysis will be 
    """
    result = testIndividual(individual)
    return result


def fitness(individual, env):
    """
    Fitness functions can be used to post-process the test results, and
    determine a single score from it test.
    In this case, the xy curve output from the analysis is compared to the 
    xy curve from experimental hysteresis, using the hysteresis package's 
    compare hysteresis function.
    """
    
    # Get the XY data
    xyAnalysis = individual.result
    
    
    # Try to make the output object into a hysteresis, if it can't be then 
    # skip the analysis and assume the input values are bad. This usually 
    # happens because the output xy curve has bad data points in it.
    try:
        hys1 = hys.Hysteresis(xyAnalysis)
    except:
        return 10**6
    hys2 = env.hys2

    # similarly, compare the input and output curves. If they can't be compared,
    # assume there is an error.
    try:
        diff, test = hys.compareHys(hys1, hys2)
    except:
        diff  = 10**6
   
    return diff



class Environment:
    """
    The environment is the background test data we want to use to match our
    damper popreties to. The data is read and some unit conversions are done.   
    Data stored in the environment will be 
    """
    
    def __init__(self):
        
        inches = 0.0254
        kip = 4.45*10**3
        
        EDataName = "BackboneData.csv"
        ExperimentData = np.loadtxt(EDataName,delimiter=',')
        
        Backbonex = ExperimentData[:,0]*inches
        Backboney = ExperimentData[:,1]*kip
        
        xyExp = np.column_stack([Backbonex, Backboney])
        self.hys2 = hys.Hysteresis(xyExp) 




"""
Define bounds on the damper. These are chosen based on typical estimates
for steel02 damper propreties.
"""
llims =  np.array([21.1*10**3, 2.6*10**6, 0.015, 19, .95, .15]) * 0.
ulims =  np.array([21.1*10**3, 2.6*10**6, 0.015, 19, .95, .15]) * 1.5
genePool = nat.BasicGenePool(llims, ulims)
analysisEnvironment = Environment()
helper = nat.AlgorithmHelper(ftest, genePool, fitness, environment = analysisEnvironment)

Ngen = 100
Npop = 30
Ncouples = 8
Nsurvive = 2
mutateThresold = 0.1

algorithm = nat.GeneticAlgorithm(helper, Npop, Ncouples, Nsurvive, mutateThresold)
analysis = nat.Analysis(algorithm)
solution = analysis.runAnalysis(Ngen)

np.array([2.33023155e+04, 2.94258681e+06, 2.36158239e-03, 4.06597565e+00,
        5.68384723e-01, 1.49959762e-01])

# Make a fake individual for plotting.
solutionIndv = nat.Individual([solution])
solutionIndv.gen = 0
solutionIndv.name = 'optimal'
xy = testIndividual(solutionIndv)

solHys = hys.Hysteresis(xy)

fig,ax = plt.subplots()
analysisEnvironment.hys2.plot()
solHys.plot()
ax.minorticks_on()
ax.grid(which='major', color='grey', linewidth=0.5, alpha = 0.8)
# ax.grid(b=True, which='minor', linewidth=0.5, alpha = 0.4)
ax.legend(loc='lower right')
ax.set_xlabel('Actuator Displacement (m)')
ax.set_ylabel('Actuator Force (N)')
plt.show()

