class Constraint():
    
    def __init__(self, fix_x=False, fix_y=False, fix_z=False):
        """
        Initializes constraint for x, y, z directions.
        True = constrained (fixed)
        False = free
        """
        self.fixed = [fix_x, fix_y, fix_z]
    
    def get_values(self):
        return self.fixed

    def print(self):
        """
        Print the boundary conditions.
        """
        for i, val in enumerate(self.fixed, start=1):
            status = "fixed" if val else "free"
            print(f"Direction {i}: {status}")
        
