import typing
import numpy as np

from multi_agent_path_planning.lifelong_MAPF.datastuctures import (
    AgentSet,
    Task,
)


class BaseTaskAllocator:
    """
    Def
    """

    def allocate_tasks(self, tasks: typing.List[Task], agents: AgentSet) -> AgentSet:
        """
        Arguments:
            tasks: The open tasks
            agents:

        Returns:
            Agents updated with assignments
        """
        return agents


class RandomTaskAllocator:
    def allocate_tasks(self, tasks: typing.List[Task], agents: AgentSet) -> AgentSet:
        """Randomly match task with available robots

        Args:
            tasks (typing.List[Task]): The list of tasks which are open
            agents (AgentSet): The agents which may or may not be free to recive the task

        Returns:
            AgentSet: The agents are updated with their new task
        """
        # Parse which agents are not tasked yet
        untasked_agents = AgentSet(
            [agent for agent in agents.agents if not agent.is_allocated()]
        )

        # Sample the tasks to be assigned this timestep
        sampled_tasks = np.random.choice(
            tasks, size=min(len(untasked_agents), len(tasks)), replace=False
        ).tolist()

        # Sample the agents to associate with
        sampled_agents = np.random.choice(
            untasked_agents.tolist(), len(sampled_tasks), replace=False
        ).tolist()

        # Assign each agent a task
        for agent, task in zip(sampled_agents, sampled_tasks):
            agent.set_task(task)

        # Return the agents which were updated by reference
        return agents
