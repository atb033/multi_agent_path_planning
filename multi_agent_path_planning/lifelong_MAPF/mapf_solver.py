import typing

from multi_agent_path_planning.centralized.sipp.graph_generation import SippGraph, State
from multi_agent_path_planning.centralized.sipp.sipp import SippPlanner
from multi_agent_path_planning.lifelong_MAPF.datastuctures import (
    AgentSet,
    Map,
    Path,
    Agent,
)
from multi_agent_path_planning.lifelong_MAPF.helpers import make_map_dict_dynamic_obs
from multi_agent_path_planning.centralized.cbs.cbs import CBS, Environment
import numpy as np
import logging
from copy import copy


class BaseMAPFSolver:
    """
    Def
    """

    def solve_MAPF_instance(
        self, map_instance: Map, agents: AgentSet, timestep: int,
    ) -> typing.List[Path]:
        """
        Arguments:
            map: The map representation
            assignments: The assignments that must be completed
            planned_paths: The already planned paths
            timestep: The simulation timestep
        """
        return agents


class SippSolver:
    """
    Def
    """

    def solve_MAPF_instance(
        self, map_instance: Map, agents: AgentSet, timestep: int,
    ) -> typing.List[Path]:
        """
        Arguments:
            map: The map representation
            assignments: The assignments that must be completed
            planned_paths: The already planned paths
            timestep: The simulation timestep
        """
        temp_map = make_map_dict_dynamic_obs(
            map_instance=map_instance, agents=agents, timestep=timestep
        )

        if "agents" not in temp_map:
            logging.info(f"No Agent Replans at Timestep :{timestep}")
            return agents

        if len(temp_map["agents"]) == 0:
            logging.info(f"No Agent Replans at Timestep :{timestep}")
            return agents

        for agent in range(len(temp_map["agents"])):
            id_agent = temp_map["agents"][agent]["name"]
            logging.info(f"setting plan for the following agent {id_agent}")
            sipp_planner = SippPlanner(temp_map, agent)

            if sipp_planner.compute_plan():
                plan = sipp_planner.get_plan()
                logging.info(f"Plan for agent: {id_agent}, {plan}")
                temp_map["dynamic_obstacles"].update(plan)
                # update agent
                agents.agents[
                    agents.get_agent_from_id(id_agent)
                ].set_planned_path_from_plan(plan)
            else:
                logging.warn(
                    f"Plan not found for agent : {id_agent} at timestep: {timestep}"
                )

        return agents


class CBSSolver:
    """
    Def
    """

    def set_unset_goals(self, map_instance: Map, agent_list: typing.List[Agent]):
        # These are the initial goals which may be None
        initial_goals = [a["goal"] for a in agent_list]
        # This is going to be filled out
        final_goals = copy(initial_goals)
        # We randomize the allocation order to avoid bias
        permutation = np.random.permutation(len(initial_goals))
        # Run through the goals
        for i in permutation:
            initial_goal = initial_goals[i]
            # Is this not set
            if initial_goal is None:
                valid = False
                # Randomly sample of a goal in freespace
                while not valid:
                    random_loc = list(
                        map_instance.get_random_unoccupied_locs(n_samples=1)[0].as_xy()
                    )
                    if random_loc not in final_goals:
                        valid = True
                        final_goals[i] = random_loc
        for i, final_goal in enumerate(final_goals):
            agent_list[i]["goal"] = final_goal
        return agent_list

    def solve_MAPF_instance(
        self, map_instance: Map, agents: AgentSet, timestep: int,
    ) -> typing.List[Path]:
        """
        Arguments:
            map: The map representation
            assignments: The assignments that must be completed
            planned_paths: The already planned paths
            timestep: The simulation timestep
        """
        dimension = map_instance.get_dim()
        agent_list = agents.get_agent_dict()
        agent_list = self.set_unset_goals(
            map_instance=map_instance, agent_list=agent_list
        )
        obstacles = map_instance.get_obstacles()
        env = Environment(dimension, agent_list, obstacles)
        logging.info(f"agent_list: {agent_list}")

        cbs = CBS(env)
        solution = cbs.search()
        for agent_id, plan in solution.items():
            agents.agents[
                agents.get_agent_from_id(agent_id)
            ].set_planned_path_from_plan(solution)

        return agents
