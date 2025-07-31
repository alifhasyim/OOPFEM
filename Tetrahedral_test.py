from Visualizer import Visualizer as vis
from Structure import Structure
from Constraint import Constraint
from Force import Force

import pyvista as pv
import math as mat
import numpy as np

struct = Structure()
# Dimensional information
lb = 15.0
r = 457.2 / 2000
t = 10 / 1000
a = mat.pi * (mat.pow(r,2) - mat.pow(r-t,2))
e = 2.1e11

# Constraint
c1 = Constraint(False, False, False)
c2 = Constraint(True, True, False)

# Set up force
f1 = Force(0, -20e3, -100e3)


## Create nodes
n1 = struct.add_node(0.0, 0.0, lb*mat.sqrt(2.0 / 3.0))
n2 = struct.add_node(0.0, lb/mat.sqrt(3), 0)
n3 = struct.add_node(-lb/2, -lb/mat.sqrt(12.0), 0)
n4 = struct.add_node(lb/2, -lb/mat.sqrt(12.0), 0)

## Apply BCs
n1.set_force(f1)



