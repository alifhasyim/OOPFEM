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
        self._node_set = set()
        

    def __str__(self):
        return f"Structure with {len(self.nodes)} nodes and {len(self.elements)} elements."

    def add_node(self, x1, x2, x3):
        """
        Add a node to the structure.
        """
        single_nodal = Node(x1, x2, x3)
        self.nodes.append(single_nodal)
        self._node_set.add(single_nodal)
        print(single_nodal)
        return single_nodal
        
    
    def add_element(self, e_modulus, area, density, node1, node2):
        """
        Add an element to the structure.
        """
        single_element = Element(e_modulus, area, density, node1, node2)
        self.elements.append(single_element)
        self._node_set.add(node1)
        self._node_set.add(node2)
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
        Solve the reduced system only for free DOFs.
        """
        print("Solving structure...")
        
        # enumerate dof
        self.enumerate_dof()
        
        # Initialize stiffness matrix, mass matrix, and force vector
        n = self.num_dof
        if self.num_dof == 0:
            raise ValueError("DOF enumeration must be run before assembling stiffness matrix.")
        
        self.K_global = np.zeros((n, n))
        self.m_global = np.zeros((n, n))
        self.f_global = np.zeros((n, 1))
        
        # Loop for stiffness matrix
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
        
        # Loop for mass matrix
        for element in self.elements:
            m_local = element.compute_mass_matrix()  # 6x6
            dof_map = element.node1.dof_number + element.node2.dof_number  # length 6

            for i_local, i_global in enumerate(dof_map):
                if i_global == -1:
                    continue  # constrained DOF

                for j_local, j_global in enumerate(dof_map):
                    if j_global == -1:
                        continue
                    self.m_global[i_global, j_global] += m_local[i_local, j_local]
        
        # Loop for force vector
        for node in self.nodes:
            if node.force is None:
                continue
            for i, dof in enumerate(node.dof_number):
                if dof != -1:
                    self.f_global[dof] += node.force[i]
        
        # Identify free DOF indices
        free_dofs = []
        for node in self._node_set:
            for dof in node.dof_number:
                if dof != -1:
                    free_dofs.append(dof)

        # Convert to numpy arrays
        K_ff = self.K_global[np.ix_(free_dofs, free_dofs)]
        f_f = self.f_global[free_dofs]

        # Solve reduced system
        u_f = np.linalg.solve(K_ff, f_f)

        self.U_global = u_f

        # Fill full displacement vector with zeros initially
        full_disp = np.zeros((len(self.f_global), 1))

        for idx, dof in enumerate(free_dofs):
            full_disp[dof] = u_f[idx]

        self.displacement = full_disp

        # Assign displacements back to nodes
        for node in self._node_set:
            disp = []
            for dof in node.dof_number:
                if dof == -1:
                    disp.append(0.0)
                else:
                    disp.append(float(self.displacement[dof]))
            node.displacement = disp

        print("Nodal displacements:")
        print(self.displacement)

        # print("Nodal displacements:")
        # for i, node in enumerate(self.nodes):
        #     print(f"Node {i+1}: {self.displacement}")

    def enumerate_dof(self):
        """
        Enumerate global DOFs for all nodes in the structure.
        """
        print("Enumerating global DOFs...")
        counter = 0
        for node in self.nodes:
            for i in range(3):
                if node.constraint.fixed[i]:
                    node.dof_number[i] = -1
                else:
                    node.dof_number[i] = counter
                    counter += 1
        self.num_dof = counter
        return counter

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
        if self.num_dof == 0:
            raise ValueError("DOF enumeration must be run before assembling stiffness matrix.")
        
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
        print("My stiffness matrix:")
        df = pd.DataFrame(self.K_global)
        print(df)
        return self.K_global

    def assemble_mass_matrix(self):
        """
        Assembly the global mass matrix, which here are quite the same as the stiffness matrix
        assembly.
        """
        # Step 1: Enumerate dof
        self.enumerate_dof()
        # Step 2: Initialize global mass matrix
        n = self.num_dof
        self.m_global = np.zeros((n, n))
        if self.num_dof == 0:
            raise ValueError("DOF enumeration must be run before assembling stiffness matrix.")
        
        # Step 3: Loop over elements and assemble
        for element in self.elements:
            m_local = element.compute_mass_matrix()  # 6x6
            dof_map = element.node1.dof_number + element.node2.dof_number  # length 6

            for i_local, i_global in enumerate(dof_map):
                if i_global == -1:
                    continue  # constrained DOF

                for j_local, j_global in enumerate(dof_map):
                    if j_global == -1:
                        continue
                    self.m_global[i_global, j_global] += m_local[i_local, j_local]
        print("My mass matrix:")
        df = pd.DataFrame(self.m_global)
        print(df)
        
        return self.m_global
    
    def assemble_load_vector(self):
        """
        Assemble the global load vector for the structure.
        This is a placeholder for the actual assembly logic.
        """
        print("Assembling global load vector...")
        self.enumerate_dof()

        n = self.num_dof
        self.f_global = np.zeros((n, 1))

        for node in self.nodes:
            if node.force is None:
                continue
            for i, dof in enumerate(node.dof_number):
                if dof != -1:
                    self.f_global[dof] += node.force[i]
        print("My load vector:")
        df = pd.DataFrame(self.f_global)
        print(df)
        
        return self.f_global
        

    def select_displacement(self, node_index):
        """
        Select the displacement for a specific node.
        """
        if 0 <= node_index < len(self.nodes):
            print(self.nodes[node_index].displacement)
            return self.nodes[node_index].displacement
        else:
            raise IndexError("Node index out of range.")
    
    def initial_displacement(self):
        """
        Get the initial displacement vector for the structure.
        """
        return np.zeros((self.num_dof, 1))

    def initial_velocity(self):
        """
        Get the initial velocity vector for the structure.
        """
        return np.zeros((self.num_dof, 1))

    def print_results(self):
        """
        Print the results of the structure analysis.
        This is a placeholder for the actual result printing logic.
        """
        print("Results:")
        