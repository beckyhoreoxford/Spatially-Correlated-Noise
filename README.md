# Spatially-Correlated-Noise
Generating Spatially Correlated Noise for Computational Biological Simulations

The motivation for this project was to create random noise which could be applied to biological simulations which contained multiple points. An example of such a simulation would be cells in a jelly-like substance, and an example of the random noise could be a second less viscous chemical being added to the mixture which causes the cells to move in a certain direction at a certain speed. If two cells are close together, the second chemical should affect the cells in a similar way (ie the noise should be spatially corelated over small distances), and if the cells are far apart, the second chemical should have a random effect on the two cells (ie the noise should be normally distributed overall). Additionally, the existing solutions to this worked in quadratic time, which wasn't fast enough for anything other than toy simulations, so I was working to create something which could run fast even with many thousands of data points.

Over the course of this project, I investigated two different types of random noise, and tested the spatial correlation, overall distribution, and runtime. I completed a write-up of the project which is also included, and here is a summary of what each of the code files attached achieve:

PerlinNoise.py
Implementation of Perlin Noise.

GaussianNoise.py
Implementation of Gaussian Noise using kernel smoothing to achieve some level of spatial correlation.

TimeTests.py
Uses the python Time library to test runtime of different noise types.

DistributionTesting,py
Visually displays the distribution of a sample of random noise against the best fit normal distribution, using matplotlib for display purposes.

CorrelationTesting1/2.py
Tests the spatial correlation of a random noise to get a numerical value out for comparison.

Simulation.py
Test simulation of cells in a population, with random spatially correlated noise added.

SimulationHelperFns.py
Helper functions to run the simulation.

Write_Up.pdf
5,000 word documentation of the entire project.

Write Up.tex
LaTeX formatting of Write_Up.pdf.
