import typing
import logging

from multi_agent_path_planning.lifelong_MAPF.datastuctures import AgentSet


class BaseDynamicsSimulator:
    """ """

    def step_world(
        self, agents: AgentSet, timestep: int,
    ):
        """
        Args:
            agents: the list of agents
            timestep: The current simulation timestep

        Returns:
            agents: the agents updated
            agents_at_goals: Are all agents at the goals
        """

        logging.info("Agent Simulation Step")

        for agent_index in range(len(agents)):
            logging.info(f"Updating Agent: {agents.agents[agent_index].get_id()}")
            agents.agents[agent_index].soft_simulation_timestep_update()
        return agents, False
