import typing

from multi_agent_path_planning.lifelong_MAPF.datastuctures import (
    Map,
    Path,
    AgentSet,
)

from multi_agent_path_planning.centralized.sipp.sipp import SippPlanner
from multi_agent_path_planning.lifelong_MAPF.helpers import make_map_dict_dynamic_obs

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
        # TODO: finish this function 
        temp_map = make_map_dict_dynamic_obs(map_instance=map_instance, agents=agents, timestep=1)

        if not temp_map.__contains__("agents"):

            print('No Agent Replans at Timestep :', timestep)

            return agents

        for agent in temp_map["agents"]:

            id_agent = agent["name"]

            sipp_planner = SippPlanner(temp_map, id_agent)

            if sipp_planner.compute_plan():

                plan = sipp_planner.get_plan()

                temp_map["dynamic_obstacles"].update(plan)
        
                # TODO: finish this function 
                agent.set_planned_path_from_plan(plan)

            else:
                print("Plan not found for agent :", id_agent, " at timestep:", timestep)

        return agents




        
