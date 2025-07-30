import pyvista as pv

#boundary_n1 = [True, False, True]
#boundary_n2 = [False, True, False]

#n1 = Node(0, 0, 0)
#n1.set_constraint(boundary_n1)
#n2 = Node(1, 0, 0)
#n2.set_constraint(boundary_n2)

#Bar1 = Element(1,1,n1,n2)

#l1 = Bar1.get_length()

# Structure1 = Structure()
# n1 = Node(0, 0, 0)
# constraint1= n1.set_constraint([True, False, True])
# n2 = Node(1, 0, 0)
# n2.set_constraint([False, True, False])
# Structure1.add_node(n1)
# Structure1.add_node(n2)


# element1 = Structure1.add_element(Element(1, 1, n1, n2))
# print(f"This is node 1 constraint: {constraint1}")
# print(f"This is node 2: {n2}")
# print(f"This is element 1: {element1}")

# n3 = Node(0, 1, 0)
# n3.set_constraint([False, False, True])
# Structure1.add_node(n3)
# n4 = Node(1, 1, 0)
# n4.set_constraint([False, True, False])
# Structure1.add_node(n4)

# element2 = Structure1.add_element(Element(2, 1, n3, n4))
# print(f"This is element 2: {element2}")
# print(f"This is structure 1: {Structure1}")

cone = pv.Cone()


p = pv.Plotter()

p.add_mesh(cone, color='lightblue', show_edges=True)
p.show()
