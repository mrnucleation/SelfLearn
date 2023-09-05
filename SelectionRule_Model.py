from math import exp, sqrt, log, fabs
from random import random, choice, seed, shuffle

# ========================================================
class SelectionRule(object):
    # --------------------------------------------------------
    def __init__(self) -> None:
        pass

    # --------------------------------------------------------
    def __call__(self, nodelist, exploreconstant, verbose=False):
        '''
        Default selection rule with uniqueness criteria. 
        '''
        #Compute the average uniqueness factor
        uniqscore = [1.0 for x in nodelist]
        for i, node in enumerate(nodelist):
            score = node.getuniquenessdata(nodelist)
            uniqscore[i] = score

        keylist = {}
        for i, node in enumerate(nodelist):
            keylist[str(node)] = uniqscore[i]

        selection = sorted(nodelist, key=lambda x:x.getid())
        selection = sorted(selection, key=lambda x:self.UCT_Unique_Score(x, keylist[str(x)], exploreconstant, doprint=verbose))[-1]
        print("Selecting Node %s with Score: %s"%(selection.getid(),  self.UCT_Unique_Score(selection, keylist[str(selection)], exploreconstant, doprint=verbose)  ))
        return selection
    # --------------------------------------------------------

    def UCT_Unique_Score(node, uniqval, exploreconstant, doprint=False):
        
        parent = node.getparent()
        score = node.getscore()
        visits = node.getvisits()
        if parent is None:
            parscore = node.getscore()
            parvisits = visits
        else:
            parscore = parent.getscore()
            parvisits = parent.getvisits()


        depth = node.getdepth()
        _, playoutEList = node.getallplayouts()
        usedlist = node.getusedlist()

        #nodescore = node.getscore()

        scalefunc = lambda x: x
        exploitweight = 1e300
        cnt = 1

        if len(playoutEList) > 0:
            for i, score in enumerate(playoutEList):
                if i not in usedlist:
                    exploitweight = min(exploitweight, scalefunc(score))
        exploitweight = exploitweight/cnt
        explore = 0.0

        score = -exploitweight + exploreconstant*explore
        if parent is not None:
            node.setexploitvalue(-exploitweight)
            node.setexplorevalue(explore)
        if node.isminned() or (parent is None):
            if doprint:
                try:
                    print("Node %s (Parent:%s, Depth %s, Visits:%s): Exploit: %s Score:%s"%(node.getid(), parent.getid(), depth, visits, -exploitweight, -1e20))
                except:
                    print("Node %s (Parent:Head, Depth %s, Visits:%s): Exploit: %s Score:%s"%(node.getid(), depth, visits, -exploitweight, -1e20))
            return -1e20


        if doprint:
            if parent is None:
                print("Node %s (Parent:%s, Depth:%s, Visits:%s): Exploit:%s  Explore:%s Score:%s"%(node.getid(), 'Head', depth, visits, -exploitweight, exploreconstant*explore, score))
            else:
                print("Node %s (Parent:%s, Depth:%s, Visits:%s): Exploit:%s  Explore:%s Unique:%s Score:%s"%(node.getid(), parent.getid(), depth, visits, -exploitweight, exploreconstant*explore, uniqval, score))
        return score
    # --------------------------------------------------------
    def processdata(self):
        pass
    # --------------------------------------------------------
#========================================================

