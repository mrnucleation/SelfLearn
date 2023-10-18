from ObjectiveClass import HeriacleObjective
from SelectionRule_Model import SelectionRule
import numpy as np
# ===================================
class DeadZone(HeriacleObjective):
    def __init__(self, model, parentobj=None, nullscore=0.0, zonewidth=0.25, psudumpfilename='pseudo_dumpfile.dat', dumpfilename='dumpfile.dat'):
        super().__init__(parentobj, nullscore)
        self.name = 'DeadZone'
        self.zonewidth = zonewidth
        self.xhi = self.zonewidth/2.0
        self.xlo = -self.zonewidth/2.0
        self.model = model
        self.psudumpfilename = psudumpfilename
        self.psudumpfile = open(psudumpfilename, 'w')
        self.dumpfilename = dumpfilename
        self.dumpfile = open(dumpfilename, 'w')
        


        print("Using a Deadzone of width: %s"%(zonewidth))
        print("Deadzone low/high: %s, %s"%(self.xlo, self.xhi))
    # ---------------------------
    def __call__(self, parameters, verbose=False, depth=0, **kwargs):
        
        maskedweights = np.array([self.deadzone(x) for x in parameters])
        

        curweight = self.model.get_weights()
        cnt = -1
        for i, row in enumerate(curweight):
            for j, x in np.ndenumerate(row):
                cnt += 1
                curweight[i][j] = maskedweights[cnt]
        self.model.set_weights(curweight)
        
        mctsrule = SelectionRule(model=self.model)
        print("Starting Chain, Depth: %s"%(depth))
        score = 0.0
        score += self.getchildscores(parameters=parameters, model=self.model, mctsrule=mctsrule,depth=depth, **kwargs)
        numscore = np.array(score)
        if not verbose or not self.psudumpfilename is None:
            outstr = ' '.join([str(x) for x in parameters])
            self.psudumpfile.write('%s | %s \n'%(outstr, numscore))
    
        if not verbose or not self.dumpfilename is None:
            outstr = ' '.join([str(x) for x in maskedweights])
            self.dumpfile.write('%s | %s \n'%(outstr, numscore))
        return score
    
    # ---------------------------
    def deadzone(self, par):
        if par >= self.xhi:
            return par-self.xhi
        elif par <= self.xlo:
            return par-self.xlo
        else:
            return 0.0

    # ---------------------------
    def inv_deadzone(self, par):
        if par >= 0:
            return par+self.xhi
        elif par <= 0:
            return par+self.xlo
        else:
            return 0.0

    # ---------------------------
# ===================================