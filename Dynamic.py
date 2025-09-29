from Structure import Structure
import numpy as np
import matplotlib.pyplot as plt

class dynamic:
    def __init__(self, structure):
        """
        Dynamic solver setup.
        """
        self.structure = structure

        # 1. Enumerate DOFs first so all assembly uses the same global numbering
        self.structure.enumerate_dof()   # ensures node.dof_number[] is set

        # 2. Assemble matrices with this DOF map
        self.M = self.structure.assemble_mass_matrix()
        self.K = self.structure.assemble_stiffness_matrix()
        self.R = self.structure.assemble_load_vector()

        # 3. Store DOF mapping info, not just a count
        self.num_dof = self.structure.num_dof  # integer count
        self.dof_map = [node.dof_number for node in self.structure.nodes]

        # 4. Initial conditions
        self.initial_displacement = self.structure.initial_displacement()
        self.initial_velocity = self.structure.initial_velocity()

    def generalized_alpha(self, initial_step, initial_time, final_time,
                          alpha_1=0.01, alpha_2=0.02, rho=0.9):

        # Time stepping parameters
        dt = initial_step
        t = initial_time
        t_end = final_time

        # Dynamic response parameters
        p = rho

        # Allowable error boundaries
        v1 = 0.5
        v2 = 1
        ne = 1e-2

        # Construct matrices and force vector
        M = self.M
        K = self.K
        C = alpha_1 * M + alpha_2 * K

        R = np.array(self.R)   # ensure it's an ndarray
        R0 = R[:, 0].ravel()   # first load vector

        # Newmark parameters
        alpha_m = (2 * p - 1) / (p + 1)
        alpha_f = p / (p + 1)
        B = 0.25 * (1 - alpha_m + alpha_f) ** 2
        G = 0.5 - alpha_m + alpha_f

        # Determine total steps
        n_steps = int(np.ceil((t_end - t) / dt)) + 1

        # Preallocate arrays
        u = np.zeros((self.num_dof, n_steps))
        v = np.zeros((self.num_dof, n_steps))
        a = np.zeros((self.num_dof, n_steps))
        r_eff = np.zeros((self.num_dof, n_steps))
        e = np.zeros((self.num_dof, n_steps))

        et = np.zeros(n_steps)
        cet = np.zeros(n_steps)
        tn = np.zeros(n_steps)
        dtn = np.zeros(n_steps)

        # Initial conditions
        u[:, 0] = self.initial_displacement.ravel()
        v[:, 0] = self.initial_velocity.ravel()
        a[:, 0] = np.linalg.solve(M, R0 - C @ v[:, 0] - K @ u[:, 0])
        tn[0] = t
        dtn[0] = dt

        # Time stepping loop
        i = 0
        while t < t_end and i + 1 < n_steps:
            # Effective stiffness
            Km = (1 - alpha_m) / (B * dt ** 2)
            Kc = G * (1 - alpha_f) / (B * dt)
            Kk = (1 - alpha_f)
            Keff = M * Km + C * Kc + K * Kk

            # Effective load vector
            rk = alpha_f * u[:, i]
            rcu = G * (1 - alpha_f) / (B * dt)
            rcv = (G - G * alpha_f - B) / B
            rca = (G - 2 * B) * (1 - alpha_f) / (2 * B) * dt
            rc = rcu * u[:, i] + rcv * v[:, i] + rca * a[:, i]

            rmu = (1 - alpha_m) / (B * dt ** 2)
            rmv = (1 - alpha_m) / (B * dt)
            rma = (1 - alpha_m - 2 * B) / (2 * B)
            rm = rmu * u[:, i] + rmv * v[:, i] + rma * a[:, i]

            # Pick load vector for this step
            R_t = R0   # use column i of your load matrix
            
            r_eff[:, i+1] = R_t - K @ rk + C @ rc + M @ rm

            # Update motion
            u[:, i+1] = np.linalg.solve(Keff, r_eff[:, i+1])
            v[:, i+1] = (G / (B * dt)) * (u[:, i+1] - u[:, i]) \
                        - (G - B) / B * v[:, i] \
                        - (G - 2 * B) / (2 * B) * dt * a[:, i]
            a[:, i+1] = (1 / (B * dt ** 2)) * (u[:, i+1] - u[:, i]) \
                        - (1 / (B * dt)) * v[:, i] \
                        - (1 - 2 * B) / (2 * B) * a[:, i]

            # Error calculations
            e[:, i] = (6 * B - 1) / 6 * (a[:, i+1] - a[:, i]) * dt ** 2
            if np.linalg.norm(u[:, i+1] - u[:, i]) != 0:
                et[i] = np.linalg.norm(e[:, i]) / np.linalg.norm(u[:, i+1] - u[:, i])
            cet[i+1] = cet[i] + np.linalg.norm(e[:, i])

            # Adaptive dt
            if v2 * ne > et[i] > v1 * ne:
                dt = dt * np.sqrt(ne / et[i])

            # Update time trackers
            t += dt
            i += 1
            tn[i] = t
            dtn[i] = dt

        # Final results
        self.u, self.v, self.a = u[:, :i+1], v[:, :i+1], a[:, :i+1]
        self.time = tn[:i+1]
        self.dt_hist = dtn[:i+1]
        self.errors = et[:i+1]
        print("Displacement history:")
        print(self.u)
        return

    def plot_results(self, dof_index=0):
        """
        Plot displacement, velocity, and acceleration for the given DOF index.
        """
        # Map solver outputs to histories for a single DOF
        time_history = self.time
        displacement_history = self.u[dof_index, :]
        velocity_history = self.v[dof_index, :]
        acceleration_history = self.a[dof_index, :]

        plt.figure(figsize=(12, 8))

        # Displacement
        plt.subplot(3, 1, 1)
        plt.plot(time_history, displacement_history, label='Displacement')
        plt.title('Displacement History')
        plt.xlabel('Time [s]')
        plt.ylabel('Displacement [m]')
        plt.grid()
        plt.legend()

        # Velocity
        plt.subplot(3, 1, 2)
        plt.plot(time_history, velocity_history, label='Velocity', color='orange')
        plt.title('Velocity History')
        plt.xlabel('Time [s]')
        plt.ylabel('Velocity [m/s]')
        plt.grid()
        plt.legend()

        # Acceleration
        plt.subplot(3, 1, 3)
        plt.plot(time_history, acceleration_history, label='Acceleration', color='green')
        plt.title('Acceleration History')
        plt.xlabel('Time [s]')
        plt.ylabel('Acceleration [m/s²]')
        plt.grid()
        plt.legend()

        plt.tight_layout()
        plt.show()
        
    def plot_results_all(self):
        """
        Plot displacement, velocity, and acceleration histories
        for all DOFs stored in self.u, self.v, self.a vs self.time.
        """
        time_history = self.time
        num_dofs = self.u.shape[0]

        plt.figure(figsize=(12, 8))

        # Displacement subplot
        plt.subplot(1, 1, 1)
        for dof in range(num_dofs):
            plt.plot(time_history, self.u[dof, :], label=f'DOF {dof+1}')
        plt.title('Displacement History')
        plt.xlabel('Time [s]')
        plt.ylabel('Displacement [m]')
        plt.grid()
        plt.legend(loc='upper right')
        
        # Y-DOFs (assuming ordering: x=0, y=1, z=2 per node)
        #y_dofs = range(1, num_dofs, 2)

        #plt.subplot(3, 1, 1)
        #for dof in y_dofs:
            #plt.plot(time_history, self.u[dof, :], label=f'DOF {dof+1} (y)')
        #plt.title('Y-Displacement History')
        #plt.xlabel('Time [s]')
        #plt.ylabel('Displacement Y [m]')
        #plt.grid()
        #plt.legend(loc='upper right')

        # Velocity subplot
        #plt.subplot(3, 1, 2)
        #for dof in range(num_dofs):
            #plt.plot(time_history, self.v[dof, :], label=f'DOF {dof+1}')
        #plt.title('Velocity History')
        #plt.xlabel('Time [s]')
        #plt.ylabel('Velocity [m/s]')
        #plt.grid()
        #plt.legend(loc='upper right')

        # Acceleration subplot
        #plt.subplot(3, 1, 3)
        #for dof in range(num_dofs):
            #plt.plot(time_history, self.a[dof, :], label=f'DOF {dof+1}')
        #plt.title('Acceleration History')
        #plt.xlabel('Time [s]')
        #plt.ylabel('Acceleration [m/s²]')
        #plt.grid()
        #plt.legend(loc='upper right')

        #plt.tight_layout()
        plt.show()