import yaml
from datastuctures import Agent, AgentSet, Map
import logging


def make_agent_set(input):
    """_summary_

    Args:
        input (_type_): _description_

    Returns:
        _type_: _description_
    """
    with open(input, "r") as input_file:
        try:
            temp = yaml.load(input_file, Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:
            logging.error(exc)
    # encorporate the actual agent class!
    agent_list = []
    for agent in temp["agents"]:
        agent_list.append(Agent(loc=agent["start"], ID=agent["name"]))
    agent_set = AgentSet(agent_list)
    return agent_set


def make_map_dict_dynamic_obs(
    map_instance: Map, agents: AgentSet, timestep: int,
):
    yaml_style_map = {}
    agents_style_map_list = []
    map_style_map = {}
    dynamic_obstacles_dict = {}
    n_buffer = 100

    # make the map: this is the dimension and static obstacles
    map_style_map.update(map_instance.get_map_dict())
    yaml_style_map["map"] = map_style_map

    # make the agents: this are the agents which need planning
    for agent in agents.tolist():
        # if the agent has a goal BUT has no planned path, we need a replan, so add to agent list
        if (type(agent.get_goal()) != type(None)) and (
            type(agent.get_planned_path()) == type(None)
        ):
            logging.info(f"Agent : {agent.get_id()} needs a path!")
            temp = {}
            temp["start"] = agent.get_loc().as_xy()  # TODO verify this is what's needed
            temp["goal"] = agent.get_goal().as_xy()  # TODO same as above
            temp["name"] = agent.get_id()
            agents_style_map_list.append(temp)
            yaml_style_map["agents"] = agents_style_map_list
        # take all agents with planned_paths, and turn their path into dynamic obstacles
        # for agents that are in motion
        elif type(agent.get_planned_path()) != type(None):
            logging.info(f"Agent : {agent.get_id()} needs planning around!")
            temp_list = []
            # TODO is this the correct default if no paths are planned
            time = agent.timestep
            loc = agent.get_loc()

            # make dynamic obstacles
            for path_node in agent.get_planned_path().get_path():
                temp_dict = {}

                loc = path_node.get_loc()
                time = int(path_node.get_time())

                temp_dict["x"] = loc.x()
                temp_dict["y"] = loc.y()
                temp_dict["t"] = time
                temp_list.append(temp_dict)
            # make non-moving dynamic obstacle from agent last pose
            for _ in range(n_buffer):
                temp_dict = {}
                time += 1
                temp_dict["x"] = loc.x()
                temp_dict["y"] = loc.y()
                temp_dict["t"] = time
                temp_list.append(temp_dict)
            dynamic_obstacles_dict[agent.get_id()] = temp_list

        # for stationary agents
        else:
            logging.info(f"Agent : {agent.get_id()} is stationary")
            # make non-moving dynamic obstacle from agent last pose
            temp_list = []
            loc = agent.get_loc()
            time = timestep
            for _ in range(n_buffer * 2):
                temp_dict = {}
                time += 1
                temp_dict["x"] = loc.x()
                temp_dict["y"] = loc.y()
                temp_dict["t"] = time
                temp_list.append(temp_dict)
            dynamic_obstacles_dict[agent.get_id()] = temp_list

    yaml_style_map["dynamic_obstacles"] = dynamic_obstacles_dict

    return yaml_style_map
