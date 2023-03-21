import yaml
import typing


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
    def __init__(
        self,
        loc,
        ID,
        goal=None,
        task: Task = None,
    ):
        """_summary_

        Args:
            loc (_type_): _description_
            ID (_type_): _description_
            goal (_type_, optional): _description_. Defaults to None.
            task (Task, optional): _description_. Defaults to None.
        """
        self.loc = loc
        self.ID = ID
        self.goal = goal
        self.task = task
        self.planned_path = None
        self.executed_path = Path()
        self.n_completed_task = 0
        self.idle_timesteps = 0

    # updater_routine:
    # update location
    # update full trajceory
    # if loc == goal
    # if task[1] == loc
    #   make goal and task null
    # method to take desired path and update the location
    def get_executed_path(self):
        return self.executed_path


class AgentSet:
    def __init__(self, agents: typing.List[Agent]):
        self.agents = agents

    def get_executed_paths(self):
        executed_paths = []
        for agent in self.agents:
            executed_paths.append(agent.get_executed_path())
        return executed_paths


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
