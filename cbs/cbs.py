"""

Graph generation for sipp 

author: Ashwin Bose (@atb033)

See the article: 10.1109/ICRA.2011.5980306

"""

import argparse
import yaml
from enum import Enum, auto

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
    def __init__(self, dimension, obstacles):
        self.dimension = dimension
        self.obstacles = obstacles

        self.constraints = Constraints()

        vcon = VertexConstraint(2, Location(1,0))
        self.constraints.vertex_constraints.append(vcon)

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
            and VertexConstraint(state.time, state.location) not in self.constraints.vertex_constraints

    def transition_valid(self, state_1, state_2):
        return EdgeConstraint(state_1.time, state_1.location, state_2.location) not in self.constraints.edge_constraints

    def is_solution(self):
        pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("map", help="input file containing map and obstacles")
    args = parser.parse_args()
    
    with open(args.map, 'r') as map_file:
        try:
            map = yaml.load(map_file, Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:
            print(exc)

    # print(map)
    dimension = map["map"]["dimensions"]
    obstacles = map["map"]["obstacles"]
    env = Environment(dimension, obstacles)
    s1 = State(1,1,1)
    for n in env.get_neighbors(s1):
        print(n)
    


if __name__ == "__main__":
    main()
