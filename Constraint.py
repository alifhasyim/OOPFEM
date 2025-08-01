class Constraint():
    
    def __init__(self, u1, u2, u3):
        self.boundary = [u1, u2, u3]
        #self.print()
        # Error handling
        if len(self.boundary) != 3:
            raise ValueError("Boundary conditions must have three components.")
        elif not all(isinstance(val, bool) for val in self.boundary):
            raise ValueError("All boundary values must be boolean.")
    
    def get_values(self):
        return self.boundary

    def print(self):
        """
        Print the boundary conditions.
        """
        for i, val in enumerate([self.u1, self.u2, self.u3], start=1):
            status = "fixed" if val else "free"
            print(f"Direction {i}: {status}")
        
