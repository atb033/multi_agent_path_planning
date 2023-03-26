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
    map_style_map = {}
    dynamic_obstacles_dict = {}
    n_buffer = 100

    print('a')
    # make the map: this is the dimension and static obstacles 
    map_style_map.update(map_instance.get_map_dict())
    yaml_style_map["map"] = map_style_map
    print(' b')

    # make the agents: this are the agents which need planning 
    for agent in agents.tolist():
        # if the agent has a goal BUT has no planned path, we need a replan
        if (type(agent.get_goal()) != type(None)) and (type(agent.get_planned_path()) == type(None)):
            print('Agent :', agent.get_id(), 'needs a path!')
            temp = {}
            temp['start'] = agent.get_loc()
            temp['goal'] = agent.get_goal()
            temp['name'] = agent.get_id()
            agents_style_map_list.append(temp)
    yaml_style_map['agents'] = agents_style_map_list

    # take all agents with planned_paths, and turn their path into dynamic obstacles
    for agent in agents.tolist():
        # for agents that are in motion
        if (type(agent.get_planned_path()) != type(None)):
            print("agent path needs planning around")
            temp_list = []
            # make dynamic obstacles
            print(len(agent.get_planned_path().get_path()))
            for path_node in agent.get_planned_path().get_path()[1:]:

                print(path_node)


                temp_dict = {}
                loc = path_node.get_loc()
                time = int(path_node.get_time()-timestep)
                temp_dict['x'] = loc[0] # TODO: verify that its [x,y]
                temp_dict['y'] = loc[1] # TODO: verify that its [x,y]
                temp_dict['t'] = time
                temp_list.append(temp_dict)            
            # make non-moving dynamic obstacle from agent last pose
            for _ in range(n_buffer):
                temp_dict = {}
                time += 1
                temp_dict['x'] = loc[0] # TODO: verify that its [x,y]
                temp_dict['y'] = loc[1] # TODO: verify that its [x,y]
                temp_dict['t'] = time
                temp_list.append(temp_dict)            
            dynamic_obstacles_dict[agent.get_id()] = temp_list

        else: 
            # make non-moving dynamic obstacle from agent last pose
            temp_list = []
            loc = agent.get_loc()
            time = int(0)
            for _ in range(n_buffer*2):
                temp_dict = {}
                time += 1
                temp_dict['x'] = loc[0] # TODO: verify that its [x,y]
                temp_dict['y'] = loc[1] # TODO: verify that its [x,y]
                temp_dict['t'] = time
                temp_list.append(temp_dict)            
            dynamic_obstacles_dict[agent.get_id()] = temp_list            

    yaml_style_map['dynamic_obstacles'] = dynamic_obstacles_dict

    return yaml_style_map
