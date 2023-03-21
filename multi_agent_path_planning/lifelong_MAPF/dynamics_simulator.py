import typing
from multi_agent_path_planning.lifelong_MAPF.datastuctures import AgentSet


class BaseDynamicsSimulator:
    """ """

    def step_world(
        self,
        agents: AgentSet,
        timestep: int,
    ):
        """
        Args:
            agents: the list of agents
            timestep: The current simulation timestep

        Returns:
            agents: the agents updated
            agents_at_goals: Are all agents at the goals
        """
        return agents, False
