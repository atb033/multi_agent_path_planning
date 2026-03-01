import os
import sys

import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cbs.cbs import Environment, CBS

@pytest.mark.timeout(5)  # Timeout after 5 seconds
def test_cbs_two_agents():

    """
    X X O X X
    a b O B A

    a, b: agent starts
    A, B: agent goals
    X: obstacle
    O: space
    """
    dimension = [5, 2]
    obstacles = [(0, 1), (1,1), (3,1), (4,1)]

    agents = [
        {"start": [0, 0], "goal": [4, 0], "name": "A"},
        {"start": [1, 0], "goal": [3, 0], "name": "B"},
    ]


    env = Environment(dimension, agents, obstacles)
    cbs = CBS(env)

    solution = cbs.search()

    assert solution is not None

    assert solution["A"][-1]["x"] == 4
    assert solution["A"][-1]["y"] == 0

    assert solution["B"][-1]["x"] == 3
    assert solution["B"][-1]["y"] == 0
