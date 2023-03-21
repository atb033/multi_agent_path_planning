import typing

from multi_agent_path_planning.lifelong_MAPF.datastuctures import (
    AgentSet,
    Assignment,
    Task,
)


class BaseTaskAllocator:
    """
    Def
    """

    def allocate_tasks(
        self, tasks: typing.List[Task], agents: AgentSet
    ) -> typing.List[Assignment]:
        """
        Arguments:
            tasks: The open tasks
            agents:

        Returns:
            Agents updated with assignments
        """
        return agents
