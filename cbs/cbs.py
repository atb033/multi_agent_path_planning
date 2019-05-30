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
    def __eq__(self, other):
        return self.time == other.time and self.location == other.location
    def __hash__(self):
        return hash(str(self.time)+str(self.location.x) + str(self.location.y))
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
        self.agent_dict = {}

        self.make_agent_dict()

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

    def is_solution(self, agent_name):
        pass

    def admissible_heuristic(self, state, agent_name):
        goal = self.agent_dict[agent_name]["goal"]
        return fabs(state.location.x - goal.location.x) + fabs(state.location.y - goal.location.y)

    def a_star_search(self, agent_name):
        """
        low level search 
        """
        initial_state = self.agent_dict[agent_name]["start"]
        step_cost = 1
        
        closed_set = set()
        open_set = {initial_state}

        came_from = {}

        g_score = {} # default infinity
        g_score[initial_state] = 0

        f_score = {} # default infinity

        f_score[initial_state] = self.admissible_heuristic(initial_state, agent_name)

        counter = 0
    
        while open_set:
            print(counter)
            counter+=1

            temp_dict = {open_item:f_score.setdefault(open_item, float("inf")) for open_item in open_set}
            current = min(temp_dict, key=temp_dict.get)
            print(current)
            if self.is_at_goal(current, agent_name):
                print("goal reached")
                path = self.reconstruct_path(came_from, current)
                for state in path:
                    print(state)
                return self.reconstruct_path(came_from, current)

            open_set -= {current}
            closed_set |= {current}

            neighbor_list = self.get_neighbors(current)

            for neighbor in neighbor_list:
                print("neighbor: " + str(neighbor))
                if neighbor in closed_set:
                    continue
                
                tentative_g_score = g_score.setdefault(current, float("inf")) + step_cost

                if neighbor not in open_set:
                    open_set |= {neighbor}
                elif tentative_g_score >= g_score.setdefault(neighbor, float("inf")):
                    continue

                came_from[neighbor] = current

                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + self.admissible_heuristic(neighbor, agent_name)

    def reconstruct_path(self, came_from, current):
        total_path = [current]
        while current in came_from.keys():
            current = came_from[current]
            total_path.append(current)
        return total_path[::-1]

    def is_at_goal(self, state, agent_name):
        goal_state = self.agent_dict[agent_name]["goal"]
        return state.is_equal_except_time(goal_state)

    def make_agent_dict(self):
        for agent in self.agents:
            start_state = State(0, agent['start'][0], agent['start'][1])
            goal_state = State(0, agent['goal'][0], agent['goal'][1])
            
            self.agent_dict.update({agent['name']:{'start':start_state, 'goal':goal_state}})

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

    # s1 = State(1,1,1)
    vcon = VertexConstraint(1, Location(1,0))
    env.constraints.vertex_constraints.append(vcon)

    # for n in env.get_neighbors(s1):
    #     print(n)
    
    env.a_star_search('agent0')

if __name__ == "__main__":
    main()
