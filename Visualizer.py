from matplotlib.pyplot import step
import pyvista as pv
import numpy as np
from moviepy import VideoFileClip
from pathlib import Path

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
                    
    def post_processing(self, plotter, displacement):
        
        forces = []
        line_all = []
        
        for element in self.element:
            nodes = element.get_nodes()

            # Original and displaced positions
            pos0 = np.array(nodes[0].position)
            pos1 = np.array(nodes[1].position)
            disp0 = np.array(nodes[0].displacement)
            disp1 = np.array(nodes[1].displacement)

            pos0_def = pos0 + self.scale * disp0
            pos1_def = pos1 + self.scale * disp1
            # Compute force
            f_local = element.compute_internal_force(displacement)
            f_axial = f_local # Axial force
            forces.append(f_axial)
            
            ## Original
            #plotter.add_mesh(pv.Line(pos0, pos1), color='gray', line_width=2, label="Original")

            # Deformed
            line_individual = pv.Line(pos0_def, pos1_def)
            line_all.append(line_individual)
    
            #plotter.add_mesh(pv.Line(pos0_def, pos1_def), color='red', line_width=4, label="Deformed")
        
        # Combine all line into one mesh
        multi_block = pv.MultiBlock(line_all)
        combined = multi_block.combine()
        
        # Assign axial forces as scalar values
        force_array = np.array(forces)
        combined["AxialForce"] = np.repeat(force_array, len(combined.points) // len(forces))
        
        plotter.add_mesh(
            combined,
            scalars="AxialForce",
            line_width=10, 
            cmap="jet",  
            show_scalar_bar=True,
            scalar_bar_args={"title": "Axial Force"},
            lighting=False,
        )
    
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
    
    
    def animate_displacement(self, plotter, displacement_history, time_history):
        """
            _summary_
        Animate the structure's deformation over time, coloring elements by axial force.
        Parameters:
        1. plotter: pyvista.Plotter object for rendering
        2. displacement_history: 2D numpy array of shape (num_dofs, num_time_steps)
        3. time_history: 1D numpy array of time steps corresponding to displacement_history
        """
        def apply_displacement(pos, disp, scale=0.05):
            """_summary_

            Args:
                pos (_type_): _description_
                disp (_type_): _description_
                scale (float, optional): _description_. Defaults to 0.05.

            Returns:
                _type_: _description_
            """
            disp_full = np.zeros_like(pos)
            if disp.size > 0:
                disp_full[:len(disp)] = disp
            return pos + scale * disp_full

        # Here we store the displacement history 
        num_steps = displacement_history.shape[1]

        # --- Build initial multiblock from last step's displacement (or t=0 if you prefer) ---
        multi_block = []
        forces = []

        # Initialize node displacements 
        for node in self.nodes:
            node.displacement = np.array([
                displacement_history[d, num_steps - 1] if d != -1 else 0.0
                for d in node.dof_number
            ])

        for element in self.element:
            nodes = element.get_nodes()
            pos0 = np.array(nodes[0].position)
            pos1 = np.array(nodes[1].position)

            disp0 = np.array(nodes[0].displacement)
            disp1 = np.array(nodes[1].displacement)

            # pad to coordinates length
            disp0_full = np.zeros_like(pos0); disp0_full[:len(disp0)] = disp0
            disp1_full = np.zeros_like(pos1); disp1_full[:len(disp1)] = disp1

            pos0_def = pos0 + self.scale * disp0_full
            pos1_def = pos1 + self.scale * disp1_full

            # compute element force at first time (or whichever baseline you want)
            f_local = element.compute_internal_force(displacement_history[:, 0])
            forces.append(f_local)

            multi_block.append(pv.Line(pos0_def, pos1_def))

        multi_block_mesh = pv.MultiBlock(multi_block)
        combined = multi_block_mesh.combine()

        # create per-point scalar array (2 point entries per element)
        combined["AxialForce"] = np.array([f for f in forces for _ in range(2)])

        # STEP 1: Compute global color limits (symmetric around zero)
        all_forces = []
        for step in range(num_steps):
            step_forces = [element.compute_internal_force(displacement_history[:, step])
                        for element in self.element]
            all_forces.extend(step_forces)
        all_forces = np.asarray(all_forces)
        absmax = np.max(np.abs(all_forces)) if all_forces.size > 0 else 1.0
        clim_factor = 1.0
        clim = (-clim_factor * absmax, clim_factor * absmax)

        # STEP 2: Initial plot with first time step
        init_forces = np.array([element.compute_internal_force(displacement_history[:, 0])
                                for element in self.element])
        # After combine(), assign cell_data (not point_data)
        combined = multi_block_mesh.combine()
        combined.cell_data["AxialForce"] = init_forces

        actor = plotter.add_mesh(
            combined,
            scalars="AxialForce",
            line_width=10,
            cmap="jet",
            show_scalar_bar=True,
            scalar_bar_args={"title": f"Axial Force | Time {time_history[0]:.4f} s"},
            lighting=False,
            clim=list(clim),
        )
        scalar_bar_actor = plotter.scalar_bar

        # Sanity print
        print("Initial: n_points=", combined.n_points, "n_cells=", combined.n_cells,
            "cell_scalars_len=", combined.cell_data["AxialForce"].size)

        # STEP 3: Animation loop (use cell_data) 
        for step in range(1, num_steps):
            forces = []

            # Update node displacements
            for node in self.nodes:
                node.displacement = np.array([
                    displacement_history[d, step] if d != -1 else 0.0
                    for d in node.dof_number
                ])

            # Move each line’s endpoints
            for i, element in enumerate(self.element):
                nodes = element.get_nodes()
                pos0_def = apply_displacement(np.array(nodes[0].position),
                                            np.array(nodes[0].displacement), self.scale)
                pos1_def = apply_displacement(np.array(nodes[1].position),
                                            np.array(nodes[1].displacement), self.scale)
                multi_block[i].points[:] = [pos0_def, pos1_def]

                f_local = element.compute_internal_force(displacement_history[:, step])
                forces.append(f_local)

            # Combine MultiBlock and assign cell scalars (one per element/cell)
            combined = multi_block_mesh.combine()
            per_cell_forces = np.array(forces)  # length should equal number of elements/cells
            combined.cell_data["AxialForce"] = per_cell_forces

            # Update mapper input and force it to use cell data for coloring
            actor.mapper.SetInputData(combined)

            # Tell mapper to use cell data scalars
            try:
                # Prefer VTK-style calls (works with PyVista/VTK)
                actor.mapper.SetScalarModeToUseCellData()
            except Exception:
                # Fallback: use PyVista mapper API
                actor.mapper.SetScalarMode(1)  # 1 == use cell data in VTK

            actor.mapper.SelectColorArray("AxialForce")
            actor.mapper.ScalarVisibilityOn()
            actor.mapper.SetScalarRange(clim[0], clim[1])  # keep fixed range

            # Update scalar bar title
            if scalar_bar_actor:
                scalar_bar_actor.SetTitle(f"Axial Force | Time {time_history[step]:.4f} s")

            plotter.render()
            plotter.write_frame()
            
    def gif_to_mp4_moviepy(gif_path, output_path=None):
        gif_path = Path(gif_path)
        if output_path is None:
            output_path = gif_path.with_suffix(".mp4")
        
        clip = VideoFileClip(str(gif_path))
        clip.write_videofile(str(output_path), codec="libx264")
        print(f"Converted {gif_path} → {output_path}")