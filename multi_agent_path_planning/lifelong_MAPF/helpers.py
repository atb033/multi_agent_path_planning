import yaml


def make_agent_dict(input):
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
    agents = {}
    for agent in temp["agents"]:
        # encorporate the actual agent class!
        agents[agent["name"]] = agent["start"]
    return agents
