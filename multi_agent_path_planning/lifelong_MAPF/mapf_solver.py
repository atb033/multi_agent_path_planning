import typing

from multi_agent_path_planning.lifelong_MAPF.datastuctures import Assignment, Map, Path


class BaseMAPFSolver:
    """
    Def
    """

    def solve_MAPF_instance(
        self,
        map: Map,
        assignments: typing.List[Assignment],
        planned_paths: typing.List[Path],
        timestep: int,
    ) -> typing.List[Path]:
        """
        Arguments:
            map: The map representation
            assignments: The assignments that must be completed
            planned_paths: The already planned paths
            timestep: The simulation timestep
        """
        return []