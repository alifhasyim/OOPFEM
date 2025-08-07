from Visualizer import Visualizer
from Structure import Structure
from Constraint import Constraint
from Force import Force

import pyvista as pv
import math as mat

struct = Structure()

## Properties information
# Young's modulus
e_modulus = 2.1e11
# Area
r = 0.01
area = mat.pi * mat.pow(r, 2)
# Density
density = 1000

## Constraint
c1 = Constraint(True, True, True)
c2 = Constraint(True, True, True)
# for 2D constraint
c_2D = Constraint(False, False, True)

# Set up force
f1 = Force (0, -100e3, 0)

## Geometry
l = 1/2 * mat.sqrt(3)
n1 = struct.add_node(0.0, 0.0, 0.0)
n2 = struct.add_node(0.5, l, 0.0)
n3 = struct.add_node(1.0, 0.0, 0.0)
n4 = struct.add_node(1.5, l, 0.0) 
n5 = struct.add_node(2.0, 0.0, 0.0)
n6 = struct.add_node(2.5, l, 0.0)
n7 = struct.add_node(3.0, 0.0, 0.0) 

## Apply force and bc
n4.set_force(f1)
n4.set_constraint(c_2D)
n1.set_constraint(c1)
n7.set_constraint(c2)
n2.set_constraint(c_2D)
n3.set_constraint(c_2D)
n5.set_constraint(c_2D)
n6.set_constraint(c_2D)


## Create elements
element1 = struct.add_element(e_modulus, area, density, n1, n2)
element2 = struct.add_element(e_modulus, area, density, n1, n3)
element3 = struct.add_element(e_modulus, area, density, n2, n3)
element4 = struct.add_element(e_modulus, area, density, n2, n4)
element5 = struct.add_element(e_modulus, area, density, n3, n4)
element6 = struct.add_element(e_modulus, area, density, n3, n5)
element7 = struct.add_element(e_modulus, area, density, n4, n5)
element8 = struct.add_element(e_modulus, area, density, n4, n6)
element9 = struct.add_element(e_modulus, area, density, n5, n6)
element10 = struct.add_element(e_modulus, area, density, n5, n7)
element11 = struct.add_element(e_modulus, area, density, n6, n7)

for i, node in enumerate(struct.nodes):
    print(f"Node {i+1} constraint.fixed = {node.constraint.fixed}")
## Enumerate DOF (must happen before printing them)
#struct.enumerate_dof()
print("Try to compute the mass matrix of element1")
#m1 = element1.compute_mass_matrix()
## Now safe to print
#for i, node in enumerate(struct.nodes):
    #print(f"Node {i+1} DOF numbers: {node.dof_number}")
    
# Compute Stiffness matrix 
# for i, element in enumerate([element1, element2, element3, element4, element5, element6, 
#                              element7, element8, element9, element10, element11], start=1):
#     k_e = element.compute_stiffness_matrix()
#     print(f"Element {i} stiffness matrix:")
#     element.print_stiffness_matrix()

# Compute force vector
#element1.compute_force()

# Assemble stiffness matrix
struct.assemble_stiffness_matrix()

# Assemble load vector matrix
struct.assemble_load_vector()

# Assemble mass matrix
struct.assemble_mass_matrix()

# Solve the Matrix problem
struct.solve()

## Visualize element
vis = Visualizer([element1, element2, element3, element4, element5, element6, 
                            element7, element8, element9, element10, element11])
plotter = pv.Plotter()
vis.draw_elements(plotter)
vis.draw_constraint(plotter)
vis.draw_nodal_forces(plotter)
vis.post_processing(plotter, struct.displacement)
plotter.view_isometric()
plotter.show_axes()
plotter.show()
