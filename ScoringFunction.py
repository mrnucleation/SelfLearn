


class MCTS_MacroScore:
    def __init__(self, model):
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

