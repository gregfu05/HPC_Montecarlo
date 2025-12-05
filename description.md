Our group plans to develop a Monte Carlo Energy Optimization simulation, inspired by molecular modeling. The goal is to find the lowest-energy configuration of a simple molecule represented as a set of atoms connected by bonds.

Each atom has a position in 3D space, and the total energy depends on how stretched or compressed the bonds are. We will use a Monte Carlo (Metropolis) algorithm with simulated annealing to randomly explore different molecular configurations. In each iteration, a small random move is applied to an atom, the new energy is calculated, and the move is accepted or rejected based on the change in energy and temperature.

The project is suitable for an HPC environment because it is embarrassingly parallel, each node or process can run an independent simulation with different random seeds and initial conditions. We will measure strong and weak scaling, parallel efficiency, and perform profiling to identify bottlenecks (e.g., computation vs. communication).

As an optimization step, we plan to implement neighbor lists to reduce the computational cost of energy calculations or experiment with overlapping communication and computation when aggregating results across nodes.

This project combines a clear scientific concept with straightforward parallelism, allowing us to demonstrate correctness, scalability, and performance analysis within the scope of the course.