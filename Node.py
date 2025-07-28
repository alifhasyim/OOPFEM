from Constraint import Constraint
from Force import Force
from Vector3D import Vector3D

class node():
    def __init__(self, x1, x2, x3):
        """
        Initialize a Node object with a degree of freedom
        """
        self.position = Vector3D(x1, x2, x3)
        self.displacement = Vector3D()
        self.constraint = None
        self.force = None
        self.dof_number = [0, 0, 0]

    def set_force(self, force_vector):
        """
        Set the force vector associated with the node.
        """
        if not isinstance(force_vector, Force):
            raise ValueError("Force must be a Force object.")
        self.force = force_vector

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
        if not isinstance(boundary_conditions, Constraint):
            raise ValueError("Boundary conditions must be a Constraint object.")
        self.constraint = boundary_conditions
        
    def get_constraint(self):
        """
        Get the constraint associated with the node.
        """
        if self.constraint is None:
            raise ValueError("No constraint associated with this node.")
        return self.constraint

    def enumerate_dof(self, dof_number)
        """
        Enumerate the degrees of freedom for the node.
        """
        dof_number = [1, 2, 3] if dof_number is None else dof_number
        if len(dof_number) != 3:
            raise ValueError("DOF number must have three components.")
        self.dof_number = dof_number
    
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
        if not isinstance(displacement, Vector3D):
            raise ValueError("Displacement must be a Vector3D object.")
        self.displacement = displacement

    def get_displacement(self):
        """
        Get the displacement of the node.
        """
        return self.displacement
    
    def print(self):
        """
        Print the coordinates of the node.
        """
        print(f"Node coordinates: x={self.x}, y={self.y}, z={self.z}")
