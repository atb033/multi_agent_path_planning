import numpy as np

def compute_desired_velocity(current_pos, goal_pos, robot_radius, vmax):
    disp_vec = (goal_pos - current_pos)[:2]
    norm = np.linalg.norm(disp_vec)
    if norm < robot_radius / 5:
        return np.zeros(2)
    disp_vec = disp_vec / norm
    np.shape(disp_vec)
    desired_vel = vmax * disp_vec
    return desired_vel
