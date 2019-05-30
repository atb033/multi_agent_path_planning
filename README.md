# Multi-Agent path planning in python

# Introduction
This repository consists of the implementation of some multi-agent path-planning algorithms in Python. Two methods, namely Safe-Interval Path Planning, and Conflict-Based Search are implemented
 
The dimensions of the map, obstacles, and initial and final positions of the agents must be mentioned in input.yaml. 

The output is generated and stored in output.yaml.
# Table of contents
 * [Safe-Interval Path Planning (SIPP)](#safe-interval-path-planning) 
 * [Conflict-Based Search (CBS)](#conflict-based-search) 

# Safe-Interval Path Planning
SIPP is a local planner, using which, a collision-free plan can be generated, after considering the static and dynamic obstacles in the environment. In the case of multi-agent path planning, the other agents in the environment are considered as dynamic obstacles. 

## Execution

Please run the following commands to generate a plan. 


For SIPP single-agent planning with dynamic obstacles: 
```
cd ./sipp
python3 sipp.py input.yaml output.yaml
```

For SIPP multi-agent prioritized planning:
```
python3 multi_sipp.py input.yaml output.yaml
```

## Results
To visualize the generated results

```
python3 visualize_sipp.py input.yaml output.yaml 
```
To record video

```
python3 visualize_sipp.py input.yaml output.yaml --video 'sipp.avi' --speed 1
```

Test 1 (Success)                        | Test 2 (Failure)
:--------------------------------------:|:-------------------------:
![Success](./sipp/results/success.gif)  |![Failure](./sipp/results/failure.gif)

# Conflict Based Search
Conclict-Based Search (CBS), is a multi-agent global path planner. 

## Execution 
Run the following command:
```
cd ./cbs
python3 cbs.py input.yaml output.yaml
```

## Results
To visualize the generated results:
```
python3 ../visualize.py input.yaml output.yaml
```

Test 1 (Success                         | Test 2 (Success)
:--------------------------------------:|:-------------------------:
![Success](./cbs/results/test_1.gif)  |![Failure](./cbs/results/test_2.gif)

