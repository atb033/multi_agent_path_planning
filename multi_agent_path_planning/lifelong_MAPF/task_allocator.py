import typing

from multi_agent_path_planning.lifelong_MAPF.datastuctures import (Agent,
                                                                   Assignment,
                                                                   Task)


class BaseTaskAllocator:
    """
    Def
    """

    def allocate_tasks(
        self, tasks: typing.List[Task], agents: typing.Dict[int, Agent]
    ) -> typing.List[Assignment]:
        """
        Arguments:
            tasks: The open tasks
            agents:

        Returns:
            a list of assignments
        """
        return []
