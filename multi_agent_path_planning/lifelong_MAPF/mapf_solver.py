import typing

from multi_agent_path_planning.centralized.sipp.graph_generation import SippGraph, State
from multi_agent_path_planning.centralized.sipp.sipp import SippPlanner
from multi_agent_path_planning.lifelong_MAPF.datastuctures import AgentSet, Map, Path
from multi_agent_path_planning.lifelong_MAPF.helpers import make_map_dict_dynamic_obs


class BaseMAPFSolver:
    """
    Def
    """

    def solve_MAPF_instance(
        self,
        map_instance: Map,
        agents: AgentSet,
        timestep: int,
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
        self,
        map_instance: Map,
        agents: AgentSet,
        timestep: int,
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
            print("No Agent Replans at Timestep :", timestep)
            return agents

        if len(temp_map["agents"]) == 0:
            print("No Agent Replans at Timestep :", timestep)
            return agents

        for agent in range(len(temp_map["agents"])):
            id_agent = temp_map["agents"][agent]["name"]
            print("setting plan for the following agent", id_agent)
            sipp_planner = SippPlanner(temp_map, agent)

            if sipp_planner.compute_plan():
                plan = sipp_planner.get_plan()
                print("Plan for agent:", id_agent, plan)
                temp_map["dynamic_obstacles"].update(plan)
                # update agent
                agents.agents[
                    agents.get_agent_from_id(id_agent)
                ].set_planned_path_from_plan(plan)
            else:
                print("Plan not found for agent :", id_agent, " at timestep:", timestep)

        return agents
