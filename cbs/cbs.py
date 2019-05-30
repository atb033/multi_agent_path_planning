"""

Graph generation for sipp 

author: Ashwin Bose (@atb033)

See the article: 10.1109/ICRA.2011.5980306

"""

import argparse
import yaml
from enum import Enum, auto
from math import fabs

class Location(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    def __str__(self):
        return str((self.x, self.y))

class State(object):
    def __init__(self, time, x, y):
        self.time = time
        self.location = Location(x, y)

    def is_equal_except_time(self, state):
        return self.location == state.location
    def __str__(self):
        return str((self.time, self.location.x, self.location.y))

class VertexConstraint():
    def __init__(self, time, location):
        self.time = time
        self.location = location

    def __eq__(self, other):
        return self.time == other.time and self.location == other.location

class EdgeConstraint(object):
    def __init__(self, time, location_1, location_2):
        self.time = time
        self.location_1 = location_1
        self.location_2 = location_2

class Constraints(object):
    def __init__(self):
        self.vertex_constraints = []
        self.edge_constraints = []

# Chumma :P
class Actions(Enum):
    WAIT = auto()
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

class Environment(object):
    def __init__(self, dimension, agents, obstacles):
        self.dimension = dimension
        self.obstacles = obstacles
        self.agents = agents

        self.make_agent_goal_dict()

        self.constraints = Constraints()

    def get_neighbors(self, state):
        neighbors = []
        
        # Wait action
        n = State(state.time + 1, state.location.x, state.location.y)
        if self.state_valid(n):
            neighbors.append(n)
        # Up action
        n = State(state.time + 1, state.location.x, state.location.y+1)
        if self.state_valid(n) and self.transition_valid(state, n):
            neighbors.append(n)
        # Down action
        n = State(state.time + 1, state.location.x, state.location.y-1)
        if self.state_valid(n) and self.transition_valid(state, n):
            neighbors.append(n)
        # Left action
        n = State(state.time + 1, state.location.x-1, state.location.y)
        if self.state_valid(n) and self.transition_valid(state, n):
            neighbors.append(n)
        # Right action
        n = State(state.time + 1, state.location.x+1, state.location.y)
        if self.state_valid(n) and self.transition_valid(state, n):
            neighbors.append(n)
        return neighbors

        
    def get_first_conflict(self):
        pass

    def create_constraints_from_conflict(self):
        pass

    def get_state(self, agend_id, solution, t):
        pass

    def state_valid(self, state):
        return state.location.x >= 0 and state.location.x < self.dimension[0] \
            and state.location.y >= 0 and state.location.y < self.dimension[1] \
            and VertexConstraint(state.time, state.location) not in self.constraints.vertex_constraints \
            and (state.location.x, state.location.y) not in self.obstacles

    def transition_valid(self, state_1, state_2):
        return EdgeConstraint(state_1.time, state_1.location, state_2.location) not in self.constraints.edge_constraints

    def is_solution(self):
        pass

    def admissible_heuristic(self, state, agent_name):
        goal = self.agent_goal_dict[agent_name]
        return fabs(state.location.x - goal[0]) + fabs(state.location.y - goal[1])

    def a_star_search(self, initial_state, goal_state):
        """
        low level search 
        """
        closed_set = []
        open_set = [initial_state]

        came_from = {}
        

    def make_agent_goal_dict(self):
        self.agent_goal_dict = {}
        for agent in self.agents:
            self.agent_goal_dict.update({agent['name']:agent['goal']})

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("param", help="input file containing map and obstacles")
    args = parser.parse_args()
    
    with open(args.param, 'r') as param_file:
        try:
            param = yaml.load(param_file, Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:
            print(exc)

    # print(param)
    dimension = param["map"]["dimensions"]
    obstacles = param["map"]["obstacles"]
    agents = param['agents']

    env = Environment(dimension, agents, obstacles)

    s1 = State(1,1,1)
    vcon = VertexConstraint(2, Location(1,0))
    env.constraints.vertex_constraints.append(vcon)

    for n in env.get_neighbors(s1):
        print(n)
    


if __name__ == "__main__":
    main()
