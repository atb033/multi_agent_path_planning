class BaseTaskFactory:
    """
    Def
    """

    def produce_tasks(self, timestep: int = None):
        """
        Args:
            timestep: The current simulation timestep
        Returns:
            tasks: A list of Tasks
            complete: Is the factory done producing tasks
        """
        return [], True
