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
        #self.print_propwhereerties()
        
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

        k_local = np.block([
            [ K, -K],
            [-K,  K]
        ])

        self.stiffness_matrix = k_local
        return k_local
    
    def enumerate_dof(self):
        """
        Calculate the whole degrees of freedom for the element.
        """
        return self.node1.dof_number + self.node2.dof_number
    
    def compute_force(self):
        """"
        Compute the force vector for the element.
        """
        # Get the force from 
        f1 = np.array(self.node1.get_force()).reshape(-1, 1)
        f2 = np.array(self.node2.get_force()).reshape(-1, 1)
        
        f_local = np.block([[f1], [f2]])
        
        self.force_vector = f_local
        return f_local

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
    
    def transformation_matrix(self):
        """
        Compute the 6x6 transformation matrix for a 3D truss element.
        Maps global coordinates to local coordinates (x' along the element axis).
        """
        # Get node coordinates
        x1, y1, z1 = self.node1.position
        x2, y2, z2 = self.node2.position

        # Element direction vector
        dx = x2 - x1
        dy = y2 - y1
        dz = z2 - z1
        L = np.sqrt(dx**2 + dy**2 + dz**2)
        
        if L == 0:
            raise ValueError("Element has zero length")

        # Direction cosines
        l = dx / L
        m = dy / L
        n = dz / L

        # Construct transformation matrix
        T = np.zeros((6, 6))
        
        # Fill 3x3 rotation block (for each node)
        T_local = np.array([
            [l, m, n],
            [0, 0, 0],
            [0, 0, 0]
        ])  # Only the axial direction matters in truss

        T[0:3, 0:3] = np.array([
            [l, m, n],
            [0, 0, 0],
            [0, 0, 0]
        ])
        T[3:6, 3:6] = T[0:3, 0:3]  # Same rotation for node2

        # But to be correct in general, use identity for full transformation along element axis
        direction_cosines = np.array([l, m, n])
        R = np.zeros((3, 6))
        R[0, 0:3] = direction_cosines
        R[1, 3:6] = -direction_cosines

        # Full transformation matrix for axial deformation:
        # T = [ l m n  0 0 0
        #       0 0 0  l m n ]
        T = np.zeros((6, 6))
        T[0:3, 0:3] = np.eye(3)
        T[3:6, 3:6] = np.eye(3)

        return T
        
    
    def compute_internal_force(self, U_global):
        """
        Compute internal force vector in local coordinates.
        """
        # Get DOF mapping
        dof_map = self.node1.dof_number + self.node2.dof_number  # 6 DOFs

        # Extract global displacement vector for this element
        u_global = np.zeros(6)
        for i, dof in enumerate(dof_map):
            if dof != -1:
                u_global[i] = U_global[dof]

        # Transform to local coordinate system
        T = self.transformation_matrix()  # 6x6
        u_local = T @ u_global

        # Compute local stiffness matrix
        k_local = self.compute_stiffness_matrix()  # 6x6 in local coords

        # Compute internal force vector (in local coords)
        f_local = k_local @ u_local
        return f_local
    
    

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