import yaml
from datastuctures import AgentSet, Agent


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
