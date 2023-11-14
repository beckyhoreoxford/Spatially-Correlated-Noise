import numpy as np
import matplotlib.pyplot as plt
from GaussianNoise import *
from PerlinNoise import *
import random

n = 100
rs = [100,90,75,50,25,10,0]
colors = ['#66c2a5','#fc8d62','#8d9fca','#e789c2','#a5d853','#ffd82f','#e5c494']

def FastCorrelationFactor(noise):
    N = len(noise)
    def f(d):
        total,sumSq = 0,0
        for x in range(N):
            for y in range(N):
                xD = min(N-1,x+d)
                yD = min(N-1,y+d)
                dNoise = noise[x,yD] + noise[xD,y]
                total += noise[x,y]*dNoise
                sumSq += noise[x,y]**2
        f_d = total/(2*sumSq)
        return f_d

    f_ds = []
    ds = np.arange(1,N)
    f_ds.append(f(0))
    vals = []
    founds = np.zeros((len(rs)), dtype=bool)
    for i in range(len(rs)):
        vals.append(None)

    vals[0] = 0

    for d in ds:
        f_d = f(d)
        for i in range(1,len(rs)):
            if (not founds[i] and f_d < f_ds[0]*rs[i]/100):
                vals[i] = d-1
                founds[i] = True
        f_ds.append(f_d)
    ds = np.concatenate(([0],ds))

    plt.plot(ds, f_ds)
    return vals

#noisetype = "perlin"|"gaussian", N = size of output, ok = #octaves|k value
#output: return 2D array of perlin noise
def get_noise(noisetype, N, ok = 1):
    if noisetype == "gaussian":
        return gaussian_noise(ok, N)
    elif noisetype == "perlin":
        gen = PerlinNoise(ok)
        noise = np.zeros([N,N])
        for i in range(N):
            for j in range(N):
                noise[i,j] = gen((i/N,j/N))
        return noise
    elif noisetype == "random":
        noise = np.zeros([N,N])
        for i in range(N):
            for j in range(N):
                noise[i,j] = random.uniform(-1,1)
        return noise
    else:
        print("ERROR, noisetype != perlin|gaussian")

N = 250
oct = 1.25
k = 100

A = get_noise("perlin", N,oct)
B = get_noise("gaussian", N, k)
C = get_noise("random", N)
#plt.imshow(C)
plt.show()

rvalues = FastCorrelationFactor(B)
for i in range(len(rs)):
    if rvalues[i] != None:
        plt.axvline(rvalues[i], color = colors[i], label = "r{} = {}".format(rs[i], rvalues[i]))
    print("r value {} = {}".format(rs[i], rvalues[i]))


#plt.title("R Values of Random Noise")
plt.title("R Values of Gaussian Noise (k = {})".format(k))
plt.xlabel("Distance")
plt.ylabel("Spatial Correlation")

plt.legend(loc="upper right")
plt.show()

