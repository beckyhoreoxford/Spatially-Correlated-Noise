import numpy as np
import matplotlib.pyplot as plt
from GaussianNoise import *
from PerlinNoise import *

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
    f_ds.append(f(0))
    vals = []
    founds = np.zeros((len(rs)), dtype=bool)
    for i in range(len(rs)):
        vals.append(None)

    vals[0] = 0

    d = 0
    while(d < N and not founds[len(rs)-1]):
        f_d = f(d)
        i = 1
        for i in range(1,len(rs)):
            if (not founds[i] and f_d < f_ds[0]*rs[i]/100):
                vals[i] = d-1
                founds[i] = True
        f_ds.append(f_d)
        d+=1

    return vals

def get_noise(noisetype, N, ok):
    if noisetype == "g":
        return gaussian_noise(ok, N)
    elif noisetype == "p":
        return perlin_noise(ok,N)
    else:
        print("ERROR, noisetype != perlin|gaussian")


nt = "p"
N = 100
stepsize = 10
t = 5
params = np.arange(1,N,stepsize)
rs = [100,90,75,50,25,10,0]

rvals = np.zeros([len(params),len(rs)])

if nt == "g":
    paramtype = "Octave Size"
    noisename = "Perlin"
else:
    paramtype = "K"
    noisename = "Gaussian"

for i in range(len(params)):
    print(params[i])
    noise = get_noise(nt, N, params[i])
    vs = []
    for j in range(t):
        print(t)
        vs += FastCorrelationFactor(noise)

    rvals[i] = vs
    
rvals = np.rot90(np.fliplr(rvals))
print(rvals)

for i in range(len(rvals)):
    plt.scatter(params, rvals[i], color = colors[i], marker = "x")
    a,b = np.polyfit(params,rvals[i],1)
    plt.plot(params, a*params+b, color = colors[i],label = "r{}".format(rs[i]))

