class Force():
    def __init__(self, vector):
        """"
        Initialize a Force object with a vector.
        """
        self.r1 = vector[0]
        self.r2 = vector[1]
        self.r3 = vector[2]
        self.print()

        # Error handling
        if len(vector) != 3:
            raise ValueError("Force vector must have three components.")
        elif len(vector) > 3:
            raise ValueError("Force vector must have exactly three components.")
        elif not all(isinstance(val, (int, float)) for val in vector):
            raise ValueError("All force vector values must be numeric.")
    
    def print(self):
        """"
        Print the force vector.
        """
        print("Force vector:")
        print(self.r1, self.r2, self.r3)