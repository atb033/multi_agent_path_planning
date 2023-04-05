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

    def fixup_goals(self, map_instance: Map, agent_list: typing.List[Agent]):
        """Some goals may be unset, others may be duplicates

        Args:
            map_instance (Map): _description_
            agent_list (typing.List[Agent]): _description_

        Returns:
            _type_: _description_
        """
        # These are the initial goals which may be None
        initial_goals = [a["goal"] for a in agent_list]
        # Find duplicate goals
        unique_goals, inv, counts = np.unique(
            [(g if g is not None else (np.inf, np.inf)) for g in initial_goals],
            return_inverse=True,
            return_counts=True,
            axis=0,
        )
        # Iterate over unique goals
        for i in range(len(unique_goals)):
            # If there are duplicates
            if counts[i] > 1:
                # Find which inds match
                duplicate_inds = np.where(inv == i)[0]
                del_inds = np.random.choice(
                    duplicate_inds, size=counts[i] - 1, replace=False
                )
                for del_ind in del_inds:
                    initial_goals[del_ind] = None
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
        # Get the dimensions, agents, and obstacles in the expected format
        dimension = map_instance.get_dim()
        agent_list = agents.get_agent_dict()
        obstacles = map_instance.get_obstacles()

        # Make sure there are no errors in the agent list
        agent_list = self.fixup_goals(map_instance=map_instance, agent_list=agent_list)
        # Create an environment and solver
        env = Environment(dimension, agent_list, obstacles)
        cbs = CBS(env)
        # Solve the CBS instance
        solution = cbs.search()

        # Set the paths for each agent
        for agent_id in solution.keys():
            agents.agents[
                agents.get_agent_from_id(agent_id)
            ].set_planned_path_from_plan(solution)

        return agents
