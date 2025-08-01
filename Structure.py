from Node import Node
from Element import Element
import numpy as np
import pandas as pd

class Structure:
    def __init__(self):
        """
        Initialize a Structure object with empty lists for nodes and elements.
        """
        self.nodes = []
        self.elements = []

    def __str__(self):
        return f"Structure with {len(self.nodes)} nodes and {len(self.elements)} elements."

    def add_node(self, x1, x2, x3):
        """
        Add a node to the structure.
        """
        single_nodal = Node(x1, x2, x3)
        self.nodes.append(single_nodal)
        return single_nodal
        
    
    def add_element(self, area, e_modulus, node1, node2):
        """
        Add an element to the structure.
        """
        single_element = Element(area, e_modulus, node1, node2)
        self.elements.append(single_element)
        return single_element

    def get_number_of_nodes(self):
        """
        Get the number of nodes in the structure.
        """
        self.num_nodes = len(self.nodes)
        return self.num_nodes

    def get_number_of_elements(self):
        """
        Get the number of elements in the structure.
        """
        return len(self.elements)

    def get_element(self, index):
        """
        Get an element by its index.
        """
        if index < 0 or index >= len(self.elements):
            raise IndexError("Element index out of range.")
        return self.elements[index]

    def print_structure(self):
        """
        Print the structure's nodes and elements.
        """
        print("Nodes:")
        for node in self.nodes:
            print(node)
        
        print("Elements:")
        for element in self.elements:
            print(element)

    def solve(self):
        """
        Solve the structure's equations.
        This is a placeholder for the actual solving logic.
        """
        print("Solving structure...")
        # Implement the solving logic here
        # This could involve assembling global stiffness matrices, applying boundary conditions, etc.
        self.displacement = np.linalg.inv(self.K_global) @ self.f_global
        print("Nodal displacements:")
        print(self.displacement)

    def enumerate_dof(self):
        """
        Enumerate global DOFs for all nodes in the structure.
        """
        counter = 0
        for node in self.nodes:
            counter = node.enumerate_dof(counter)
        self.num_dof = counter

    def assemble_stiffness_matrix(self):
        """
        Assemble the global stiffness matrix for the structure.
        This is a placeholder for the actual assembly logic.
        """
        print("Assembling global stiffness matrix...")
        # Implement the assembly logic here
        # This could involve iterating over elements and nodes to build the global stiffness matrix
        # Step 1: Enumerate DOFs
        self.enumerate_dof()

        # Step 2: Initialize global stiffness matrix
        n = self.num_dof
        self.K_global = np.zeros((n, n))
        
        # Step 3: Loop over elements and assemble
        for element in self.elements:
            k_local = element.compute_stiffness_matrix()  # 6x6
            dof_map = element.node1.dof_number + element.node2.dof_number  # length 6

            for i_local, i_global in enumerate(dof_map):
                if i_global == -1:
                    continue  # constrained DOF

                for j_local, j_global in enumerate(dof_map):
                    if j_global == -1:
                        continue
                    self.K_global[i_global, j_global] += k_local[i_local, j_local]
        df = pd.DataFrame(self.K_global)
        print(df)

    def assemble_load_vector(self):
        """
        Assemble the global load vector for the structure.
        This is a placeholder for the actual assembly logic.
        """
        print("Assembling global load vector...")
        # Implement the assembly logic here
        # This could involve summing forces from all nodes into a global load vector
        self.enumerate_dof()
        
        n = self.num_dof
        self.f_global = np.zeros((n, 1))
        
        for element in self.elements:
            f_local = element.compute_force()
            dof_map = element.node1.dof_number + element.node2.dof_number
            
            for k_local, k_global in enumerate(dof_map):
                if k_global == -1:
                    continue
                self.f_global[k_global] += f_local[k_local]
        df = pd.DataFrame(self.f_global)
        print(df)

    def select_displacement(self, node_index):
        """
        Select the displacement for a specific node.
        """
        

    def print_results(self):
        """
        Print the results of the structure analysis.
        This is a placeholder for the actual result printing logic.
        """
        print("Results:")
        