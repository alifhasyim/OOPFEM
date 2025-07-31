from Constraint import Constraint
from Force import Force
import numpy as np

class Node():
    def __init__(self, x1, x2, x3):
        """
        Initialize a Node object with a degree of freedom
        """
        # Set default values for position, displacement, constraint, force, and dof_number
        self.position = [x1, x2, x3]
        self.displacement = [0, 0, 0]
        self.constraint = [False, False, False]
        self.force = Force(0, 0, 0)
        self.dof_number = [0, 0, 0]
        # Print the node's coordinates
        #self.print()
  
    def __str__(self):
        return f"[{self.position[0]}, {self.position[1]}, {self.position[2]}]"
    
    def set_force(self, f1, f2, f3):
        """
        Set the force vector associated with the node.
        """
        self.force = Force(f1, f2, f3)
        return self.force

    def get_force(self):
        """
        Get the force vector associated with the node"
        """
        return self.force

    def set_constraint(self, boundary_conditions):
        """
        Set the boundary conditions for the node.
        """
        self.constraint = Constraint(boundary_conditions)
        return self.constraint
        
    def get_constraint(self):
        """
        Get the constraint associated with the node.
        """
        return self.constraint

    def enumerate_dof(self):
        """
        Enumerate the degrees of freedom for the node based on the False DOF.
        """
        # Assuming self.constraint.u1, u2, u3 are booleans: True if constrained, False if free
        self.dof_number = [
            0 if self.constraint.u1 else 1,
            0 if self.constraint.u2 else 1,
            0 if self.constraint.u3 else 1
        ]
        # Counts the number of degrees of freedom = number of non-fixed DOF
        #print(f"DOF number for node: {self.dof_number.count(1)}")
    
    def get_dof_number(self):
        """
        Get the degrees of freedom number for the node.
        """
        return self.dof_number
    
    def get_position(self):
        """
        Get the position of the node.
        """
        return self.position
    
    def set_displacement(self, displacement):
        """
        Set the displacement of the node.
        """
        dist = np.array(displacement)
        self.displacement = dist

    def get_displacement(self):
        """
        Get the displacement of the node.
        """
        return self.displacement
    
    def print(self):
        """
        Print the coordinates of the node.
        """
        print(f"Node coordinates: x={self.position.x}, y={self.position.y}, z={self.position.z}")
        