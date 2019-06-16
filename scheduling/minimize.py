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
        self.vertices = sorted(self.vertices, key = lambda i:(i.agent, i.time))
        self.agent_names = list(set([i.agent for i in self.vertices])-{'start', 'end'})

    def optimize(self):
        
        (A_in, b_in) = self.get_inequality_constraints()
        (A_equ, b_equ) = self.get_equality_constraints()
        c = self.get_cost_matrix()

        res = linprog(c, A_ub=A_in, b_ub=b_in, A_eq=A_equ, b_eq=b_equ)

        return res

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
            # upper bound
            row = [0.]*len(self.vertices)
            row[index_b] = 1
            row[index_a] = -1
            ub = edge.bound[1]
            if ub == float('inf') : continue

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

    def generate_schedule(self):
        schedule_list = self.optimize()
        schedule = {agent_name: [] for agent_name in self.agent_names}

        # output_list
        for i in  range(len(self.vertices)):
            for agent_name in self.agent_names:
                if self.vertices[i].agent == agent_name:
                    point = {}
                    point['x'] = self.vertices[i].location.x
                    point['y'] = self.vertices[i].location.y
                    point['t'] = float("{0:.3f}".format(schedule_list.x[i]))

                    schedule[agent_name].append(point)           

        return schedule

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("plan", help="plan file with the schedule")
    parser.add_argument("real_schedule", help="plan file with the schedule")
    args = parser.parse_args()

    # Read from input file
    with open(args.plan, 'r') as plan_file:
        try:
            plan = yaml.load(plan_file, Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:
            print(exc)

    tpg = TemporalPlanGraph(plan['schedule'])
    stn = SimpleTemporalNetwork(tpg)
    opt = OptimizationClass(stn)
    schedule = opt.generate_schedule()

    with open(args.real_schedule, 'w') as real_schedule_yaml:
        yaml.dump(schedule, real_schedule_yaml, default_flow_style=False)

if __name__ == "__main__":
    main()