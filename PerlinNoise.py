import math
import random
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import norm

#datatype having x and y values
class Coord:
    def __init__(self, x:float, y:float):
        self.x = x
        self.y = y

    def map(self, f):
        self.x = f(self.x)
        self.y = f(self.y)

    def get_bounds(self):
        lowerX_bound = math.floor(self.x)
        upperX_bound = math.floor(self.x + 1)
        lowerY_bound = math.floor(self.y)
        upperY_bound = math.floor(self.y + 1)
        return [lowerX_bound, upperX_bound, lowerY_bound,upperY_bound]
    
    def print(self):
        print("(", end = '')
        print(round(self.x,2), end = '')
        print(",", end = '')
        print(round(self.y,2), end = '')
        print(") ", end = '')

    def value(self):
        return self.x,self.y

    def getweight(self) -> float:
        return fade(1-abs(self.x))*fade(1-abs(self.y))

class Vec:
    def __init__(self, x:float, y:float):
        self.x = x
        self.y = y

    def print(self):
        print("(", end = '')
        print(round(self.x,2), end = '')
        print(",", end = '')
        print(round(self.y,2), end = '')
        print(") ", end = '')
    
    def value(self):
        return self.x,self.y
def halfzip(list:list[int]) -> list[Coord]:
    a,b,c,d = list
    return [Coord(a,c), Coord(a,d), Coord(b,c), Coord(b,d)]
#returns c1-c2
def subtract(c1:Coord, v2:Vec) -> Vec:
    x1,y1 = c1.value()
    x2,y2 = v2.value()
    return Coord(x1-x2, y1-y2)
def dot(v1:Vec, v2:Vec) -> float:
    x1,y1 = v1.value()
    x2,y2 = v2.value()
    return x1*x2 + y1*y2
#smoothes [0,1] value
def fade(given_value: float) -> float:
    if given_value < -0.1 or given_value > 1.1: 
        raise ValueError('expected to have value in [-0.1, 1.1]')
    return 6 * math.pow(given_value, 5) - 15 * math.pow(given_value, 4) + 10 * math.pow(given_value, 3)
#assume seed = 1, octaves = 1

class PerlinNoise:
    def __init__(self, octSize: float = 1, seed: int = 1):
        self.octSize: int = octSize
        self.seed: int = random.randint(1,100)
        self.cache: dict[Coord,Vec] = {}

    #returns noise values for a pair of coordinates
    def __call__(self, xy) -> float:
        x,y = xy
        coords = Coord(x,y)
        #working coordinates we're trying to find noise for: Coord
        coords.map(lambda x: x/self.octSize)

        #bounding box around working coordinates: List[Int]
        bounds = coords.get_bounds()
        #grid points surrounding working coordinates: List[Coord]
        gridpts = halfzip(bounds)
        #vector values corresponding to those gridpoints: List[Vec], vector distances between each grid point and the working coordinates: List[Vec]
        gridvecs = []
        dists = []
        for gridpt in gridpts:
            gridvecs.append(self.getvector(gridpt))
            dists.append(subtract(coords,gridpt))
        #vector weights between each grid point and the working coordinates: List[Float], ie how much this should count for, points further away get a smaller weight and v.v.
        weights = []
        for dist in dists:
            weights.append(dist.getweight())
        #weighted contributions of each grid point: List[Float]
        contributions = []
        for i in range(0,4):
            contributions.append(weights[i] * dot(gridvecs[i], dists[i]))
        return sum(contributions)
    def getvector(self, pt:Coord) -> Vec:
        if pt not in self.cache:
            self.cache[pt] = randVec(self.seed + hasher(pt))
        return self.cache[pt]
def hasher(coors: Coord) -> int:
    x,y = coors.value() 
    return max(1,int(abs(dot(coors, Coord(10**x, 10**y)) + 1,))    )
#returns normalised vector, always same for a given seed
def randVec(seed:int) -> Vec:
    st = random.getstate()
    random.seed(seed)
    vec = Vec(random.uniform(-1,1), random.uniform(-1,1))
    random.setstate(st) 
    #this line has to be included so that it always creates same random vector for same input
    return vec
#plots a noise against the normal distribution on a given set of axes

def perlin_noise(octSize, N):
    A = np.zeros([N,N])
    pn = PerlinNoise(octSize)
    for i in range(N):
        for j in range(N):
            A[i,j] = pn((i,j))
    return A
