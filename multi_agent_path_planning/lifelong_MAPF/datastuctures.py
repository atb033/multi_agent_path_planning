import yaml
import typing
import numpy as np
import matplotlib.pyplot as plt


class Task:
    def __init__(self, start, goal, timestep):
        self.start = start
        self.goal = goal
        self.timestep = timestep


class TaskSet:
    """An unordered set of tasks
    """

    def __init__(self, task_iterable: typing.Iterable = ()) -> None:
        """An unordered set of tasks

        Args:
            task_iterable (typing.Iterable, optional): The individual tasks. Defaults to ().
        """
        self.task_dict = {i: task_iterable[i] for i in range(len(task_iterable))}
        self.next_key = len(task_iterable) + 1

    def __len__(self) -> int:
        """The number of tasks

        Returns:
            int: the number of tasks
        """
        return len(self.task_dict)

    def add_tasks(self, task_iterable: typing.Iterable[Task]):
        """Add new tasks to the set

        Args:
            task_iterable (typing.Iterable[Task]): The tasks
        """
        new_task_dict = {
            i + self.next_key: task_iterable[i] for i in range(len(task_iterable))
        }
        self.next_key += len(task_iterable)
        self.task_dict.update(new_task_dict)

    def pop_n_random_tasks(self, n_tasks: int) -> typing.List[Task]:
        """Select, remove, and return n tasks

        Args:
            n_tasks (int): Number to remove

        Returns:
            typing.List[Task]: The tasks which were popped
        """
        keys = list(self.task_dict.keys())
        chosen_keys = np.random.choice(keys, size=n_tasks, replace=False)
        tasks = [self.task_dict.pop(k) for k in chosen_keys]
        return tasks


class PathNode:
    def __init__(self, loc, timestep):
        # print('New Path Node with Location:', loc," Time: ",timestep)
        self.loc = loc
        self.timestep = timestep
    def get_loc(self):
        return self.loc
    def get_time(self):
        return self.timestep

class Path:
    def __init__(self, initial_pathnodes=[]):
        self.pathnodes = initial_pathnodes

    def get_path(self):
        return self.pathnodes

    def add_pathnode(self, pathnode: PathNode):
        # print('path node added ', len(self.pathnodes))
        self.pathnodes.append(pathnode)

    def pop_pathnode(self):
        if len(self.pathnodes) > 0:
            # print('')
            # TODO: Debug time issue
            # print("Lenth of path before popping",len(self.pathnodes))
            temp = self.pathnodes.pop(0)
            # print("Lenth of path after popping",len(self.pathnodes))
            # print("Location of popped path node",temp.loc)
            # print("World time of popped path node",temp.timestep)
            # print('')
            return temp
        else:
            print("Popped from empty Path")
            exit()


class Agent:
    def __init__(
        self, loc, ID, goal=None, task: Task = None,
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
        self.timestep = 0

    def get_id(self):
        return self.ID

    def get_loc(self):
        return self.loc

    def get_goal(self):
        return self.goal

    def get_planned_path(self):
        return self.planned_path

    def set_task(self, task: Task):
        self.task = task
        self.goal = self.task.start

    def get_executed_path(self):
        return self.executed_path

    def is_allocated(self):
        return self.goal is not None

    def set_planned_path_from_plan(self, plan):
        temp_path = Path()
        for node in plan[self.ID]:
            temp_loc = [node["x"],node["y"]]
            temp_time = self.timestep + node["t"]
            temp_path.add_pathnode(PathNode(temp_loc,temp_time))

        self.planned_path = temp_path

    def soft_simulation_timestep_update(self):
        # if the agent has no plan is taskless
        if self.planned_path is None:
            print('Agent stationary')
            self.executed_path.add_pathnode(PathNode(self.loc, self.timestep))
            self.timestep += 1
            self.idle_timesteps += 1
        else:
            print('Agent on the move')
            # print(self.loc)
            self.loc = self.planned_path.pop_pathnode().get_loc()
            # print(self.loc)
            # print(self.timestep)
            self.executed_path.add_pathnode(PathNode(self.loc, self.timestep))
            self.timestep += 1
            # if path is exausted (goal reached)
            if len(self.planned_path.pathnodes) == 0:
                # if we have hit the "start" of a "task"
                if self.loc == self.task.start:
                    self.goal = self.task.goal 
                else:
                    self.goal = None
                    self.task = None
                    self.planned_path = None
                    self.n_completed_task += 1


class AgentSet:
    def __init__(self, agents: typing.List[Agent]):
        self.agents = agents

    def __len__(self):
        return len(self.agents)

    def get_executed_paths(self):
        schedule = {}

        for agent in self.agents:
            temp_id = agent.get_id()
            temp_list = []

            for path_node in agent.get_executed_path().get_path():
                temp = {}
                temp['x'] = path_node.get_loc()[0]
                temp['y'] = path_node.get_loc()[1]
                temp['t'] = path_node.get_time()
                temp_list.append(temp)
            schedule[temp_id] = temp_list

        output = {}
        output['schedule'] = schedule

        return output

    def tolist(self):
        return self.agents

    def get_unallocated_agents(self):
        return AgentSet([agent for agent in self.agents if not agent.is_allocated()])

    def get_n_random_agents(self, n_agents):
        sampled_agents = np.random.choice(self.agents, size=n_agents).tolist()
        return sampled_agents

    def get_agent_from_id(self, search_id):
        # search for agent by self.ID
        for index, agent in enumerate(self.agents):
            if agent.get_id() == search_id:
                return index
        print('agent ID does not exist in agent list')
        return False


class Map:
    def __init__(self, map, vis=False):
        with open(map, "r") as map_file:
            try:
                self.map_dict = yaml.load(map_file, Loader=yaml.FullLoader)["map"]
            except yaml.YAMLError as exc:
                print(exc)
        self.map_np = np.ones(self.map_dict["dimensions"]).astype(bool)
        for obstacle in self.map_dict["obstacles"]:
            self.map_np[obstacle[0], obstacle[1]] = False
        self.unoccupied_inds = np.stack(np.where(self.map_np), axis=0).T
        if vis:
            plt.imshow(self.map_np)
            plt.show()

    def get_map_dict(self):
        return self.map_dict

    def check_ocupied(self, loc):
        return self.map_np[loc[0], loc[1]]

    def get_random_unoccupied_loc(self, n_samples, with_replacement=False):
        selected_inds = np.random.choice(
            self.unoccupied_inds.shape[0], n_samples, replace=with_replacement
        )
        selected_locs = self.unoccupied_inds[selected_inds]
        return selected_locs

