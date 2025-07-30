from Node import Node
import numpy as np
class Element:
    
    def __init__(self, area, e_modulus, node1, node2):
        """
        Initialize an Element object with two nodes.
        """
        # Material properties
        self.area = area
        self.e_modulus = e_modulus
        #self.print_properties()
        
        # Set nodes
        self.node1 = node1
        self.node2 = node2
        #self.print_nodes()
    
    def __str__(self):
        return f"Element(area={self.area}, e_modulus={self.e_modulus}, node1={self.node1}, node2={self.node2})"
        
    
    def compute_stiffness_matrix(self, index=0):
        """
        Compute the stiffness matrix for the element.
        """
        if not isinstance(self.node1, Node) or not isinstance(self.node2, Node):
            raise ValueError("Both nodes must be instances of Node.")
        # Initialize a 2x2 stiffness matrix
        self.stiffness_matrix = np.array([[0, 0], [0, 0]])
        self.stiffness_matrix[0][0] = 1
        self.stiffness_matrix[0][1] = -1
        self.stiffness_matrix[1][0] = -1
        self.stiffness_matrix[1][1] = 1
        self.new_stiffness_matrix = self.stiffness_matrix * (self.e_modulus * self.area)/self.get_length()
        return self.new_stiffness_matrix
    
    def enumerate_dof(self):
        """
        Calculate the whole degrees of freedom for the element.
        """
    
    def compute_force(self):
        """"
        Compute the force vector for the element.
        """

    def get_modulus(self):
        """
        Get the elastic modulus of the element.
        """
        return self.e_modulus

    def get_length(self):
        """
        Get the length between two nodes.
        """
        # Determine the positions of the nodes
        pos1 = self.node1.get_position()
        pos2 = self.node2.get_position()
        # Calculate the differences in coordinates
        length = np.linalg.norm(np.subtract(pos2, pos1))
        # Calculate the length 
        return length
    
    def get_nodes(self):
        """
        Get the node of the object associated with the element.
        """
        return self.node1, self.node2
    
    def get_area(self):
        """
        Get the defined area. 
        """
        return self.area

    def get_modulus(self):
        """
        Get the elastic modulus of the element
        """
        return self.e_modulus
        
    
    def print_properties(self):
        """
        Print the properties of the element.
        """
        print("Element Properties:")
        print(f"Area: {self.area}")
        print(f"Elastic Modulus: {self.e_modulus}")

    def print_nodes(self):
        """
        Print the details of the element.
        """
        print(f"Element between Node 1 at {self.node1} and Node 2 at {self.node2}")