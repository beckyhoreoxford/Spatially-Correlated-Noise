import math
import numpy as np
import random

def size(coord):
    x,y = coord
    return math.sqrt(x*x + y*y)
    
class Cell:
    def __init__(self, x:float, y:float, id:int, r:float):
        self.x = x
        self.y = y
        self.id = id
        self.r = r

class Pair:
    def __init__(self, x:float, y:float):
        self.x = x
        self.y = y
    def printPair(self):
        return ("({},{})".format(self.x,self.y))

def create_Cells(n, N, minRadius, maxRadius):
    pairs = []
    while(len(pairs)!=n):
        x = np.random.randint(0,N)
        y = np.random.randint(0,N)
        if (x,y) not in pairs:
            pairs.append((x,y))
    i = 0
    C = []
    for x,y in pairs:
        r = np.random.uniform(minRadius,maxRadius)
        c = Cell(x,y, i, r)

        C.append(c)
        i+=1
    return C
def unit(coord):
    if coord == (0,0):
        return (0,0)
    x,y = coord
    sz = size(coord)
    return (x/sz,y/sz)

def F(I, J, maxRadius, mu, kc):
    #print("{},{}: ".format(I.id,J.id), end  ='')
    if (I == J):
        #print("same node, force = (0,0)")
        return Pair(0,0)
    ri = (I.x,I.y)
    rj = (J.x,J.y)
    sij = I.r+J.r       #natural separation between cell I and J
    rij = (I.x-J.x, I.y-J.y)         #distance between cells
    

    #too far away, no attraction or repulsion
    if size(rij) > maxRadius:
        #print("far away, force = (0,0)")
        return Pair(0,0)
    
    urij = unit(rij)
    #if too close together, repel
    if size(rij) < sij:
        frac = (size(rij) - sij)/sij
        const = mu*sij*math.log(1+frac)
        urijx,urijy = urij
        ans = Pair(urijx*const, urijy*const)
        #print("too close, force = {}".format(ans.printPair()))

        return ans

    #if apart but not too far, attract
    frac = (size(rij)-sij)/sij
    exponential = math.exp(-kc*frac)
    const = mu*(size(rij)-sij)*exponential
    urijx,urijy = urij
    ans = Pair(urijx*const,urijy*const)
    #print("far, force = {}".format(ans.printPair()))

    return ans

def Cells_to_Coords(C, n):
    xs = []
    ys = []
    rs = []
    for i in range(n):
        xs.append(C[i].x)
        ys.append(C[i].y)
        rs.append(C[i].r*100)
    return xs,ys,rs

def update_cells(forces,C,n,t, cellSpeed):
    xForce = 0
    yForce = 0
    for i in range(n):
        for j in range(n):
            xForce += forces[i,j].x
            yForce += forces[i,j].y
        C[i].x += xForce*t*cellSpeed
        C[i].y += yForce*t*cellSpeed
        xForce = 0
        yForce = 0
    return C

def add_noise(C, PNx, PNy, n,N, noiseSize,cellSpeed):
    for i in range(n):
        xNoise = PNx((C[i].x/N, C[i].y/N))
        yNoise = PNy((C[i].x/N, C[i].y/N))
        C[i].x += random.uniform(-1,1)
        C[i].y += random.uniform(-1,1)
        #C[i].x += xNoise*noiseSize*cellSpeed
        #C[i].y += yNoise*noiseSize*cellSpeed
    return C

