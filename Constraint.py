class Constraint():
    def __init__(self, boundary):
        self.u1 = float(boundary[0])
        self.u2 = float(boundary[1])
        self.u3 = float(boundary[2])
        self.print()
        # Error handling
        if len(boundary) != 3:
            raise ValueError("Boundary conditions must have three components.")
        elif not all(isinstance(val, bool) for val in boundary):
            raise ValueError("All boundary values must be boolean.")

    def print(self):
        """
        Print the boundary conditions.
        """
        for i, val in enumerate([self.u1, self.u2, self.u3], start=1):
            status = "fixed" if val else "free"
            print(f"Direction {i}: {status}")
        
