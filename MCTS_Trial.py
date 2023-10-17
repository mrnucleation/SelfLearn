from time import time
from MCTSOpt.MCTree import Tree
from MCTSOpt.ParameterOpt.UniformSearch import UniformSearch
import numpy as np
from math import fabs
# =============================================================================
class FunctionWrapper:
    def __init__(self, function) -> None:
        self.function = function
        self.bestscore = None
        self.best_x = None
        self.evalcount = 0
    # --------------------------------------------------------
    def __call__(self, parameters):
        self.evalcount += 1
        score = self.function(parameters)
        if self.bestscore is None:
            self.bestscore = score
            self.best_x = parameters
        else:
            if score < self.bestscore:
                self.bestscore = score
                self.best_x = parameters
        return score
    # --------------------------------------------------------
    

#===============================================================================
def runtrial(testfunction, selectionrule, lbounds, ubounds):

    wrappedfunction = FunctionWrapper(testfunction)
    depthscale = [1.0, 0.7, 0.5, 0.3, 0.2, 0.1]
    depthlimit = len(depthscale)+5
    f_target = testfunction.f_best
    startset = np.random.uniform(lbounds, ubounds, size=ubounds.shape[0])

    indata = UniformSearch(parameters=startset, lbounds=lbounds, ubounds=ubounds, depthscale=depthscale, lossfunction=wrappedfunction)


    #---Tree Main Run loop---
    #Critical Parameters to Set
    tree = Tree(seeddata=indata, 
            playouts=20, 
            selectfunction=selectionrule, 
            headexpansion=10,
            verbose=True)
    tree.expand(nExpansions=1)
    tree.setconstant(5.37e2)
    starttime = time()
    for iLoop in range(1,500):
        print("Sub Loop Number: %s, Current Best:%s"%(iLoop, wrappedfunction.bestscore))
        tree.playexpand(nExpansions=1, depthlimit=depthlimit)
        tree.autoscaleconstant(scaleboost=2.0)
        tree.simulate(nSimulations=1)
        curmin = wrappedfunction.bestscore
        if fabs(curmin - f_target) < 1e-4 and np.linalg.norm(wrappedfunction.best_x - testfunction.x_best) < 1e-4:
            break
        curtime = time()
        print("Search Duration: %s, Best Score:%s"%(curtime-starttime, curmin))
    bestscore = wrappedfunction.bestscore   
    evalcount = wrappedfunction.evalcount 
    best_x = wrappedfunction.best_x
    return bestscore, best_x, evalcount
#===============================================================================