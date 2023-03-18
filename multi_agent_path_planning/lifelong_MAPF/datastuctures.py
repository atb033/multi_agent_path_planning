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


class Map:
    def __init__(self, map):
        self.map = map


class Assignment:
    def __init__(self, task: Task, agent: Agent) -> None:
        self.task = task
        self.agent = agent
