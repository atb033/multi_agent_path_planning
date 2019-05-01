"""

Graph generation for sipp 

author: Ashwin Bose (@atb033)

See the article: 10.1109/ICRA.2011.5980306

"""

import argparse
import yaml
from bisect import bisect

class SippGrid(object):
    def __init__(self):
        # self.position = ()
        self.interval_list = [(0, float('inf'))]
    def split_interval(self, t):
        for interval in self.interval_list:
            if t == interval[0]:
                self.interval_list.remove(interval)
                if t+1 <= interval[1]:
                    self.interval_list.append((t+1, interval[1]))
            elif t == interval[1]:
                self.interval_list.remove(interval)
                if t-1 <= interval[0]:
                    self.interval_list.append((interval[0],t-1))
            elif bisect(interval,t) == 1:
                self.interval_list.remove(interval)
                self.interval_list.append((interval[0], t-1))
                self.interval_list.append((t+1, interval[1]))
            self.interval_list.sort()

class SippGraph(object):
    def __init__(self, map):
        self.map = map
        self.dimensions = map["map"]["dimensions"]
        self.obstacles = map["dynamic_obstacles"]
        self.sipp_graph = {}
        self.init_graph()

    def init_graph(self):
        for i in range(self.dimensions[0]):
            for j in range(self.dimensions[1]):
                grid_dict = {(i,j):SippGrid()}
                self.sipp_graph.update(grid_dict)

    def init_intervals(self):
        for obstacle, schedule in self.obstacles.items():
            for location in schedule:
                position = (location["x"],location["y"])
                t = location["t"]
                self.sipp_graph[position].split_interval(t)
                # print(str(position) + str(self.sipp_graph[position].interval_list))
            

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("map", help="input file containing map and dynamic obstacles")
    args = parser.parse_args()
    
    with open(args.map, 'r') as map_file:
        try:
            map = yaml.load(map_file, Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:
            print(exc)

    graph = SippGraph(map)
    graph.init_intervals()
