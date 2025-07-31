class Force():
    def __init__(self, r1: float, r2: float, r3:float):
        """"
        Initialize a Force object with a vector.
        """
        self.force = [r1, r2, r3]
        #self.print()

        # Error handling
        if len(self.force) != 3:
            raise ValueError("Force vector must have three components.")
        elif len(self.force) > 3:
            raise ValueError("Force vector must have exactly three components.")
        elif not all(isinstance(val, (int, float)) for val in self.force):
            raise ValueError("All force vector values must be numeric.")
    
    def get_values(self):
        return self.force
        
    def print(self):
        """"
        Print the force vector.
        """
        print("Force vector:")
        print(self.r1, self.r2, self.r3)