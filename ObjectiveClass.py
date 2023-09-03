

#==============================================================================
class HeriacleObjective():
    '''
     Base Class for designing a hierarchical objective function.
     This works by creating a stack tree of objectives.  Each
     Objective in the stack is evaluated and if the objective
     is successful, the next objective is evaluated.  If the
     objective is not successful, the all objectives below it in
     the stack are not evaluated.  This is done by returning a
     nullscore for each objective below the failed objective.
    '''
    #----------------------------------------------------------
    def __init__(self, parentobj=None, nullscore=1.0):
        if not isinstance(nullscore, float):
            raise TypeError("Nullscore must be a floating point value!")
        self.name = ''
        self.parent = parentobj
        self.childlist = []
        self.nullscore = nullscore
    #----------------------------------------------------------
    def __call__(self, depth=0, **kwargs):
        score = 0.0
        score += self.getchildscores(depth=depth+1, **kwargs)
        return score
    #----------------------------------------------------------
    def printinfo(self, depth=0):
        print("Object Type: %s, Depth: %s"%(self.name, depth))
        for child in self.childlist:
            child.printinfo(depth=depth+1)

    #----------------------------------------------------------
    def getnullscores(self, depth=0):
        '''
          This is a recursive function that will return the total
          nullscore of the objective tree.  This is used when 
          the tolerance of this objective is not met, and as such
          all further objectives are not evaluated.
        '''
        score = self.nullscore
        print("Depth %s is NULL! Null Score: %s"%(depth, score))
        if len(self.childlist) < 1:
            return score
        for child in self.childlist:
            score += child.getnullscores(depth=depth+1)
        return score
    #----------------------------------------------------------
    def getchildscores(self, depth=0, **kwargs):
        score = 0.0
        if len(self.childlist) < 1:
            return score
        for child in self.childlist:
            score += child(depth=depth+1, **kwargs)
        return score
    #----------------------------------------------------------
    def setparent(self, parentobj):
        '''
         The sets the parent of the objective. This is used
         travel up the objective tree.
        '''
        self.parent = parentobj
    #----------------------------------------------------------
    def addchild(self, childobj):
        '''
         This adds a child objective to the objective tree. 
        '''
        childobj.setparent(self)
        self.childlist.append(childobj)
    #----------------------------------------------------------
#==============================================================================
