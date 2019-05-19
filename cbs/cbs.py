"""

Graph generation for sipp 

author: Ashwin Bose (@atb033)

See the article: 10.1109/ICRA.2011.5980306

"""

import argparse
import yaml

class State(object):
    def __init__(self, time, x, y):
        self.time = time
        self.x = x
        self.y = y

    def is_equal_except_time(self, state):
        return self.x == state.x and self.y == state.y


