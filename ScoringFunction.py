from OptimizationTestFunctions import Sphere, Ackley, AckleyTest, Rosenbrock, Fletcher, Griewank, Penalty2, Quartic, Rastrigin, SchwefelDouble, SchwefelMax, SchwefelAbs, SchwefelSin, Stairs, Abs, Michalewicz, Scheffer, Eggholder, Weierstrass, plot_3d
from DeadZone import DeadZone
from HierObj_FuncTest import Func_Fragment
from HierObj_ModelRange import ModelRange
from ObjectiveClass import HeriacleObjective
# ======================================================================================================================    
class MCTS_MacroScore(HeriacleObjective):
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, model, deadzone=0.25, dumpfilename="dump.dat", psuedodumpfilename='pseudo.dat'):
        super(MCTS_MacroScore, self).__init__(nullscore=0.0)
        dim = 20
        self.triallist = [
#            Sphere(dim, degree = 2),
            Ackley(dim),
            AckleyTest(dim),
            Rosenbrock(dim),
            Fletcher(dim, seed = None),
            Griewank(dim),
            Penalty2(dim, a=5, k=100, m=4),
            Quartic(dim),
            Rastrigin(dim),
            SchwefelDouble(dim),
            SchwefelMax(dim),
            SchwefelAbs(dim),
            SchwefelSin(dim),
            Stairs(dim),
            Abs(dim),
            Michalewicz(m = 10),
            Scheffer(dim),
            Eggholder(dim)
            ]

        objstack = [ DeadZone(model, nullscore=0.0, zonewidth=deadzone, dumpfilename=dumpfilename, psudumpfilename=psuedodumpfilename),
                     ModelRange(model, spreadtol=0.2, nullscore=0.0)
                     ]
        
        #Create the list of objects to be used in the objective function.
        for func in self.triallist:
            rmseobj = Func_Fragment(func, dim, nullscore=100.0, xtol=1e-1, ftol=1e-1)
            objstack.append(rmseobj)

        #We now embed all the objects into a chain of heriacle objects.
        if len(objstack) > 1:
            for i, obj in enumerate(objstack):
                if i == 0:
                    continue
                print(obj)
                objstack[i-1].addchild(obj)
        self.heracleobj = objstack[0]
        self.heracleobj.printinfo()
        
            
        self.bestscore = 1e500
        
    # ----------------------------------------------------------
    def __call__(self, parameters, depth=0, **kwargs):
        score = self.heracleobj(parameters, depth=depth, **kwargs)
        if self.bestscore > score:
            self.bestscore = score
        print("Final Score: %s"%(score))
        return score
    # ------------------------------------------------------------------------------------------------------------------
# ======================================================================================================================