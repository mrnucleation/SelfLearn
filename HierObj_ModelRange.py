from ObjectiveClass import HeriacleObjective
from MCTS_Trial import runtrial
from time import time
import os
import numpy as np
import warnings
#==============================================================================
class ModelRange(HeriacleObjective):
    '''
    This is a simple objective function that calculates the Root Mean Square Error
    of a data set using a fragment of the data set. The goal of this is to break
    down the objective function into smaller pieces to force the optimizer
    to obtain a reasonable value for each and every chunk of data.
    '''
    #----------------------------------------------------------
    def __init__(self, model, spreadtol=1e1, parentobj=None,  nullscore=1.0, **kwargs):
        # Initialize the parent class
        super(ModelRange, self).__init__(parentobj=parentobj, nullscore=nullscore)
        self.randomdata = np.random.uniform(0.0, 1.0, size=(100, 5))
        self.spreadtol = spreadtol

    #----------------------------------------------------------
    def __call__(self, parameters, depth=0, **kwargs):
        # Initialize the score
        score = 0.0
        model = kwargs['model']
        
        testresults = model.predict(self.randomdata)
        maxval = testresults.max()
        minval = testresults.min()
        mean = np.mean(testresults)
#        median = np.median(testresults)
        stdev = np.std(testresults)
        
#        delta_s = np.abs(maxval-minval)
        delta_max = np.abs(maxval-mean)
        delta_min = np.abs(minval-mean)
        
        #delta = (delta_s + delta_max + delta_min)/3.0
        delta = (delta_max + delta_min)/2.0
        
        
        print("Model Spread: ", delta)
        
        score = -delta - 10.0*stdev
 
        if delta > self.spreadtol: 
            score += self.getchildscores(parameters=parameters, depth=depth, **kwargs)
        else:
            score -= self.nullscore
            score += self.getnullscores(depth=depth)
        return score
     #----------------------------------------------------------
#==============================================================================
