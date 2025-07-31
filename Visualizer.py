import pyvista as pv
import numpy as np

class Visualizer:
    def __init__(self, element: list):
        self.element = element
        return
    
    def draw_elements(self, plotter):
        
        for elem in self.element:
            nodes = [np.array(node.get_position()) for node in elem.get_nodes()]
            line = pv.Line(nodes[0], nodes[1])
            plotter.add_mesh(line, color='black', line_width=5)
        
    
    def draw_constraint(self, plotter):
        direction_vectors = {
            0: (1, 0, 0),  # x
            1: (0, 1, 0),  # y
            2: (0, 0, 1),  # z
        }
        colors = {
        0: 'red',
        1: 'green',
        2: 'blue'
        }

        for elem in self.element:
            nodes = elem.get_nodes()
            
            for node in nodes:
                pos = np.array(node.get_position())  # Assuming 3D coords
                constraint_raw = node.get_constraint()   
                constraint = constraint_raw.get_values()

                for i, is_constrained in enumerate(constraint):
                    if is_constrained:
                        direction = np.array(direction_vectors[i])
                        # Offset cone so all 3 aren't at same spot
                        center = pos + direction * -0.2
                        cone = pv.Cone(center=center, direction=direction, height=0.5, radius=0.1)
                        plotter.add_mesh(cone, color=colors[i])
    
    def draw_element_Forces(self):
        return
    
    def draw_dipslacement(self):
        return