from Structure import Structure

import pyvista as pv
import numpy as np
from Visualizer import Visualizer as Vis


# Create a structure and add nodes
Structure1 = Structure()
n1 = Structure1.add_node(0, 0, 0)
n2 = Structure1.add_node(5, 0, 0)
n3 = Structure1.add_node(5, 0, 0)
n4 = Structure1.add_node(0, 0, 5)

# Create two elements
element1 = Structure1.add_element(10, 10, n1, n2)
element2 = Structure1.add_element(2, 1, n3, n4)
print(f"This is element 1 properties: {element1}")
print(f"This is element 2 properties: {element2}")
print(f"This is node 1 in element 1: {element1.node1}")
print(f"This is the data type of node 1 in element1 : {type(element1.node1)}")
print(f"This is node 2 in element 1: {element1.node2}")

# Node 1
print(f"This is node 1: {n1}")
constraint_n1 = n1.set_constraint([True, True, True])
print(f"This is constraint n1 = {constraint_n1}")

# Node 2
print(f"This is node 2: {n2}")
constraint_n2 = n2.set_constraint([True, False, True])

# Node 3
print(f"This is node 3: {n3}")
constraint_n3= n3.set_constraint([True, False, True])

# Node 4 
print(f"This is node 4: {n4}")
constraint_n4 = n4.set_constraint([True, True, True])

# Information about the structure
print(f"This is structure 1: {Structure1}")

# Compute stiffness matrices for elements
stiffness_matrix1 = element1.compute_stiffness_matrix()
length1 = element1.get_length()
print(f"Local stiffness matrix for element 1: (local) {stiffness_matrix1} with length {length1}")
stiffness_matrix2 = element2.compute_stiffness_matrix()
length2 = element2.get_length()
print(f"Local stiffness matrix for element 2: (local) {stiffness_matrix2} with length {length2}")

# new_n1 = tuple(element1.node1.get_position())
# new_n2 = tuple(element1.node2.get_position())
# new_n3 = tuple(element2.node1.get_position())
# new_n4 = tuple(element2.node2.get_position())

# element1 = pv.Line(new_n1, new_n2)
# element2 = pv.Line(new_n3, new_n4)
# plotter = pv.Plotter()
# plotter.add_mesh(element1, color='k', line_width=10)
# plotter.add_mesh(element2, color='r', line_width=10)
# plotter.show()
vis = Vis([element1, element2])
plotter = pv.Plotter()
vis.draw_elements(plotter)
vis.draw_constraint(plotter)
plotter.view_isometric()
plotter.show_axes()
plotter.show()







# edges = np.array([
#     [0, 1],
#     [1, 2],  
#     [2, 3]  
# ])

# padding = np.empty(edges.shape[0], int) * 2
# padding[:] = 2
# edges_w_padding = np.vstack((padding, edges.T)).T


# mesh = pv.PolyData(nodes, edges_w_padding)

# colors = range(edges.shape[0])
# mesh.plot(
#     scalars=colors,
#     render_lines_as_tubes=True,
#     style='wireframe',
#     line_width=10,
#     cmap='jet',
#     show_scalar_bar=False,
#     background='w',
# )





