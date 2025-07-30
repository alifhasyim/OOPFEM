from Force import Force 
from Constraint import Constraint
from Node import Node
from Element import Element

boundary_n1 = [True, False, True]
boundary_n2 = [False, True, False]

n1 = Node(0, 0, 0)
n1.set_constraint(boundary_n1)
n2 = Node(1, 0, 0)
n2.set_constraint(boundary_n2)
Bar1 = Element(1,1,n1,n2)
Bar1.get_length()

