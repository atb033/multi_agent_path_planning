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
        self.edges = list(self.stn.edges)

        self.vertices = list(self.stn.vertices)
        self.variables = self.get_variables()

    def optimize(self):
        
        (A_in, b_in) = self.get_inequality_constraints()
        (A_equ, b_equ) = self.get_equality_constraints()
        c = self.get_cost_matrix()

        res = linprog(c, A_ub=A_in, b_ub=b_in, A_eq=A_equ, b_eq=b_equ)
        # res = linprog(c, A_ub=A_in, b_ub=b_in)

        print(res)

    # def generate_
    def get_cost_function(self, variables):
        for i, v in enumerate(self.vertices):
            self.vertices[i].cost = variables[i]
        for v in self.vertices:
            if v.agent == 'end':
                return v.cost

    def get_cost_matrix(self):        
        A = [0.]*len(self.vertices)
        for i, v in enumerate(self.vertices):
            if v.agent == 'end':
                A[i] = 1
        return A

    def get_variables(self):
        variables = []
        for v in self.vertices:
            print(v)
            variables.append(v.cost)
        return variables

    def get_inequality_constraints(self):
        A = []
        b = []
        for edge in self.edges:
            index_a = -1
            index_b = -1
            for i, v in enumerate(self.vertices):
                if v == edge.vertex_a:
                    index_a = i
                if v == edge.vertex_b:
                    index_b = i
            # lower bound
            row = [0.]*len(self.vertices)
            row[index_a] = 1
            row[index_b] = -1
            lb = edge.bound[0]
            A.append(row)
            b.append(-lb)

            print(str(row) + ',  ' + str(-lb))
            
            # upper bound
            row = [0.]*len(self.vertices)
            row[index_b] = 1
            row[index_a] = -1
            ub = edge.bound[1]
            if ub == float('inf') : continue
            
            print(str(row) + ',  ' + str(ub))

            A.append(row)
            b.append(ub)

        return (A, b)

    def get_equality_constraints(self):
        A = []
        b = 0
        for i, v in enumerate(self.vertices):
            if v.agent == 'start':
                row = [0.]*len(self.vertices)
                row[i] = 1
                A.append(row)
        return (A, b)

                
            
    

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

    optimize.optimize()


if __name__ == "__main__":
    main()