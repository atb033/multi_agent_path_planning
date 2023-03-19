import yaml 

def make_agent_dict(input):
    with open(input, "r") as input_file:
        try:
            temp = yaml.load(input_file, Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:
            print(exc)
    agents = {}
    for agent in temp["agents"]:    
        agents[agent['name']] = agent['start']
    return agents
    