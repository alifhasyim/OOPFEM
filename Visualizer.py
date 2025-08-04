import pyvista as pv
import numpy as np
from Structure import Structure

class Visualizer:
    def __init__(self, elements: list, scale=100.0):
        self.element = elements
        self.scale = scale
        # Extract unique nodes from elements (order preserved)
        seen = set()
        self.nodes = []
        for elem in elements:
            for node in elem.get_nodes():
                if node not in seen:
                    seen.add(node)
                    self.nodes.append(node)
       
    
    def draw_elements(self, plotter):
        
        for elem in self.element:
            nodes = [np.array(node.get_position()) for node in elem.get_nodes()]
            line = pv.Line(nodes[0], nodes[1])
            plotter.add_mesh(line, color='grey', line_width=5)
        
    
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
                constraint = np.array(node.get_constraint().get_values())   

                for i, is_constrained in enumerate(constraint):
                    if is_constrained:
                        direction = np.array(direction_vectors[i])
                        # Offset cone so all 3 aren't at same spot
                        center = pos + direction * -0.1
                        cone = pv.Cone(center=center, direction=direction, 
                                       height=self.scale*0.5/200, radius=self.scale*0.1/200)
                        plotter.add_mesh(cone, color=colors[i])
    
    def draw_nodal_forces(self, plotter):
        """
        Draw the element force based on the nodal information.
        """
        for elem in self.element:
            nodes = elem.get_nodes()
            for node in nodes:
                position = np.array(node.get_position())
                force_raw = node.get_force()
                force = np.array(force_raw)

                if np.allclose(force, [0, 0, 0]):
                    None
                else:
                    arrow = pv.Arrow(start=position, 
                                     direction=force, 
                                     tip_length=0.1, 
                                     tip_radius=0.1, 
                                     scale=0.5)
                    plotter.add_mesh(arrow, color='yellow')
                    
    def draw_displacement(self, plotter):
        
        for element in self.element:
            nodes = element.get_nodes()

            # Original and displaced positions
            pos0 = np.array(nodes[0].position)
            pos1 = np.array(nodes[1].position)
            disp0 = np.array(nodes[0].displacement)
            disp1 = np.array(nodes[1].displacement)

            pos0_def = pos0 + self.scale * disp0
            pos1_def = pos1 + self.scale * disp1

            # Original
            plotter.add_mesh(pv.Line(pos0, pos1), color='gray', line_width=2, label="Original")

            # Deformed
            plotter.add_mesh(pv.Line(pos0_def, pos1_def), color='red', line_width=4, label="Deformed")
    
        plotter.add_legend()
    
    def draw_axial_forces(self, plotter, displacement):
        """
        Draw 2D rectangular patches (squares) for each element, colored by axial force.
        """
        rectangles = []
        forces = []

        half_width = 0.1  # Half-thickness of the square in the perpendicular direction

        for elem in self.element:
            node_pos = [np.array(node.get_position()) for node in elem.get_nodes()]
            start, end = node_pos

            # Compute force
            f_local = elem.compute_internal_force(displacement)
            f_axial = f_local # Axial force
            forces.append(f_axial)

            # Compute the direction vector of the element
            vec = end - start
            length = np.linalg.norm(vec)
            if length == 0:
                continue
            direction = vec / length

            # Compute a perpendicular vector (2D only)
            perp = np.array([-direction[1], direction[0], 0.0])
            perp = perp / np.linalg.norm(perp)
            
            offset_distance = 0.1
            shift = offset_distance * perp

            # Define 4 corner points of a rectangle (square strip)
            p1 = start + half_width * perp + shift
            p2 = start - half_width * perp + shift
            p3 = end - half_width * perp + shift
            p4 = end + half_width * perp + shift

            # Build the quad (single face of 4 points)
            points = np.array([p1, p2, p3, p4])
            faces = [4, 0, 1, 2, 3]  # Quad with 4 points
            rect = pv.PolyData(points, faces)

            rectangles.append(rect)

        # Combine all rectangles into one mesh
        multi_block = pv.MultiBlock(rectangles)
        combined = multi_block.combine()

        # Assign axial forces as scalar values
        force_array = np.array(forces)
        combined["AxialForce"] = np.repeat(force_array, len(combined.points) // len(forces))

        # Add to plotter
        plotter.add_mesh(
            combined,
            scalars="AxialForce",
            cmap="jet",  
            show_scalar_bar=True,
            scalar_bar_args={"title": "Axial Force"},
            lighting=False,
        )