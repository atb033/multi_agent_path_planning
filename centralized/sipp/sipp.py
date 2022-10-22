"""

SIPP implementation  

author: Ashwin Bose (@atb033)

See the article: DOI: 10.1109/ICRA.2011.5980306

"""

import argparse
import yaml
from math import fabs
from graph_generation import SippGraph, State

class SippPlanner(SippGraph):
    def __init__(self, map, agent_id):
        SippGraph.__init__(self, map)
        self.start = tuple(map["agents"][agent_id]["start"])
        self.goal = tuple(map["agents"][agent_id]["goal"])
        self.name = map["agents"][agent_id]["name"]
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
        return successors

    def get_heuristic(self, position):
        return fabs(position[0] - self.goal[0]) + fabs(position[1]-self.goal[1])

    def compute_plan(self):
        self.open = []
        goal_reached = False
        cost = 1

        s_start = State(self.start, 0) 

        self.sipp_graph[self.start].g = 0.
        f_start = self.get_heuristic(self.start)
        self.sipp_graph[self.start].f = f_start

        self.open.append((f_start, s_start))

        while (not goal_reached):
            if self.open == {}: 
                # Plan not found
                return 0
            s = self.open.pop(0)[1]
            successors = self.get_successors(s)
    
            for successor in successors:
                if self.sipp_graph[successor.position].g > self.sipp_graph[s.position].g + cost:
                    self.sipp_graph[successor.position].g = self.sipp_graph[s.position].g + cost
                    self.sipp_graph[successor.position].parent_state = s

                    if successor.position == self.goal:
                        print("Plan successfully calculated!!")
                        goal_reached = True
                        break

                    self.sipp_graph[successor.position].f = self.sipp_graph[successor.position].g + self.get_heuristic(successor.position)
                    self.open.append((self.sipp_graph[successor.position].f, successor))

        # Tracking back
        start_reached = False
        self.plan = []
        current = successor
        while not start_reached:
            self.plan.insert(0,current)
            if current.position == self.start:
                start_reached = True
            current = self.sipp_graph[current.position].parent_state
        return 1
            
    def get_plan(self):
        path_list = []

        # first setpoint
        setpoint = self.plan[0]
        temp_dict = {"x":setpoint.position[0], "y":setpoint.position[1], "t":setpoint.time}
        path_list.append(temp_dict)

        for i in range(len(self.plan)-1):
            for j in range(self.plan[i+1].time - self.plan[i].time-1):
                x = self.plan[i].position[0]
                y = self.plan[i].position[1]
                t = self.plan[i].time
                setpoint = self.plan[i]
                temp_dict = {"x":x, "y":y, "t":t+j+1}
                path_list.append(temp_dict)

            setpoint = self.plan[i+1]
            temp_dict = {"x":setpoint.position[0], "y":setpoint.position[1], "t":setpoint.time}
            path_list.append(temp_dict)

        data = {self.name:path_list}
        return data



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("map", help="input file containing map and dynamic obstacles")
    parser.add_argument("output", help="output file with the schedule")
    
    args = parser.parse_args()
    
    with open(args.map, 'r') as map_file:
        try:
            map = yaml.load(map_file, Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:
            print(exc)


    output = dict()
    output["schedule"] = dict()

    # compute first plan
    sipp_planner = SippPlanner(map,0)

    if sipp_planner.compute_plan():
        plan = sipp_planner.get_plan()
        output["schedule"].update(plan)
        with open(args.output, 'w') as output_yaml:
            yaml.safe_dump(output, output_yaml)  
    else: 
        print("Plan not found")


if __name__ == "__main__":
    main()