import sys
sys.path.insert(0, '../')
import yaml
import argparse

from scheduling.tpg import Vertex, TemporalPlanGraph
from scheduling.stn import SimpleTemporalNetwork
from cbs.cbs import Location

from scipy.optimize import linprog

class OptimizationClass:
    def __init__(self, stn):
        self.stn = stn
        self.stn.edges = list(self.stn.edges)
        self.stn.vertices = list(self.stn.vertices)
        self.variables = self.get_variables()
        self.generate_constraint_matrix()

    # def generate_
    def get_cost_function(self, variables):
        for i, v in enumerate(self.stn.vertices):
            self.stn.vertices[i].cost = variables[i]
        for v in self.stn.vertices:
            if v.agent == 'end':
                return v.cost

    def get_variables(self):
        variables = []
        for v in self.stn.vertices:
            variables.append(v.cost)
        return variables

    def generate_constraint_matrix(self):
        for i, edge in enumerate(self.stn.edges):
            if i==1 : return
            for v in self.stn.vertices:
                if v == edge.vertex_a:
                    print(v)
    

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

    optimize = OptimizationClass(stn)



if __name__ == "__main__":
    main()