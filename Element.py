from Node import Node
import pandas as pd
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
        
    
    def compute_stiffness_matrix(self):
        """
        Compute the 6x6 stiffness matrix for a 3D truss element using dyadic form.
        """
        x1 = np.array(self.node1.get_position())
        x2 = np.array(self.node2.get_position())

        # Element length
        L_vec = x2 - x1
        L = np.linalg.norm(L_vec)

        if L == 0:
            raise ValueError("Element length is zero — nodes are overlapping.")

        # Unit direction vector
        direction = L_vec / L

        # Outer product (3x3)
        outer = np.outer(direction, direction)

        # Scale factor
        scale = (self.e_modulus * self.area) / L

        # Assemble the 6x6 stiffness matrix
        # Using block matrix form:
        # [ K  -K ]
        # [ -K  K ]

        K = scale * outer  # 3x3 local stiffness

        k_global = np.block([
            [ K, -K],
            [-K,  K]
        ])

        self.stiffness_matrix = k_global
        return k_global
    
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
        
    def print_stiffness_matrix(self):
        k = self.compute_stiffness_matrix()
        df = pd.DataFrame(k)
        print("Element Stiffness Matrix [k]:")
        print(df.round(3))