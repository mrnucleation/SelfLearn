from OptimizationTestFunctions import Sphere, Ackley, AckleyTest, Rosenbrock, Fletcher, Griewank, Penalty2, Quartic, Rastrigin, SchwefelDouble, SchwefelMax, SchwefelAbs, SchwefelSin, Stairs, Abs, Michalewicz, Scheffer, Eggholder, Weierstrass, plot_3d
from DeadZone import DeadZone
from HierObj_FuncTest import Func_Fragment
# ======================================================================================================================    
class MCTS_MacroScore:
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, model, dumpfilename='dumpfile.dat'):
        dim = 20
        self.triallist = [
            Sphere(dim, degree = 2),
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

        objstack = [ DeadZone(model, nullscore=0.0, zonewidth=0.75) ]
        
        #Create the list of objects to be used in the objective function.
        for func in self.triallist:
            rmseobj = Func_Fragment(func, nullscore=0.0, xtol=1e-2, ftol=1e-2)
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
        
        #Create a dump file to store the results of the optimization.
        self.dumpfilename = dumpfilename
        if self.dumpfilename is not None:
            self.dumpfile = open(self.dumpfilename, 'w')
    # ------------------------------------------------------------------------------------------------------------------
# ======================================================================================================================