import argparse

from multi_agent_path_planning.decentralized.nmpc import nmpc
from multi_agent_path_planning.decentralized.velocity_obstacle import (
    velocity_obstacle as velocity_obstacle,
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-m",
        "--mode",
        help="mode of obstacle avoidance; options: velocity_obstacle, or nmpc",
    )
    parser.add_argument(
        "-f", "--filename", help="filename, in case you want to save the animation"
    )

    args = parser.parse_args()
    if args.mode == "velocity_obstacle":
        velocity_obstacle.simulate(args.filename)
    elif args.mode == "nmpc":
        nmpc.simulate(args.filename)
    else:
        print("Please enter mode the desired mode: velocity_obstacle or nmpc")
