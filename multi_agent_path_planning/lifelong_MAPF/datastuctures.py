import yaml


class Task:
    def __init__(self, start, goal, timestep):
        self.start = start
        self.goal = goal
        self.timestep = timestep


class PathNode:
    def __init__(self, loc, timestep):
        self.loc = loc
        self.timestep = timestep


class Path:
    def __init__(self, initial_pathnodes=[]):
        self.pathnodes = initial_pathnodes

    def add_pathnode(self, pathnode: PathNode):
        self.pathnodes.append(pathnode)


class Agent:
    def __init__(self, loc, ID):
        self.loc = loc
        self.ID = ID
        # goal
        # task
        # desired path
        # full exectued path
        # number of tasks compleaed?
        # timesteps unallocated

    # updater_routine:
    # update location
    # update full trajceory
    # if loc == goal
    # if task[1] == loc
    #   make goal and task null
    # method to take desired path and update the location


class Map:
    def __init__(self, map):
        with open(map, "r") as map_file:
            try:
                self.map_dict = yaml.load(map_file, Loader=yaml.FullLoader)["map"]
            except yaml.YAMLError as exc:
                print(exc)


class Assignment:
    def __init__(self, task: Task, agent: Agent) -> None:
        self.task = task
        self.agent = agent
