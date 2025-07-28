from Force import Force 
from Constraint import Constraint
from Node import Node

#Force_vector = [10, 20, 32]
#Boundary_conditions = [True, False, True]

#myForce = Force(Force_vector)
#myConstraint = Constraint(Boundary_conditions)
n1 = Node(0, 0, 0)
n1.set_force([10, 20, 30])
n1.set_constraint([True, True, False])
n1.enumerate_dof()
n1.set_displacement([0.1, 0.2, 0.3])



#n2 = Node(1, 2, 3)
#n2.set_force(Force([5, 15, 25]))
#n2.set_constraint(Constraint([False, True, False]))