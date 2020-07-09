"""
Collision avoidance using Nonlinear Model-Predictive Control

author: Ashwin Bose (atb033@github.com)
"""

from utils.multi_robot_plot import plot_robot_and_obstacles
from utils.create_obstacles import create_obstacles
import numpy as np
import time

SIM_TIME = 5.
TIMESTEP = 0.1
NUMBER_OF_TIMESTEPS = int(SIM_TIME/TIMESTEP)
ROBOT_RADIUS = 0.5
VMAX = 2
VMIN = 0.2

# collision cost parameters
Q = 1.
kappa = 4.

# nmpc parameters
HORIZON_LENGTH = int(10)
NMPC_TIMESTEP = 0.2


def simulate(filename):
    obstacles = create_obstacles(SIM_TIME, NUMBER_OF_TIMESTEPS)

    start = np.array([5, 5])
    goal = np.array([5, 5])

    robot_state = start
    robot_state_history = np.empty((4, NUMBER_OF_TIMESTEPS))

    for i in range(NUMBER_OF_TIMESTEPS):
      # predict the obstacles' position in future
      obstacle_predictions = predict_obstacle_positions(obstacles[:, i, :])
      # compute velocity using nmpc
      u = np.ones(HORIZON_LENGTH * 2)
      x_robot = update_state(robot_state, u, NMPC_TIMESTEP)
      c1 = tracking_cost(x_robot, goal)
      c2 = total_collision_cost(x_robot, obstacle_predictions)
      print("collision cost is : ", c2)
      time.sleep(0.2)


def compute_velocity(robot, obstacles, p_desired):
    """
    Computes control velocity of the copter
    """
    pass


def tracking_cost(x, xref):
    numstack = int(len(x) / 2)
    Xref = np.vstack([xref.reshape(2,1)] * numstack)
    np.shape(Xref)
    return np.linalg.norm(x-Xref)


def total_collision_cost(robot, obstacles):
    total_cost = 0
    for i in range(HORIZON_LENGTH):
        for obstacle in obstacles:
            rob = robot[2 * i: 2 * i + 2]
            obs = obstacle[2 * i: 2 * i + 2]
            total_cost += collision_cost(rob, obs)
    return total_cost


def collision_cost(x0, x1):
    """
    Cost of collision between two robot_state
    """
    d = np.linalg.norm(x0 - x1)
    cost = Q / (1 + np.exp(kappa * (d - ROBOT_RADIUS)))
    return cost


def predict_obstacle_positions(obstacles):
    obstacle_predictions = []
    for i in range(np.shape(obstacles)[1]):
        obstacle = obstacles[:, i]
        obstacle_position = obstacle[:2]
        obstacle_vel = obstacle[2:]
        u = np.vstack([np.eye(2)] * HORIZON_LENGTH) @ obstacle_vel
        obstacle_prediction = update_state(obstacle_position, u, NMPC_TIMESTEP)
        obstacle_predictions.append(obstacle_prediction)
    return obstacle_predictions


def update_state(x0, u, timestep):
    """
    Computes the states of the system after applying a sequence of control signals u on
    initial state x0
    """
    N = len(u)
    lower_triangular_ones_matrix = np.tril(np.ones((N, N)))
    new_state = np.vstack([np.eye(2)] * int(N / 2)) @ x0 + \
        lower_triangular_ones_matrix @ u * timestep

    return new_state

