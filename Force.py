class Force():
    def __init__(self, r1, r2, r3):
        """"
        Initialize a Force object with a vector.
        """
        self.force = [r1, r2, r3]
        if len(self.force) != 3:
            raise ValueError("Force vector must have exactly three components.")
        if not all(isinstance(val, (int, float)) for val in self.force):
            raise ValueError("All force components must be numeric.")
    
    def get_values(self):
        return self.force
        
    def print(self):
        """"
        Print the force vector.
        """
        print(f"Force vector: {self.force[0]}, {self.force[1]}, {self.force[2]}")