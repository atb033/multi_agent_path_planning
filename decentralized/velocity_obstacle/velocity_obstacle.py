"""
Collision avoidance using Velocity-obstacle method

author: Ashwin Bose (atb033@github.com)
"""

from multi_robot_plot import plot_robot_and_obstacles
import numpy as np
import cvxpy as cp
import matplotlib.pyplot as plt
import argparse

SIM_TIME = 5.
TIMESTEP = 0.025
NUMBER_OF_TIMESTEPS = int(SIM_TIME/TIMESTEP)
ROBOT_RADIUS = 0.5
VMAX = 2
VMIN = 0.2


def simulate(filename):
    obstacles = create_obstacles()

    start = np.array([5, 0, 0, 0])
    goal = np.array([5, 10, 0, 0])

    robot_state = start
    robot_state_history = np.empty((16, NUMBER_OF_TIMESTEPS))
    v_dis = []
    for i in range(NUMBER_OF_TIMESTEPS):
        v_desired = compute_desired_velocity(robot_state, goal)
        control_vel, v_display = compute_velocity(
            robot_state, obstacles[:, i, :], v_desired)
        robot_state = update_state(robot_state, control_vel)
        robot_state_history[:4, i] = robot_state
        v_dis.append(v_display)

    plot_robot_and_obstacles(
        robot_state_history, obstacles, ROBOT_RADIUS, NUMBER_OF_TIMESTEPS,
        v_dis, filename)


def compute_velocity(robot, obstacles, v_desired):
    pA = robot[:2]
    vA = robot[-2:]
    # Compute the constraints
    # for each velocity obstacles
    number_of_obstacles = np.shape(obstacles)[1]
    Amat = np.empty((number_of_obstacles * 2, 2))
    bvec = np.empty((number_of_obstacles * 2))
    for i in range(number_of_obstacles):
        obstacle = obstacles[:, i]
        pB = obstacle[:2]
        vB = obstacle[2:]
        dispBA = pA - pB
        distBA = np.linalg.norm(dispBA)
        thetaBA = np.arctan2(dispBA[1], dispBA[0])
        if 2.2 * ROBOT_RADIUS > distBA:
            distBA = 2.2*ROBOT_RADIUS
        phi_obst = np.arcsin(2.2*ROBOT_RADIUS/distBA)
        phi_left = thetaBA + phi_obst
        phi_right = thetaBA - phi_obst

        # VO
        translation = vB
        Atemp, btemp = create_constraints(translation, phi_left, "left")
        Amat[i*2, :] = Atemp
        bvec[i*2] = btemp
        Atemp, btemp = create_constraints(translation, phi_right, "right")
        Amat[i*2 + 1, :] = Atemp
        bvec[i*2 + 1] = btemp

    # Create search-space
    th = np.linspace(0, 2*np.pi, 20)
    vel = np.linspace(0, VMAX, 5)

    vv, thth = np.meshgrid(vel, th)

    vx_sample = (vv * np.cos(thth)).flatten()
    vy_sample = (vv * np.sin(thth)).flatten()

    v_sample = np.stack((vx_sample, vy_sample))

    v_satisfying_constraints = check_constraints(v_sample, Amat, bvec)

    # Objective function
    size = np.shape(v_satisfying_constraints)[1]
    diffs = v_satisfying_constraints - \
        ((v_desired).reshape(2, 1) @ np.ones(size).reshape(1, size))
    norm = np.linalg.norm(diffs, axis=0)
    min_index = np.where(norm == np.amin(norm))[0][0]
    cmd_vel = (v_satisfying_constraints[:, min_index])

    # plt.cla()
    # plt.scatter(v_satisfying_constraints[0, :], v_satisfying_constraints[1, :])
    # plt.pause(0.1)

    v_display = v_satisfying_constraints + pA.reshape(2, 1) @ np.ones(np.shape(
        v_satisfying_constraints)[1]).reshape(1, np.shape(v_satisfying_constraints)[1])

    return cmd_vel, v_display


def check_constraints(v_sample, Amat, bvec):
    length = np.shape(bvec)[0]

    for i in range(int(length/2)):
        v_sample = check_inside(v_sample, Amat[2*i:2*i+2, :], bvec[2*i:2*i+2])

    return v_sample


def check_inside(v, Amat, bvec):
    v_out = []
    for i in range(np.shape(v)[1]):
        if not ((Amat @ v[:, i] < bvec).all()):
            v_out.append(v[:, i])
    return np.array(v_out).T


def create_constraints(translation, angle, side):
    # create line
    origin = np.array([0, 0, 1])
    point = np.array([np.cos(angle), np.sin(angle)])
    line = np.cross(origin, point)
    line = translate_line(line, translation)

    if side == "left":
        line *= -1

    A = line[:2]
    b = -line[2]

    return A, b


def translate_line(line, translation):
    matrix = np.eye(3)
    matrix[2, :2] = -translation[:2]
    return matrix @ line


def create_obstacles():
    # Obstacle 1
    v = -2
    p0 = np.array([5, 12])
    obst = create_robot(p0, v, np.pi/2).reshape(4, NUMBER_OF_TIMESTEPS, 1)
    obstacles = obst
    # Obstacle 2
    v = 2
    p0 = np.array([0, 5])
    obst = create_robot(p0, v, 0).reshape(4, NUMBER_OF_TIMESTEPS, 1)
    obstacles = np.dstack((obstacles, obst))
    # Obstacle 3
    v = 2
    p0 = np.array([10, 10])
    obst = create_robot(p0, v, -np.pi * 3 / 4).reshape(4,
                                                       NUMBER_OF_TIMESTEPS, 1)
    obstacles = np.dstack((obstacles, obst))
    # Obstacle 4
    v = 2
    p0 = np.array([7.5, 2.5])
    obst = create_robot(p0, v, np.pi * 3 / 4).reshape(4,
                                                      NUMBER_OF_TIMESTEPS, 1)
    obstacles = np.dstack((obstacles, obst))

    return obstacles


def create_robot(p0, v, theta):
    # Creates obstacles starting at p0 and moving at v in theta direction
    t = np.linspace(0, SIM_TIME, NUMBER_OF_TIMESTEPS)
    theta = theta * np.ones(np.shape(t))
    vx = v * np.cos(theta)
    vy = v * np.sin(theta)
    v = np.stack([vx, vy])
    p0 = p0.reshape((2, 1))
    p = p0 + np.cumsum(v, axis=1) * TIMESTEP
    p = np.concatenate((p, v))
    return p


def update_state(x, v):
    new_state = np.empty((4))
    new_state[:2] = x[:2] + v * TIMESTEP
    new_state[-2:] = v
    return new_state


def compute_desired_velocity(current_pos, goal_pos):
    disp_vec = (goal_pos - current_pos)[:2]
    norm = np.linalg.norm(disp_vec)
    if norm < ROBOT_RADIUS / 5:
        return np.zeros(2)
    disp_vec = disp_vec / norm
    np.shape(disp_vec)
    desired_vel = VMAX * disp_vec
    return desired_vel


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", "--filename", help="filename, in case you want to save the animation")
    args = parser.parse_args()
    simulate(args.filename)
