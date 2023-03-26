from multi_agent_path_planning.lifelong_MAPF.datastuctures import Map, Task


class BaseTaskFactory:
    """
    Def
    """

    # encorporate the map?
    # total number of agents
    # timestep = 0

    def produce_tasks(self, timestep: int = None):
        """
        Args:
            timestep: The current simulation timestep
        Returns:
            tasks: A list of Tasks
            complete: Is the factory done producing tasks
        """
        # only place tasks in free space

        return [], True


class RandomTaskFactory:
    def __init__(
        self, world_map: Map, tasks_per_timestep=1, max_timestep: int = None
    ) -> None:
        """Initalize a random task generator

        Args:
            world_map (Map): The map of the world
            tasks_per_timestep (int, optional): How many tasks to produce per timestep. Defaults to 1.
            max_timestep (_type_, optional): The timestep to stop producing tasks at. Defaults to None.
        """
        self.world_map = world_map
        self.tasks_per_timestep = tasks_per_timestep
        self.max_timestep = max_timestep

    def produce_tasks(self, timestep: int = None):
        """
        Args:
            timestep: The current simulation timestep
        Returns:
            tasks: A list of Tasks
            complete: Is the factory done producing tasks
        """
        if self.max_timestep is not None and self.max_timestep < timestep:
            return [], True

        task_list = []
        for _ in range(self.tasks_per_timestep):
            start, goal = self.world_map.get_random_unoccupied_loc(2)
            print("New Task Start: ",start,"New Task Goal: ",goal)
            new_task = Task(start=start, goal=goal, timestep=timestep)
            task_list.append(new_task)

        return task_list, False
