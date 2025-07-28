from Force import Force 
from Constraint import Constraint
from Node import Node

Force_vector = [10, 20, 32]
Boundary_conditions = [True, False, True]

myForce = Force(Force_vector)
myConstraint = Constraint(Boundary_conditions)