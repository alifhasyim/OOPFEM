from Node import Node 
class Element:
    def __init__(self, node1, node2):
        """
        Initialize an Element object with two nodes.
        """
        self.node1 = node1
        self.node2 = node2
        self.print()

    def print(self):
        """
        Print the details of the element.
        """
        print(f"Element between Node 1 at {self.node1.position} and Node 2 at {self.node2.position}")