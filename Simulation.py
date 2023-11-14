import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math
from scipy.interpolate import LinearNDInterpolator
from scipy import interpolate
from matplotlib.widgets import Slider, Button, TextBox
from PerlinNoise import *
from SimulationHelperFns import *

global c
global C
global n
global PNx
global PNy
global newn
global mu
global kc
global t
global noiseSize
global cellSpeed

N = 100 #size of grid
init_n = 50 #number of points
n = init_n
init_cellSpeed = 1
cellSpeed = init_cellSpeed
init_noiseSize = 1
noiseSize = init_noiseSize
newn = n
C = []
maxRadius = 6
minRadius = 2
init_mu = 0.05
mu = init_mu #spring constant, controls size of force
init_kc = 1
kc = init_kc #defines decay of attractive force
init_t = 0.5
t = init_t #percentage of a second each timestep takes
init_octaves = 4
octaves = init_octaves
#light to dark
colorpallete = ['#f2f4f9','#b8d1ff','#c2cee5','#51a2da']
COL = colorpallete[3]
COL2 = colorpallete[2]
COLinnerbg = colorpallete[1]
COLbg = colorpallete[0]

PNx = PerlinNoise(init_octaves,1)
PNy = PerlinNoise(init_octaves,2)

fig, ax = plt.subplots()
fig.subplots_adjust(left = 0.25, bottom = 0.3)
ax.set_xlim(0,N)
ax.set_ylim(0,N)
#ax.set_title("Cell Behaviour with Random Noise", fontsize = 20)
ax.set_xticks([])
ax.set_yticks([])
ax.set_facecolor(COLinnerbg)
fig.set_facecolor(COLbg)
plt.setp(ax.spines.values(), color = COL2, linewidth = 4)


#octave changing
axOctaves = fig.add_axes([0.25,0.25,0.65,0.03])
OctSlider = Slider(
    ax = axOctaves,
    label = "Number of Octaves",
    valmin = 1,
    valmax = 10,
    valinit = init_octaves,
    initcolor = 'none',
    color = COL2,
    track_color = COL2,
)
def updateOctaves(val):
    octaves = OctSlider.val
    global PNx
    global PNy
    PNx = PerlinNoise(octaves, 1)
    PNy = PerlinNoise(octaves,2)
OctSlider.on_changed(updateOctaves)

#noise size
axNoiseSize = fig.add_axes([0.25,0.2,0.65,0.03])
NoiseSlider = Slider(
    ax = axNoiseSize,
    label = "Noise Effect",
    valmin = 0,
    valmax = 10,
    valinit = init_noiseSize,
    initcolor = 'none',
    color = COL2,
    track_color = COL2,
)
def updateNoiseSize(val):
    global noiseSize
    noiseSize = val
NoiseSlider.on_changed(updateNoiseSize)

#mu
axMu = fig.add_axes([0.25,0.15, 0.65,0.03])
MuSlider = Slider(
    ax = axMu,
    label = "Mu (Spring Constant)",
    valmin = 0,
    valmax = 1,#play around
    valinit = init_mu,
    initcolor = 'none',
    color = COL2,
    track_color = COL2,
)
def updateMu(val):
    global mu
    mu = MuSlider.val
MuSlider.on_changed(updateMu)

#kc
axKC = fig.add_axes([0.25,0.1,0.65,0.03])
KCSlider = Slider(
    ax = axKC,
    label = "KC (attraction decay)",
    valmin = 0,
    valmax = 10, #play around
    valinit = init_kc,
    initcolor = 'none',
    color = COL2,
    track_color = COL2,
)
def updateKC(val):
    global kc
    kc = KCSlider.val
KCSlider.on_changed(updateKC)

#cell speed
axCellSpeed = fig.add_axes([0.25,0.05,0.65,0.03])
cellSpeedSlider = Slider(
    ax = axCellSpeed,
    label = "Cell Speed",
    valmin = 0,
    valmax = 10, #play around
    valinit = init_cellSpeed,
    initcolor = 'none',
    color = COL2,
    track_color = COL2,
)
def updateCellSpeed(val):
    global cellSpeed
    cellSpeed = cellSpeedSlider.val
cellSpeedSlider.on_changed(updateCellSpeed)



#adding new cells
axNewCell = fig.add_axes([0.1,0.3, 0.09, 0.05])
bNewCell = Button(axNewCell, "Add", color = COL2)
def add_cell(val):
    global newn
    xs,ys,rs = Cells_to_Coords(C,n)
    pairs = []
    for i in range(n):
        pairs.append((xs[i],ys[i]))
    added = False
    while not added:
        x = np.random.randint(0,N)
        y = np.random.randint(0,N)
        r = np.random.uniform(minRadius,maxRadius)
        if (x,y) not in pairs:
            newCell = Cell(x,y,n,r)
            C.append(newCell)
            newn += 1
            added = True
bNewCell.on_clicked(add_cell)

def update_n():
    global n
    n = newn

def animate(i):
    global C
    update_n()
    forces = []
    for x in range(n):
        for y in range(n):
            forces.append(F(C[x], C[y], maxRadius, mu, kc))

    forces = np.reshape(forces, (n,n))

    update_cells(forces,C,n,t, cellSpeed)
    PNx = PerlinNoise(octaves, 1)
    PNy = PerlinNoise(octaves,2)
    add_noise(C,PNx, PNy, n,N, noiseSize, cellSpeed)
    xs,ys,rs = Cells_to_Coords(C,n)

    line = ax.scatter(xs,ys, s = rs, c = COL, alpha = 0.6)
    return line,

def init():
    global C
    update_n()

    C = create_Cells(n,N, minRadius, maxRadius)

    xs,ys,rs = Cells_to_Coords(C,n)
    line = ax.scatter(xs,ys ,s= rs, c = COL, alpha = 0.8)
    return line,

#start button
axStart = fig.add_axes([0.1,0.35, 0.09, 0.05])
bStart = Button(axStart, "Start", color = COL2)
def start(val):
    ani = animation.FuncAnimation(fig,animate,np.arange(1,200), init_func = init, interval = 1000*t, blit = True)
    plt.show()  
    bStart.set_active(False)
bStart.on_clicked(start)

#get input values for time and number of circles
#time changing
axTime = fig.add_axes([0.1,0.45,0.09,0.03])
TimeSlider = Slider(
    ax = axTime,
    label = "Time scale",
    valmin = 0,
    valmax = 1,
    valinit = init_t,
    initcolor = 'none',
    color = COL2,
    track_color = COL2,
)
def updateTime(val):
    global t
    t = val
TimeSlider.on_changed(updateTime)


fig.text(0.08,0.55, "Population A", fontsize = 12)

#n changing
axn = fig.add_axes([0.1,0.5,0.09,0.03])
nSlider = Slider(
    ax = axn,
    label = "No of Cells",
    valmin = 0,
    valmax = 1000,
    valstep = 10,
    valinit = init_n,
    initcolor = 'none',
    color = COL2,
    track_color = COL2,
)
def updaten(val):
    global newn
    newn = val
nSlider.on_changed(updaten)

plt.show()