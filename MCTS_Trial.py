from time import time
from MCTSOpt.MCTree import Tree
from MCTSOpt.ParameterOpt.UniformSearch import UniformSearch
import numpy as np

#===============================================================================
def runtrial(testfunction, selectionrule):

    depthscale = [1.0, 0.7, 0.5, 0.3, 0.2, 0.1]
    depthlimit = len(depthscale)+5
    ubounds = testfunction.ubounds
    lbounds = testfunction.lbounds
    startset = np.random.uniform(lbounds, ubounds, size=ubounds.shape[0])

    indata = UniformSearch(startset, lbounds, ubounds, depthscale=depthscale)
    indata.setevaluator(testfunction)


    #---Tree Main Run loop---
    #Critical Parameters to Set
    tree = Tree(seeddata=indata, 
            playouts=20, 
            selectfunction=selectionrule, 
            headexpansion=10)
    tree.setconstant(5.37e2)
    starttime = time()
    for iLoop in range(1,50):
        print("Loop Number: %s"%(iLoop))
        tree.playexpand(nExpansions=1, depthlimit=depthlimit)
        tree.simulate(nSimulations=1)
        curmin = tree.getbestscore()
        curtime = time()
        print("Search Duration: %s, Best Score:%s"%(curtime-starttime, curmin))
#===============================================================================