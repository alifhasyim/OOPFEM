from Node import Node
from Element import Element

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
        return len(self.nodes)

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
        pass

    def enumerate_dof(self):
        """
        Enumerate the degrees of freedom for all nodes in the structure.
        """
        dof_list = []
        for node in self.nodes:
            dof = node.enumerate_dof()
            dof_list.extend(dof)
        return dof_list

    def assemble_stiffness_matrix(self):
        """
        Assemble the global stiffness matrix for the structure.
        This is a placeholder for the actual assembly logic.
        """
        print("Assembling global stiffness matrix...")
        # Implement the assembly logic here
        # This could involve iterating over elements and nodes to build the global stiffness matrix
        pass

    def assemble_load_vector(self):
        """
        Assemble the global load vector for the structure.
        This is a placeholder for the actual assembly logic.
        """
        print("Assembling global load vector...")
        # Implement the assembly logic here
        # This could involve summing forces from all nodes into a global load vector
        pass

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
        