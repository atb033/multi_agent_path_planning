import typing
import numpy as np

from multi_agent_path_planning.lifelong_MAPF.datastuctures import AgentSet, TaskSet


class BaseTaskAllocator:
    """
    Def
    """

    def allocate_tasks(self, tasks: TaskSet, agents: AgentSet) -> AgentSet:
        """
        Arguments:
            tasks: The open tasks
            agents:

        Returns:
            Agents updated with assignments
        """
        return agents


class RandomTaskAllocator:
    def allocate_tasks(self, tasks: TaskSet, agents: AgentSet) -> AgentSet:
        """Randomly match task with available robots

        Args:
            tasks (typing.List[Task]): The list of tasks which are open
            agents (AgentSet): The agents which may or may not be free to recive the task

        Returns:
            AgentSet: The agents are updated with their new task
        """
        # Parse which agents are not tasked yet
        untasked_agents = agents.get_unallocated_agents()

        # Sample the tasks to be assigned this timestep
        sampled_tasks = tasks.pop_n_random_tasks(min(len(untasked_agents), len(tasks)))

        # Sample the agents to associate with
        sampled_agents = untasked_agents.get_n_random_agents(len(sampled_tasks))

        # Assign each agent a task
        for agent, task in zip(sampled_agents, sampled_tasks):
            # TODO: make this more elegent, we dont want to assign tasks where the agent is on top of the start, unless we rework some of the initilization stuff, it creates issues with the planner which assumes there is a path required
            if (
                agent.get_loc()[0] != task.start[0]
                and agent.get_loc()[1] != task.start[1]
            ):
                print("Agent :", agent.get_id(), " has been allocated a task!")
                agent.set_task(task)
            else:
                print("Agent sitting on goal, moving on...")

        # Return the agents which were updated by reference
        return agents
