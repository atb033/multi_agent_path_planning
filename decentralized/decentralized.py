import velocity_obstacle.velocity_obstacle as velocity_obstacle
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-m", "--mode", help="mode of obstacle avoidance; options: velocity_obstacle, or nmpc")
    parser.add_argument(
        "-f", "--filename", help="filename, in case you want to save the animation")

    args = parser.parse_args()
    if args.mode == "velocity_obstacle":
        velocity_obstacle.simulate(args.filename)
    if args.mode == "nmpc":
        print("nmpc is currently not implemented")
    else:
        print("Please enter mode 0 or 1")
