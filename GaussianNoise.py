import numpy as np
import scipy.signal
import matplotlib.pyplot as plt
import math
import random
from scipy.stats import norm, entropy
from scipy import stats

#-------------------------------------------------
#PARAMETERS FOR EDITING
mean, std_dev = 0, 1
#k  = 1
#n = 100
#-------------------------------------------------

class Gaussian:
    def __call__(self,m,s) -> float:
        s = self.normal_dist(m,s)
        return s

    def normal_dist(self, m,s):
        #s = random.uniform(-1,1)
        s = np.random.normal(m,s)
        return s

def create_filter(k):
    scale = math.ceil(k/2)
    x = np.arange(-scale, scale)
    y = np.arange(-scale, scale)
    X,Y = np.meshgrid(x,y)
    dist = np.sqrt(X**2 + Y**2)
    filter = np.exp(-dist**2/(2*scale))
    return filter

def smooth(noise, k):
    filter_kernel = create_filter(k)
    return np.array(scipy.signal.fftconvolve(noise,filter_kernel, mode = 'same'))

def gaussian_noise(k,n):
    noise = Gaussian()
    A = np.zeros([n,n])
    for x in range(n):
        for y in range(n):
            A[x,y] = noise(mean, std_dev)

    A = smooth(A, k)

    return A


