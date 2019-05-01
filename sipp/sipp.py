"""

SIPP implementation  

author: Ashwin Bose (@atb033)

See the article: 10.1109/ICRA.2011.5980306

"""

import argparse
import yaml
from math import fabs
from graph_generation import SippGraph, SippGrid

# TODO: initialization of time interval in the first iteration

class State(object):
    def __init__(self, position, t=0, interval=(0,float('inf'))):
        self.position = tuple(position)
        self.time = t
        self.interval = interval


class SippPlanner(SippGraph):
    def __init__(self, map):
        SippGraph.__init__(self, map)
        self.start = tuple(map["agents"][0]["start"])
        self.goal = tuple(map["agents"][0]["goal"])
        self.open = []

    def get_successors(self, state):
        successors = []
        m_time = 1
        neighbour_list = self.get_valid_neighbours(state.position)

        for neighbour in neighbour_list:
            start_t = state.time + m_time
            end_t = state.interval[1] + m_time
            for i in self.sipp_graph[neighbour].interval_list:
                if i[0] > end_t or i[1] < start_t:
                    continue
                time = max(start_t, i[0]) 
                s = State(neighbour, time, i)
                successors.append(s)
                # print(str(s.position) + str(s.interval))
        return successors

    def get_heuristic(self, position):
        return fabs(position[0] - self.goal[0]) + fabs(position[1]-self.goal[1])

    def compute_plan(self):
        self.open = {}
        goal_reached = False
        cost = 1

        s_start = State(self.start, 0) 

        self.sipp_graph[self.start].g = 0.
        f_start = self.get_heuristic(self.start)
        self.sipp_graph[self.start].f = f_start

        self.open.update({f_start:s_start})

        while (not goal_reached):
            s = self.open.pop(min(self.open.keys()))
            successors = self.get_successors(s)
            for successor in successors:
                if successor.position == self.goal:
                    print("goal reached!!")
                    goal_reached = True
                    break

                if self.sipp_graph[successor.position].g > self.sipp_graph[s.position].g + cost:
                    self.sipp_graph[successor.position].g = self.sipp_graph[s.position].g + cost
                    # TODO: Update time as per publication: but this is already done 
                    # in get_successors(). Not sure how to proceed
                    self.sipp_graph[successor.position].f = self.sipp_graph[successor.position].g + self.get_heuristic(successor.position)
                    self.open.update({self.sipp_graph[successor.position].f:successor})
                # print(successor.position)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("map", help="input file containing map and dynamic obstacles")
    
    args = parser.parse_args()
    
    with open(args.map, 'r') as map_file:
        try:
            map = yaml.load(map_file, Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:
            print(exc)

    sipp_planner = SippPlanner(map)
    # s = State((4,2),3)
    # sipp_planner.get_successor(s)
    sipp_planner.compute_plan()

if __name__ == "__main__":
    main()