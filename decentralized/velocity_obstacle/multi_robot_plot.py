"""
Plotting tool for 2D multi-robot system

author: Ashwin Bose (atb033@github.com)
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle
import numpy as np

T = 5
STEP = 0.05
NUMBER_OF_TIMESTEPS = T/STEP


def plot_robot_and_obstacles(robot, obstacles, robot_radius, num_steps, vdis, filename):
    for i in range(int(num_steps)):
        plt.cla()
        plt.gcf().canvas.mpl_connect(
            'key_release_event',
            lambda event: [exit(0) if event.key == 'escape' else None])

        # Plot robot
        plot_robot(robot, i, robot_radius)

        # Plot obstacles
        for j in range(np.shape(obstacles)[2]):
            plot_robot(obstacles[:, :, j], i, robot_radius, is_obstacle=True)

        # Plot possible velocities
        # plt.scatter(vdis[i][0, :], vdis[i][1, :])

        plt.grid(True)
        plt.ylim(0., 10.)
        plt.xlim(0., 10.)
        plt.pause(STEP)

    plt.cla()
    plt.close()

    # Save animation gif
    if not filename:
        return
    fig = plt.figure()
    ax = fig.add_subplot(111, autoscale_on=False, xlim=(0, 10), ylim=(0, 10))
    ax.set_aspect('equal')
    ax.grid()
    line, = ax.plot([], [], '--r')

    robot_patch = Circle((robot[0, 0], robot[1, 0]),
                         robot_radius, facecolor='green', edgecolor='black')
    obstacle_list = []
    for obstacle in range(np.shape(obstacles)[2]):
        obstacle = Circle((0, 0), robot_radius,
                          facecolor='blue', edgecolor='black')
        obstacle_list.append(obstacle)

    def init():
        ax.add_patch(robot_patch)
        for obstacle in obstacle_list:
            ax.add_patch(obstacle)
        line.set_data([], [])
        return [robot_patch] + [line] + obstacle_list

    def animate(i):
        robot_patch.center = (robot[0, i], robot[1, i])
        for j in range(len(obstacle_list)):
            obstacle_list[j].center = (obstacles[0, i, j], obstacles[1, i, j])
        line.set_data(robot[0, :i], robot[1, :i])
        return [robot_patch] + [line] + obstacle_list

    ani = animation.FuncAnimation(
        fig, animate, np.arange(1, num_steps), interval=200,
        blit=True, init_func=init)

    ani.save(filename, "ffmpeg", fps=30)


def plot_robot(robot, timestep, radius=1, is_obstacle=False):
    if robot is None:
        return
    center = robot[:2, timestep]
    x = center[0]
    y = center[1]
    if is_obstacle:
        circle = plt.Circle((x, y), radius, color='aqua', ec='black')
        plt.plot(robot[0, :timestep], robot[1, :timestep], '--r',)
    else:
        circle = plt.Circle((x, y), radius, color='green', ec='black')
        plt.plot(robot[0, :timestep], robot[1, :timestep], 'blue')

    plt.gcf().gca().add_artist(circle)
