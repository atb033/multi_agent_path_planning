"""

Construction of Temporal Plan Graph (TPG)

author: Ashwin Bose (@atb033)

"""
import sys
sys.path.insert(0, '../')
import yaml
import argparse

from cbs.cbs import Location

class Vertex:
    def __init__(self, agent, location, time):
        self.agent = agent
        self.location = location
        self.time = time
        self.cost = 0
    def __str__(self):
        return str(self.agent + ' t: ' + str(self.time) + ': ' + str(self.location)  )
    def __eq__(self, other):
        return self.agent == other.agent and self.location == other.location and self.time == other.time
    def __hash__(self):
        return hash(str(self.agent)+str(self.location) + str(self.time))

class Edge:
    def __init__(self, vertex_a, vertex_b):
        self.vertex_a = vertex_a
        self.vertex_b = vertex_b
        self.edge_length = self.compute_edge_length()
    def __str__(self):
        return str(self.vertex_a)  + ', ' + str(self.vertex_b)
    def compute_edge_length(self):
        return ((self.vertex_a.location.x - self.vertex_b.location.x ) ** 2 + \
            (self.vertex_a.location.y - self.vertex_b.location.y ) ** 2) ** 0.5

class TemporalPlanGraph:
    def __init__(self, schedule):

        self.delta = 0.2 # safety distance

        self.schedule = schedule

        self.vertices = []
        self.edges_type_1 = []
        self.edges_type_2 = []

        self.generate_tpg()
        self.augment_graph()

        self.initial_states = []
        self.final_states = []
        self.generate_initial_final_states()

    def generate_tpg(self):
        # Creating type-1 edges
        for agent, plan in self.schedule.items():
            vertex = Vertex(agent, Location(plan[0]['x'], plan[0]['y']), plan[0]['t'])
            self.vertices.append(vertex)
            i_prev = 0
            for i in range(len(plan)-1):
                location_a = Location(plan[i_prev]['x'], plan[i_prev]['y'])
                location_b = Location(plan[i+1]['x'], plan[i+1]['y'])
                if not location_a == location_b:
                    vertex_a = Vertex(agent, location_a, plan[i_prev]['t'])
                    vertex_b = Vertex(agent, location_b, plan[i+1]['t'])
                    self.vertices.append(vertex_b)
                    
                    edge_ab = Edge(vertex_a, vertex_b)
                    self.edges_type_1.append(edge_ab)
                    i_prev = i+1
        # Creating type-2 edges
        for agent_j, plan_j in self.schedule.items():
            for t_j in range(len(plan_j)):
                s_tj = Location(plan_j[t_j]['x'], plan_j[t_j]['y'])
                v_tj = Vertex(agent_j, s_tj, plan_j[t_j]['t'])
                if v_tj in self.vertices:
                    for agent_k, plan_k in self.schedule.items():
                        if agent_j is not agent_k:
                            for t_k in range(t_j, len(plan_k)):
                                s_tk = Location(plan_k[t_k]['x'], plan_k[t_k]['y'])
                                v_tk = Vertex(agent_k, s_tk, plan_k[t_k]['t'])
                                if v_tk in self.vertices and s_tk==s_tj:
                                    edge = Edge(v_tj, v_tk)
                                    self.edges_type_2.append(edge)

    def augment_graph(self):
        self.augmented_edges = []
        self.augmented_vertices = self.vertices
        
        for edge in self.edges_type_1:
            v1 = self.return_safety_vertex(edge.vertex_a, 1)
            v2 = self.return_safety_vertex(edge.vertex_b, -1)

            self.augmented_vertices += [v1, v2]

            edge1 = Edge(edge.vertex_a, v1)
            edge2 = Edge(v1, v2)
            edge3 = Edge(v2, edge.vertex_b)

            self.augmented_edges += [edge1,edge2,edge3]

        for edge_t2 in self.edges_type_2:
            v1 = self.return_safety_vertex(edge_t2.vertex_a, 1)
            v2 = self.return_safety_vertex(edge_t2.vertex_b, -1)

            if not (v1 and v2):
                continue
            edge4 = Edge(v1, v2)
            edge4.edge_length = 0
            self.augmented_edges.append(edge4)

    def return_safety_vertex(self, vertex, side=-1):
        """
        returns a safety vertex in a side (-1 or +1)
        """
        for edge in self.edges_type_1:
            if side == -1:
                if vertex == edge.vertex_b:
                    dir = [edge.vertex_b.location.x - edge.vertex_a.location.x, \
                        edge.vertex_b.location.y - edge.vertex_a.location.y]
                    mag = (dir[0]**2 + dir[1] ** 2) **0.5
                    dir = [dir[0]/mag, dir[1]/mag]

                    new_loc_x = vertex.location.x - self.delta * dir[0]
                    new_loc_y = vertex.location.y - self.delta * dir[1]
                    new_loc = Location(new_loc_x, new_loc_y)

                    new_vertex = Vertex(vertex.agent, new_loc, vertex.time-0.1)
                    return new_vertex
            if side == 1:
                if vertex == edge.vertex_a:
                    dir = [edge.vertex_b.location.x - edge.vertex_a.location.x, \
                        edge.vertex_b.location.y - edge.vertex_a.location.y]
                    mag = (dir[0]**2 + dir[1] ** 2) **0.5
                    dir = [dir[0]/mag, dir[1]/mag]

                    new_loc_x = vertex.location.x + self.delta * dir[0]
                    new_loc_y = vertex.location.y + self.delta * dir[1]
                    new_loc = Location(new_loc_x, new_loc_y)

                    new_vertex = Vertex(vertex.agent, new_loc, vertex.time+0.1)
                    return new_vertex
        return False

    def generate_initial_final_states(self):
        for agent, plan in self.schedule.items():
            init_state = Vertex(agent, Location(plan[0]['x'], plan[0]['y']), plan[0]['t'])
            final_state = Vertex(agent, Location(plan[-1]['x'], plan[-1]['y']), plan[-1]['t'])

            self.initial_states.append(init_state)
            self.final_states.append(final_state)


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

    tpg.augment_graph()


if __name__ == "__main__":
    main()
