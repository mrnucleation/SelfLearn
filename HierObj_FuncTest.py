from ObjectiveClass import HeriacleObjective
from MCTS_Trial import runtrial
from time import time
import os
import numpy as np
import tensorflow as tf

import warnings


#==============================================================================
def var_name(var_dict, var_value):
    for name, value in var_dict.items():
        if value is var_value:
            return name
    return None

#==============================================================================
class Func_Fragment(HeriacleObjective):
    '''
    This is a simple objective function that calculates the Root Mean Square Error
    of a data set using a fragment of the data set. The goal of this is to break
    down the objective function into smaller pieces to force the optimizer
    to obtain a reasonable value for each and every chunk of data.
    '''
    #----------------------------------------------------------
    def __init__(self, testfunc, dim, xtol=1e-2, ftol=1e-2, parentobj=None,  nullscore=1.0, **kwargs):
        # Initialize the parent class
        super(Func_Fragment, self).__init__(parentobj=parentobj, nullscore=nullscore)
        
        # The name of the objective function
        self.name = 'Function_%s'%type(testfunc).__name__
        
        self.xtol = xtol
        self.ftol = ftol
        
        self.function = testfunc
        if not callable(self.function):
            raise Exception('The function must be callable.')
        xmin, xmax, ymin, ymax = self.function.bounds
        print("X Bounds: ", xmin, xmax)
        print("Y Bounds: ", ymin, ymax)
        
        # The bounds of the objective function
        self.lbounds = np.array(dim*[xmin])
        self.ubounds = np.array(dim*[xmax])
        
        self.ymin = ymin
        self.ymax = ymax
        
        # The target score and position of the objective function
        self.target_score = self.function.f_best
        self.target_x = self.function.x_best


    #----------------------------------------------------------
    def __call__(self, parameters, depth=0, **kwargs):
        # Initialize the score
        score = 0.0
        mctsrule = kwargs['mctsrule']
        
        bestscore, best_x, n_evals = runtrial(self.function, mctsrule, self.lbounds, self.ubounds)
        
        x_error = np.linalg.norm(best_x - self.target_x)
#        bestscore = (bestscore - self.ymin)/(self.ymax - self.ymin)
        f_score_error = np.abs( bestscore - self.target_score)
        score = f_score_error + 1e3*x_error

        if x_error < self.xtol: 
            score += self.getchildscores(parameters=parameters, depth=depth, **kwargs)
        else:
            score -= self.nullscore
            score += self.getnullscores(depth=depth)
        return score
    #----------------------------------------------------------
    def rmse(self, predict, target):
        '''
        This function calculates the root mean square error of the data set.
        It returns an array of the RMSE for each point in the data set.
        This is done so both the max and mean can be calculated.
        
        data: The data set to be used for the objective function
        target: The target data set to be used for the objective function
        '''
        return tf.math.square(predict - target)
#        return tf.math.reduce_mean(predict - target)**2
    #----------------------------------------------------------
#==============================================================================
