from Node import Node
from Element import Element
from Structure import Structure

# Node 1
n1 = Node(0, 0, 0)
n1.set_constraint([True, False, True])
# Node 2
n2 = Node(1, 0, 0)
n2.set_constraint([False, True, False])

# Node 3
n3 = Node(0, 1, 0)
n3.set_constraint([False, False, True])

# Node 4 
n4 = Node(1, 10, 0)
n4.set_constraint([False, True, False])

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






