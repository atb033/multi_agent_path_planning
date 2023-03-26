import yaml
from datastuctures import AgentSet, Agent, Map


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
            print(exc)
    # encorporate the actual agent class!
    agent_list = []
    for agent in temp["agents"]:
        agent_list.append(Agent(loc=agent["start"], ID=agent["name"]))
    agent_set = AgentSet(agent_list)
    return agent_set

def make_map_dict_dynamic_obs(map_instance: Map, agents: AgentSet, timestep: int,):

    yaml_style_map = {}
    agents_style_map_list = []
    agents_style_map_dict = {}
    map_style_map = {}
    dynamic_obstacles_dict = {}

    # make the map: this is the dimension and static obstacles 
    map_style_map.update(map_instance.get_map_dict())

    # make the agents: this are the agents which need planning 
    for agent in agents.tolist():
        if (type(agent.get_goal()) != type(None)) and (type(agent.get_planned_path()) == type(None)):
            print('Agent :', agent.get_id(), 'needs a path!')
            temp = {}
            temp['start'] = agent.get_loc()
            temp['goal'] = agent.get_goal()
            temp['name'] = agent.get_id()
            agents_style_map.append(temp)
    agents_style_map_dict['agents'] = agents_style_map
    map_style_map.update(agents_style_map_dict)

    # take all agents with planned_paths, and turn their path into dynamic obstacles
    for agent in agents.tolist():
        if (type(agent.get_planned_path()) != type(None)):
            temp_list = []
            for path_node in agent.get_planned_path().get_path():
                temp_dict = {}
                temp_dict['x'] = path_node.get_loc()[0] # TODO: verify that its [x,y]
                temp_dict['y'] = path_node.get_loc()[1] # TODO: verify that its [x,y]
                temp_dict['t'] = int(path_node.get_time()-timestep)
                temp_list.append(temp_dict)
            dynamic_obstacles_dict[agent.get_id()] = temp_list
            
    agents_style_map_dict['agents'] = agents_style_map
    map_style_map.update(agents_style_map_dict)





    return yaml_style_map
