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
        self.constraint = Constraint(False, False, False)
        self.force = Force(0, 0, 0)
        self.dof_number = [0, 0, 0]
        # Print the node's coordinates
        #self.print()
  
    def __str__(self):
        return f"[{self.position[0]}, {self.position[1]}, {self.position[2]}]"
    
    def __hash__(self):
        return hash(tuple(self.position))

    def __eq__(self, other):
        return isinstance(other, Node) and self.position == other.position
    
    def set_force(self, force: Force):
        """
        Set the force vector associated with the node.
        """
        if not isinstance(force, Force):
            raise TypeError("Expected a Force object.")
        self.force = force
        return self.force

    def get_force(self):
        """
        Get the force vector associated with the node"
        """
        return self.force.get_values()

    def set_constraint(self, boundary_conditions: Constraint):
        """
        Set the boundary conditions for the node.
        """
        if not isinstance(boundary_conditions, Constraint):
            raise TypeError("Expected a constraint object.")
        self.constraint = boundary_conditions
        return self.constraint
        
    def get_constraint(self):
        """
        Get the constraint associated with the node.
        """
        return self.constraint

    def enumerate_dof(self, counter):
        """
        Enumerate the DOFs for this node, using `-1` for constrained DOFs
        and incrementing the global counter for free DOFs.
        """
        print(f"Enumerating DOF for node at {self.position} with constraint: {self.constraint.fixed}")
        for i, is_constrained in enumerate(self.constraint.fixed):
            if is_constrained:
                self.dof_number[i] = -1
            else:
                self.dof_number[i] = counter
                counter += 1
        print(f"Assigned DOF numbers: {self.dof_number}")
        return counter
    
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
        