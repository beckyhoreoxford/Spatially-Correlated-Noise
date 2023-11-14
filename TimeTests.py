import time
from PerlinNoise import *
from GaussianNoise import *
import numpy as np
import matplotlib.pyplot as plt

def p_noise(octSize,n):
    noise = PerlinNoise(octSize)
    A = np.zeros([n,n])
    for x in range(n):
        for y in range(n):
            A[x,y] = noise((x,y))
    return A

def g_noise(k,n):
    noise = Gaussian()
    A = np.zeros([n,n])
    for x in range(n):
        for y in range(n):
            A[x,y] = noise(mean, std_dev)
    A = smooth(A, k)
    return A
 
#octave size and k [0-N] on x axis and time on y
def time_test1(stepSize, N, maxparam, noisetype):
    if noisetype == "P":
        name = "Perlin"
        parameterName = "Octave Size"
        get_noise = p_noise
    else:
        name = "Gaussian"
        parameterName = "k"
        get_noise = g_noise
    xs = np.arange(1,maxparam,stepSize)

    times = []
    for x in xs:
        print(x)

        start = time.time()
        get_noise(x,N)
        end = time.time()
        times.append(end-start)

    a,b,c = np.polyfit(xs,times,2)
    print(a,b,c)
    plt.scatter(xs,times, color = "red", alpha = 0.75, marker = '.')
    #plt.plot(xs, a*xs*xs+b*xs+c, linestyle = '--', color = "pink")
    #plt.legend(loc = "upper left")
    plt.title("Time tests for {} noise, ranging {}".format(name,parameterName))
    plt.ylabel("Time taken (s)")
    plt.xlabel(parameterName)

    plt.show()

#n on x axis [0-500] and time on y
def time_test2(stepSize, defParam, maxN, noisetype ):
    if noisetype == "P":
        name = "Perlin"
        parameterName = "Octave Size"
        get_noise = p_noise
    else:
        name = "Gaussian"
        parameterName = "k"
        get_noise = g_noise
    ns = np.arange(1,maxN,stepSize)
    times = []
    for n in ns:
        print(n)
        start = time.time()
        get_noise(defParam,n)
        end = time.time()
        times.append(end-start)

    a,b,c = np.polyfit(ns,times,2)
    print(a,b,c)
    plt.plot(ns,a*ns*ns+b*ns+c, linestyle = '--', color = "pink")

    plt.scatter(ns,times, color = 'red', alpha = 0.75, marker = ".")

    #plt.legend(loc = "upper left")
    plt.title("Time tests for {} noise, ranging N".format(name))
    plt.ylabel("Time taken (s) to generate a N by N grid of {} noise".format(name))
    plt.xlabel("N")

    plt.show()
    
stepSize = 10
defN = 500
maxparam = 1500

defParam = 500
maxN = 1500

time_test1(stepSize, defN, maxparam, "G")
time_test2(stepSize,defParam,maxN,"G")
