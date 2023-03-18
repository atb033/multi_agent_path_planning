class BaseDynamicsSimulator:
    """ """

    def step_world(
        self,
        planned_paths,
        completed_paths,
        allocated_agents,
        unallocated_agents,
        timestep: int,
    ):
        """
        Args:
            planned_paths: The current lists of planned paths
            completed_paths: The completed paths from the prior timestep, which will be updated
            allocated_agents: the allocated agents, which will be updated
            unallocated_agents: The unallocated agents, which will be updated
            timestep: The current simulation timestep

        Returns:
            completed_paths: The updated completed paths
            allocated_agents: Updated based on reaching goals
            unallocated_agents: Updated based on reaching goals
            agents_at_goals: Are all agents at the goals
        """
        return completed_paths, allocated_agents, unallocated_agents, True
