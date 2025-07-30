class Constraint():
    
    all_constraint = []
    
    def __init__(self, boundary):
        if len(boundary) != 3:
            raise ValueError("Constraint requires three boolean values.")
        self.u1 = boundary[0]  # Constrain in x
        self.u2 = boundary[1]  # Constrain in y
        self.u3 = boundary[2]  # Constrain in z
        #self.print()
        # Error handling
        if len(boundary) != 3:
            raise ValueError("Boundary conditions must have three components.")
        elif not all(isinstance(val, bool) for val in boundary):
            raise ValueError("All boundary values must be boolean.")
        Constraint.all_constraint.append(self)
    
    def __str__(self):
        return f"[{self.u1}, {self.u2}, {self.u3}]"

    def print(self):
        """
        Print the boundary conditions.
        """
        for i, val in enumerate([self.u1, self.u2, self.u3], start=1):
            status = "fixed" if val else "free"
            print(f"Direction {i}: {status}")
        
