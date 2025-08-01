from Visualizer import Visualizer
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
c1 = Constraint(True, True, True)
c2 = Constraint(False, False, False)

# Set up force
f1 = Force(0, -20e3, -100e3)


## Create nodes
n1 = struct.add_node(0.0, 0.0, lb*mat.sqrt(2.0 / 3.0))
n2 = struct.add_node(0.0, lb/mat.sqrt(3), 0)
n3 = struct.add_node(-lb/2, -lb/mat.sqrt(12.0), 0)
n4 = struct.add_node(lb/2, -lb/mat.sqrt(12.0), 0)

## Apply BCs
n1.set_force(f1)
n1.set_constraint(Constraint(True, True, False))
n2.set_constraint(Constraint(True, True, True))  # fixed
n3.set_constraint(Constraint(True, True, True))  # fixed
n4.set_constraint(Constraint(True, True, True))  # fixed again, new instance

## Create elements
element1 = struct.add_element(e, a, n1, n2)
element2 = struct.add_element(e, a, n1, n3)
element3 = struct.add_element(e, a, n1, n4)
element4 = struct.add_element(e, a, n2, n3)
element5 = struct.add_element(e, a, n3, n4)
element6 = struct.add_element(e, a, n4, n2)


for i, node in enumerate(struct.nodes):
    print(f"Node {i+1} constraint.fixed = {node.constraint.fixed}")
## Enumerate DOF (must happen before printing them)
struct.enumerate_dof()

## Now safe to print
for i, node in enumerate(struct.nodes):
    print(f"Node {i+1} DOF numbers: {node.dof_number}")
    
# Compute Stiffness matrix 
for i, element in enumerate([element1, element2, element3, element4, element5, element6], start=1):
    k_e = element.compute_stiffness_matrix()
    print(f"Element {i} stiffness matrix:")
    element.print_stiffness_matrix()

# Compute force vector
element1.compute_force()

# Assemble stiffness matrix
struct.assemble_stiffness_matrix()

# Assemble load vector matrix
struct.assemble_load_vector()

# Solve the Matrix problem
struct.solve()

# Select displacement
struct.select_displacement(1)

## Visualize element
vis = Visualizer([element1, element2, element3, element4, element5, element6])
plotter = pv.Plotter()
vis.draw_elements(plotter)
vis.draw_constraint(plotter)
vis.draw_nodal_forces(plotter)
vis.draw_displacement(plotter)
plotter.view_isometric()
plotter.show_axes()
plotter.show()





