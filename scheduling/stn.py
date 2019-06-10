"""

Simple temporal network 

author: Ashwin Bose (@atb033)

"""


import sys
sys.path.insert(0, '../')
import yaml
import argparse

from scheduling.tpg import Vertex, TemporalPlanGraph
from cbs.cbs import Location

class Edge:
    """
    creating stn edge from tpg edge
    """
    def __init__(self, vertex_a, vertex_b, bound):
        self.bound = bound
        self.vertex_a = vertex_a
        self.vertex_b = vertex_b
    
    def __str__(self):
        return str(self.vertex_a) + ', ' + str(self.vertex_b) + ', ' + str(self.bound)

class SimpleTemporalNetwork:
    def __init__(self, tpg):
        self.tpg = tpg
        self.edges = []

        self.vmax = 1 # maximum velocity of agents

        self.vertices = tpg.augmented_vertices

        self.generate_bounds()
        self.generate_end_edges()

    def generate_bounds(self):
        for edge in self.tpg.augmented_edges:
            lb = edge.edge_length/self.vmax
            ub = float('inf')
            stn_edge = Edge(edge.vertex_a, edge.vertex_b, [lb, ub])
            self.edges.append(stn_edge)

    def generate_end_edges(self):
        start = Vertex('start', Location(-1, -1), -1)
        end  = Vertex('end', Location(-2, -2), -2)

        self.vertices += [start, end]
        bound_start = [0.,0.]
        bound_end = [0.,float('inf')]

        for state in self.tpg.initial_states:
            edge = Edge(start, state, bound_start)
            self.edges.append(edge)
        
        for state in self.tpg.final_states:
            edge = Edge(state, end, bound_end)
            self.edges.append(edge)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output", help="output file with the schedule")
    args = parser.parse_args()

    # Read from input file
    with open(args.output, 'r') as output_file:
        try:
            output = yaml.load(output_file, Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:
            print(exc)

    tpg = TemporalPlanGraph(output['schedule'])

    stn = SimpleTemporalNetwork(tpg)

    for edge in stn.edges:
        print(edge)


if __name__ == "__main__":
    main()
