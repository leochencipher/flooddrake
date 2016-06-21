
from __future__ import division  # Get proper divison

import math
import random

import numpy as np


from firedrake import *

from flooddrake import *

""" demo file for simple 1d shallow water equations for dam break"""


# Meshsize

n = 10
mesh = UnitIntervalMesh(n)

# mixed function space
X = FunctionSpace(mesh, "DG", 1)
Y = FunctionSpace(mesh, "DG", 1)
V = X * Y


# for slope limiter
XCG = FunctionSpace(mesh, "CG", 1)
YCG = FunctionSpace(mesh, "CG", 1)
VCG = XCG * YCG 


# setup free surface depth
g = interpolate(Expression(
    ['pow(x[0]-0.8,2)< 0.01 ? 2 : (pow(x[0]-0.8,2) < 0.01 ? -1.0 : 1)', 0]), V)

# setup bed

# pointless trivial second dimension
bed = interpolate(Expression(["x[0]*2", 0]), V)


# setup actual depth
w = g.assign(g - bed)

# setup source (is only a depth function)
source = interpolate(Expression("0"),X)



# timestep

solution = Timestepper(V, VCG, bed, source, 0.025)

solution.stepper(0, 0.75, w)
