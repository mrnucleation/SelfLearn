from OptimizationTestFunctions import Sphere, Ackley, AckleyTest, Rosenbrock, Fletcher, Griewank, Penalty2, Quartic, Rastrigin, SchwefelDouble, SchwefelMax, SchwefelAbs, SchwefelSin, Stairs, Abs, Michalewicz, Scheffer, Eggholder, Weierstrass, plot_3d


ackley = Ackley(2)
xmin, xmax, ymin, ymax = ackley.bounds
target = ackley.f_best
print(target)
print(ackley.bounds)
seed = 1
# full available functional of plotting

plot_3d(ackley, 
        points_by_dim = 70, 
        title = fr"{type(ackley).__name__}\ with\ seed = {seed}", # LaTeX formula notation
        bounds = None, 
        show_best_if_exists = True, 
        save_as = "Fletcher1.png",
        cmap = 'twilight',
        plot_surface = True,
        plot_heatmap = True)