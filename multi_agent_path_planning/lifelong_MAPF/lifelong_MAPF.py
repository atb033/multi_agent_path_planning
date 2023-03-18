import typing

from multi_agent_path_planning.lifelong_MAPF.datastuctures import Agent
from multi_agent_path_planning.lifelong_MAPF.dynamics_simulator import (
    BaseDynamicsSimulator,
)
from multi_agent_path_planning.lifelong_MAPF.mapf_solver import BaseMAPFSolver
from multi_agent_path_planning.lifelong_MAPF.task_allocator import BaseTaskAllocator
from multi_agent_path_planning.lifelong_MAPF.task_factory import BaseTaskFactory


def lifelong_MAPF_experiment(
    map_instance,
    initial_agents: typing.Dict[int, Agent],
    task_factory: BaseTaskFactory,
    task_allocator: BaseTaskAllocator,
    mapf_solver: BaseMAPFSolver,
    dynamics_simulator: BaseDynamicsSimulator,
    max_timesteps: int = 100,
):
    """
    Arguments:
        map_instance: The obstacles and extent
        initial_agents: a dict mapping from agent IDs to the location
        task_factory: Creates the tasks
        task_allocator: Allocates the tasks
        mapf_solver: Solves a MAPF instance,
        max_timesteps: How many timesteps to run the simulation for
    """
    # The set of tasks which need to be exected
    # It should be a List[Task]
    open_tasks = []

    # This is the set of agents which are ready to accept a new task assignment
    # It should be a dict[int, Agent]
    unallocated_agents = initial_agents

    # This is the set of agents which are already assigned to a location. This location could
    # either be the start or goal of a task
    # It should be a dict[int, Agent]
    allocated_agents = {}

    # The paths which have already been planned
    # Should be a List[Path]
    planned_paths = []

    # The list of locations which have already been visited by each agent.
    # It should be a List[Path]
    completed_paths = []

    # Agents are not all at their goals
    agents_at_goals = False

    # Run for a fixed number of timesteps
    for timestep in range(max_timesteps):
        # Ask the task factory for new task
        new_tasks, no_new_tasks = task_factory.produce_tasks(timestep=timestep)
        # Add them to the existing list
        open_tasks.extend(new_tasks)

        # If there are no current tasks and the factory says there won't be any more
        # and all the agents are at the goal, break
        if len(open_tasks) == 0 and no_new_tasks and agents_at_goals:
            break

        # Assign the open tasks to the open agents
        assigned_tasks = task_allocator.allocate_tasks(open_tasks, unallocated_agents)

        # Plan all the required paths. This can both be to get the agents to the starts of tasks
        # or get from their current location to the goal
        planned_paths = mapf_solver.solve_MAPF_instance(
            map=map,
            assignments=assigned_tasks,
            planned_paths=planned_paths,
            timestep=timestep,
        )

        # Step the simulation one step and record the paths
        (
            completed_paths,
            allocated_agents,
            unallocated_agents,
            agents_at_goals,
        ) = dynamics_simulator.step_world(
            planned_paths=planned_paths,
            completed_paths=completed_paths,
            allocated_agents=allocated_agents,
            unallocated_agents=unallocated_agents,
            timestep=timestep,
        )

    return completed_paths


if __name__ == "__main__":
    lifelong_MAPF_experiment(
        None,
        initial_agents={},
        task_factory=BaseTaskFactory(),
        task_allocator=BaseTaskAllocator(),
        mapf_solver=BaseMAPFSolver(),
        dynamics_simulator=BaseDynamicsSimulator(),
    )
