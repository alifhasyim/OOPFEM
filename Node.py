from Constraint import Constraint
from Force import Force
from Vector3D import Vector3D

class Node():
    def __init__(self, x1, x2, x3):
        """
        Initialize a Node object with a degree of freedom
        """
        # Set default values for position, displacement, constraint, force, and dof_number
        self.position = Vector3D(x1, x2, x3)
        self.displacement = Vector3D()
        self.constraint = None
        self.force = None
        self.dof_number = [0, 0, 0]
        # Print the node's position
        self.print()

    def set_force(self, force_vector):
        """
        Set the force vector associated with the node.
        """
        vector = Force(force_vector)
        if not isinstance(vector, Force):
            raise ValueError("Force must be a Force object.")
        self.force = vector

    def get_force(self):
        """
        Get the force vector associated with the node"
        """
        if self.force is None:
            raise ValueError("No force vector associated with this node.")
        return self.force

    def set_constraint(self, boundary_conditions):
        """
        Set the boundary conditions for the node.
        """
        dof = Constraint(boundary_conditions)
        if not isinstance(dof, Constraint):
            raise ValueError("Constraint must be a Constraint object.")
        self.constraint = dof
        

    def get_constraint(self):
        """
        Get the constraint associated with the node.
        """
        if self.constraint is None:
            raise ValueError("No constraint associated with this node.")
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
        print(f"DOF number for node: {self.dof_number.count(1)}")
    
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
        dist = Vector3D(displacement[0], displacement[1], displacement[2])
        if not isinstance(dist, Vector3D):
            raise ValueError("Displacement must be a Vector3D object.")
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
