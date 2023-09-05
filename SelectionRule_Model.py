from math import exp, sqrt, log, fabs
from random import random, choice, seed, shuffle
import numpy as np
# ========================================================
def islower(a):
    if a < 0.0:
        return 1.0
    else:
        return 0.0
# ========================================================
class SelectionRule(object):
    # --------------------------------------------------------
    def __init__(self, **kwargs) -> None:
        if 'useplayscores' in kwargs:
            if not isinstance(kwargs['useplayscores'], bool):
                raise Exception('useplayscores must be a boolean value.'
            self.useplayscores = kwargs['useplayscores']
        else:
            self.useplayscores = True

    # --------------------------------------------------------
    def __call__(self, nodelist, exploreconstant, verbose=False):
        '''
         Selection rule with neural network model for the exploration side
         of the UCT score.
         For this selection rule we compile a list of node features such as
         1. Score of this node's parameter set
         2. Visits/Total Playouts
         3. Parent's Visits/Total Playouts
         4. Depth in Tree
         5. Percentage of successful playouts (IE playouts that are lower than the score of this node)
         6. Reduced exploit score of the node (IE the lowest playout score that has not been used)
         
         This is then used to construct a feature matrix that is fed through the model
         and the resulting output is used as the exploration score.
         
         The equation used is givens
         
         UCT(Node) = minscore(Node) + C*Explore(Node)
        
        '''
        
        
        scorelist = []
        for node in nodelist:
            score = node.getscore()
            usedlist = node.getusedlist()
            exploitweight = score
            if self.useplayscores:
                if len(playoutEList) > 0:
                    for i, score in enumerate(playoutEList):
                        if i not in usedlist:
                            exploitweight = min(exploitweight, score)
            scorelist.append(exploitweight)
        maxscore = max(reducedscores)
        minscore = min(reducedscores)
        reducedscores = [ -(score-minscore)/(maxscore-minscore) for score in scorelist]
        reducedscores = np.array(reducedscores)
        
        features = []
        for node, exploitweight in zip(nodelist, reducedscores):
            node.setexploitvalue(exploitweight)
            parent = node.getparent()
            visits = node.getvisits()
            if parent is not None:
                parvisits = parent.getvisits()
            else:
                parvisits = visits
            score = (node.getscore()-minscore)/(maxscore-minscore)
            depth = node.getdepth()
            _, playoutEList = node.getallplayouts()
            playdiff = [islower(playscore-score) for playscore in playoutEList] 
            successes = sum(playdiff)
            tries = len(playdiff)
            success_rate = successes/tries
            
            features.append([score, visits, parvisits, depth, success_rate, exploitweight])
           
        featurematrix = np.array(features)
        explorescores = self.model.predict(featurematrix)
        
        for node, score in zip(nodelist, explorescores):
            node.setexplorevalue(score)
        
        uct_score = [expoitweight + exploreconstant*explorescore for exploitweight, explorescore in zip(reducedscores, explorescores)]]    
        selection_pos = np.argmax(uct_score)  
        selection = nodelist[selection_pos]
        
        print("Selecting Node %s with Score: %s"%(selection.getid(), uct_score[selection_pos]))
        return selection
    # --------------------------------------------------------
#========================================================

