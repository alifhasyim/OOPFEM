from Node import Node
from Element import Element
from Structure import Structure

import pyvista as pv
import numpy as np

# Node 1
n1 = Node(0, 0, 0)
print(f"This is node 1: {n1}")
constraint_n1 = n1.set_constraint([True, False, True])
print(f"This is constraint n1 = {constraint_n1}")

# Node 2
n2 = Node(5, 0, 0)
print(f"This is node 2: {n2}")
constraint_n2 = n2.set_constraint([False, True, False])

# Node 3
n3 = Node(0, 5, 0)
print(f"This is node 3: {n3}")
constraint_n3= n3.set_constraint([False, False, True])

# Node 4 
n4 = Node(0, 0, 0)
print(f"This is node 4: {n4}")
constraint_n4 = n4.set_constraint([False, True, False])

# Create a structure and add nodes
Structure1 = Structure()
Structure1.add_node(n1)
Structure1.add_node(n2)
Structure1.add_node(n3)
Structure1.add_node(n4)

# Create elements and add them to the structure
element1 = Structure1.add_element(Element(10, 10, n1, n2))

print(f"This is element 1 properties: {element1}")
element2 = Structure1.add_element(Element(2, 1, n3, n4))
print(f"This is element 2 properties: {element2}")

# Information about the structure
print(f"This is structure 1: {Structure1}")

# Compute stiffness matrices for elements
stiffness_matrix1 = element1.compute_stiffness_matrix()
length1 = element1.get_length()
print(f"Local stiffness matrix for element 1: (local) {stiffness_matrix1} with length {length1}")
stiffness_matrix2 = element2.compute_stiffness_matrix()
length2 = element2.get_length()
print(f"Local stiffness matrix for element 2: (local) {stiffness_matrix2} with length {length2}")


nodes = [n.coord for n in Structure1.nodes]

edges = np.array([
    [0, 1],
    [1, 2],  
    [2, 3]  
])

padding = np.empty(edges.shape[0], int) * 2
padding[:] = 2
edges_w_padding = np.vstack((padding, edges.T)).T
edges_w_padding

mesh = pv.PolyData(nodes, edges_w_padding)

colors = range(edges.shape[0])
mesh.plot(
    scalars=colors,
    render_lines_as_tubes=True,
    style='wireframe',
    line_width=10,
    cmap='jet',
    show_scalar_bar=False,
    background='w',
)





