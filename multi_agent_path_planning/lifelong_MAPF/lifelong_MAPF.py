import argparse
import typing

from multi_agent_path_planning.lifelong_MAPF.datastuctures import Agent, Map, TaskSet
from multi_agent_path_planning.lifelong_MAPF.dynamics_simulator import (
    BaseDynamicsSimulator,
)
from multi_agent_path_planning.lifelong_MAPF.helpers import *
from multi_agent_path_planning.lifelong_MAPF.mapf_solver import BaseMAPFSolver
from multi_agent_path_planning.lifelong_MAPF.task_allocator import (
    BaseTaskAllocator,
    RandomTaskAllocator,
)
from multi_agent_path_planning.lifelong_MAPF.task_factory import (
    BaseTaskFactory,
    RandomTaskFactory,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="input file")
    parser.add_argument("output", help="output file with the schedule")
    args = parser.parse_args()

    world_map = Map(args.input)

    output = lifelong_MAPF_experiment(
        map_instance=world_map,
        initial_agents=make_agent_set(args.input),
        task_factory=RandomTaskFactory(world_map),
        task_allocator=RandomTaskAllocator(),
        mapf_solver=BaseMAPFSolver(),
        dynamics_simulator=BaseDynamicsSimulator(),
    )

    # refine this later
    with open(args.output, "w") as output_yaml:
        yaml.safe_dump(output, output_yaml)


def lifelong_MAPF_experiment(
    map_instance: Map,
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
    open_tasks = TaskSet()

    # TODO: fix comment
    # This is the set of agents which are ready to accept a new task assignment
    agents = initial_agents

    # Agents are not all at their goals
    agents_at_goals = False

    # Run for a fixed number of timesteps
    for timestep in range(max_timesteps):
        # Ask the task factory for new task
        new_tasks, no_new_tasks = task_factory.produce_tasks(timestep=timestep)
        # Add them to the existing list
        open_tasks.add_tasks(new_tasks)

        # If there are no current tasks and the factory says there won't be any more
        # and all the agents are at the goal, break
        if len(open_tasks) == 0 and no_new_tasks and agents_at_goals:
            break

        # Assign the open tasks to the open agents
        agents = task_allocator.allocate_tasks(open_tasks, agents)

        # Plan all the required paths. This can both be to get the agents to the starts of tasks
        # or get from their current location to the goal
        agents = mapf_solver.solve_MAPF_instance(
            map=map_instance, agents=agents, timestep=timestep,
        )

        # Step the simulation one step and record the paths
        (agents, agents_at_goals) = dynamics_simulator.step_world(
            agents=agents, timestep=timestep,
        )

    executed_paths = agents.get_executed_paths()
    return executed_paths


if __name__ == "__main__":
    paths = main()
