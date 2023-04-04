#!/usr/bin/env python3
import yaml
import matplotlib

# matplotlib.use("Agg")
from matplotlib.patches import Circle, Rectangle, Arrow
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation
import matplotlib.animation as manimation
import argparse
import math

Colors = ["orange", "blue", "green"]


class Animation:
    def __init__(self, map, output):
        self.map = map
        self.output = output
        self.obstacle_output = map["dynamic_obstacles"]
        self.combined_output = {}
        self.combined_output.update(self.output["schedule"])
        self.combined_output.update(self.obstacle_output)

        aspect = map["map"]["dimensions"][0] / map["map"]["dimensions"][1]

        self.fig = plt.figure(frameon=False, figsize=(4 * aspect, 4))
        self.ax = self.fig.add_subplot(111, aspect="equal")
        self.fig.subplots_adjust(
            left=0, right=1, bottom=0, top=1, wspace=None, hspace=None
        )
        # self.ax.set_frame_on(False)

        self.patches = []
        self.artists = []
        self.agents = dict()
        self.agent_names = dict()
        self.active_starts = dict()
        self.active_goals = dict()
        self.open_starts = dict()
        self.open_goals = dict()
        self.open_alpha = 0.2
        # create boundary patch
        xmin = -0.5
        ymin = -0.5
        xmax = map["map"]["dimensions"][0] - 0.5
        ymax = map["map"]["dimensions"][1] - 0.5

        # self.ax.relim()
        plt.xlim(xmin, xmax)
        plt.ylim(ymin, ymax)
        # self.ax.set_xticks([])
        # self.ax.set_yticks([])
        # plt.axis('off')
        # self.ax.axis('tight')
        # self.ax.axis('off')

        self.patches.append(
            Rectangle(
                (xmin, ymin),
                xmax - xmin,
                ymax - ymin,
                facecolor="none",
                edgecolor="red",
            )
        )
        for o in map["map"]["obstacles"]:
            x, y = o[0], o[1]
            self.patches.append(
                Rectangle((x - 0.5, y - 0.5), 1, 1, facecolor="red", edgecolor="red")
            )

        # create agents:
        self.T = 0
        # draw goals first
        # for d, i in zip(map["agents"], range(0, len(map["agents"]))):
        #     self.patches.append(
        #         Rectangle(
        #             (d["goal"][0] - 0.25, d["goal"][1] - 0.25),
        #             0.5,
        #             0.5,
        #             facecolor=Colors[0],
        #             edgecolor="black",
        #             alpha=0.5,
        #         )
        #     )
        # Active tasks
        for d, i in zip(output["active_tasks"], range(0, len(output["active_tasks"]))):
            id = d['task_id']
            if id not in self.active_starts.keys():
                self.active_starts[id] = Rectangle(
                        (d['start']["x"] - 0.25, d['start']["y"] - 0.25),
                        0.5,
                        0.5,
                        facecolor="cyan",
                        edgecolor="black",
                        alpha=1.0,
                    )
                self.active_goals[id] = Rectangle(
                        (d['goal']["x"] - 0.25, d['goal']["y"] - 0.25),
                        0.5,
                        0.5,
                        facecolor="lime",
                        edgecolor="black",
                        alpha=1.0,
                    )
                start_id_text = self.ax.text(d["start"]['x'], d["start"]['y'], d['task_id'])
                goal_id_text = self.ax.text(d["goal"]['x'], d["goal"]['y'], d['task_id'])
                self.artists.append(start_id_text)
                self.artists.append(goal_id_text)
                self.patches.append(self.active_starts[id])
                self.patches.append(self.active_goals[id])
        # Open tasks
        for d, i in zip(output["open_tasks"], range(0, len(output["open_tasks"]))):
            id = d['task_id']
            if id not in self.open_starts.keys():
                self.open_starts[id] = Rectangle(
                        (d['start']["x"] - 0.25, d['start']["y"] - 0.25),
                        0.5,
                        0.5,
                        facecolor="cyan",
                        edgecolor="black",
                        alpha=self.open_alpha,
                    )
                self.open_goals[id] = Rectangle(
                        (d['goal']["x"] - 0.25, d['goal']["y"] - 0.25),
                        0.5,
                        0.5,
                        facecolor="lime",
                        edgecolor="black",
                        alpha=self.open_alpha,
                    )
                start_id_text = self.ax.text(d["start"]['x'], d["start"]['y'], d['task_id'], alpha=self.open_alpha)
                goal_id_text = self.ax.text(d["goal"]['x'], d["goal"]['y'], d['task_id'], alpha=self.open_alpha)
                self.artists.append(start_id_text)
                self.artists.append(goal_id_text)
                self.patches.append(self.open_starts[id])
                self.patches.append(self.open_goals[id])
        # Agents
        for d, i in zip(map["agents"], range(0, len(map["agents"]))):
            name = d["name"]
            self.agents[name] = Circle(
                (d["start"][0], d["start"][1]),
                0.3,
                facecolor=Colors[0],
                edgecolor="black",
            )
            self.agents[name].original_face_color = Colors[0]
            self.patches.append(self.agents[name])
            self.T = max(self.T, output["schedule"][name][-1]["t"])
            self.agent_names[name] = self.ax.text(
                d["start"][0], d["start"][1], name.replace("agent", "")
            )
            self.agent_names[name].set_horizontalalignment("center")
            self.agent_names[name].set_verticalalignment("center")
            self.artists.append(self.agent_names[name])

        for name in self.obstacle_output:
            self.agents[name] = Circle(
                (d["start"][0], d["start"][1]),
                0.3,
                facecolor=Colors[2],
                edgecolor="black",
            )
            self.agents[name].original_face_color = Colors[2]
            self.patches.append(self.agents[name])
            self.T = max(self.T, map["dynamic_obstacles"][name][-1]["t"])
            self.agent_names[name] = self.ax.text(
                d["start"][0], d["start"][1], name.replace("dynamic_obs", "obs")
            )
            self.agent_names[name].set_horizontalalignment("center")
            self.agent_names[name].set_verticalalignment("center")
            self.artists.append(self.agent_names[name])

        # self.ax.set_axis_off()
        # self.fig.axes[0].set_visible(False)
        # self.fig.axes.get_yaxis().set_visible(False)

        # self.fig.tight_layout()

        self.anim = animation.FuncAnimation(
            self.fig,
            self.animate_func,
            init_func=self.init_func,
            frames=int(self.T + 1) * 10,
            interval=100,
            blit=True,
        )

    def save(self, file_name, speed):
        self.anim.save(file_name, "ffmpeg", fps=10 * speed, dpi=200),
        # savefig_kwargs={"pad_inches": 0, "bbox_inches": "tight"})

    def show(self):
        plt.show()

    def init_func(self):
        for p in self.patches:
            self.ax.add_patch(p)
        for a in self.artists:
            self.ax.add_artist(a)
        return self.patches + self.artists

    def animate_func(self, i):
        t = int(np.floor(i/10))

        # Active tasks
        for id in self.active_starts.keys():
            for active_task in self.output['active_tasks']:
                if active_task['task_id'] == id:
                    if t == active_task['t']:
                        p_start = (active_task['start']['x'], active_task['start']['y'])
                        self.active_starts[id].center = p_start
                        self.active_starts[id].set_alpha(1.0)
                        p_goal = (active_task['goal']['x'], active_task['goal']['y'])
                        self.active_goals[id].center = p_goal
                        self.active_goals[id].set_alpha(1.0)
                        self.artists[int(id * 2)].set_alpha(1.0)
                        self.artists[int(id * 2)+1].set_alpha(1.0)
                        break
                    else:
                        self.active_starts[id].set_alpha(0.0)
                        self.active_goals[id].set_alpha(0.0)
                        self.artists[int(id * 2)].set_alpha(0.0)
                        self.artists[int(id * 2)+1].set_alpha(0.0)
        # Open tasks
        for id in self.open_starts.keys():
            for open_task in self.output['open_tasks']:
                if open_task['task_id'] == id:
                    active_offset = 0#int(len(self.active_starts)*2)
                    if t == open_task['t']:
                        p_start = (open_task['start']['x'], open_task['start']['y'])
                        self.open_starts[id].center = p_start
                        self.open_starts[id].set_alpha(self.open_alpha)
                        p_goal = (open_task['goal']['x'], open_task['goal']['y'])
                        self.open_goals[id].center = p_goal
                        self.open_goals[id].set_alpha(self.open_alpha)
                        self.artists[active_offset + int(id * 2)].set_alpha(self.open_alpha)
                        self.artists[active_offset + int(id * 2)+1].set_alpha(self.open_alpha)
                        break
                    else:
                        self.open_starts[id].set_alpha(0.0)
                        self.open_goals[id].set_alpha(0.0)
                        self.artists[active_offset + int(id * 2)].set_alpha(0.0)
                        self.artists[active_offset + int(id * 2)+1].set_alpha(0.0)

        for agent_name, agent in self.combined_output.items():
            pos = self.getState(i / 10, agent)
            p = (pos[0], pos[1])
            self.agents[agent_name].center = p
            self.agent_names[agent_name].set_position(p)

        # reset all colors
        for _, agent in self.agents.items():
            agent.set_facecolor(agent.original_face_color)

        # check drive-drive collisions
        agents_array = [agent for _, agent in self.agents.items()]
        for i in range(0, len(agents_array)):
            for j in range(i + 1, len(agents_array)):
                d1 = agents_array[i]
                d2 = agents_array[j]
                pos1 = np.array(d1.center)
                pos2 = np.array(d2.center)
                if np.linalg.norm(pos1 - pos2) < 0.7:
                    d1.set_facecolor("red")
                    d2.set_facecolor("red")
                    print("COLLISION! (agent-agent) ({}, {})".format(i, j))

        return self.patches + self.artists

    def getState(self, t, d):
        idx = 0
        while idx < len(d) and d[idx]["t"] < t:
            idx += 1
        if idx == 0:
            return np.array([float(d[0]["x"]), float(d[0]["y"])])
        elif idx < len(d):
            posLast = np.array([float(d[idx - 1]["x"]), float(d[idx - 1]["y"])])
            posNext = np.array([float(d[idx]["x"]), float(d[idx]["y"])])
        else:
            return np.array([float(d[-1]["x"]), float(d[-1]["y"])])
        dt = d[idx]["t"] - d[idx - 1]["t"]
        t = (t - d[idx - 1]["t"]) / dt
        pos = (posNext - posLast) * t + posLast
        return pos


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("map", help="input file containing map")
    parser.add_argument("output", help="output for agents")
    parser.add_argument(
        "--video",
        dest="video",
        default=None,
        help="output video file (or leave empty to show on screen)",
    )
    parser.add_argument("--speed", type=int, default=1, help="speedup-factor")
    args = parser.parse_args()

    with open(args.map) as map_file:
        map = yaml.load(map_file, Loader=yaml.FullLoader)

    with open(args.output) as states_file:
        output = yaml.load(states_file, Loader=yaml.FullLoader)

    animation = Animation(map, output)

    if args.video:
        animation.save(args.video, args.speed)
    else:
        animation.show()
