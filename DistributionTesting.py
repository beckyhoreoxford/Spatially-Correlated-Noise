import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
from PerlinNoise import *
from GaussianNoise import *

N = 100
f, axes = plt.subplots(2,3)
params = [5,50,250]
mus = np.zeros([2,len(params)])
stds = np.zeros([2,len(params)])

plt.suptitle("Visualising the Extent to which Perlin and Smooth Gaussian noises are Normally Distributed")
bins = 50

for i in range(len(params)):
    print(i)
    p_noise = perlin_noise(params[i], N).flatten()
    g_noise = gaussian_noise(params[i],N).flatten()   

    axes[0,i].set_title("Perlin Noise, Oct Size = {}".format(params[i]))

    axes[1,i].set_title("Smooth Gaussian Noise, k = {}".format(params[i]))

    #fit
    pmu, pstd = norm.fit(p_noise)
    gmu, gstd = norm.fit(g_noise)

    #plot histograms
    axes[0,i].hist(p_noise, bins = bins, density = True, color = "pink")
    axes[1,i].hist(g_noise, bins = bins, density = True, color = "skyblue")

    pxmin,pxmax = axes[0,i].get_xlim()
    gxmin,gxmax = axes[1,i].get_xlim()

    px = np.linspace(pxmin,pxmax,100)
    gx = np.linspace(gxmin,gxmax,100)

    pp = norm.pdf(px,pmu, pstd)
    gp = norm.pdf(gx,gmu,gstd)

    axes[0,i].plot(px,pp,color = "red")
    axes[1,i].plot(gx,gp, color = "blue")

plt.show()
