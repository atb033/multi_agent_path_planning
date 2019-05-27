# Multi-Agent path planning in python
 
# Table of contents
 * [Safe-Interval Path Planning (SIPP)](#safe-interval-path-planning) 
 * [Conflict-Based Search (CBS)](#conflict-based-search) 

# Safe-Interval Path Planning
## Execution

Please run the following commands to generate a plan. 

The dimensions of the map, obstacles, and initial and final positions of the agents must be mentioned in input.yaml. The output is generated and stored in output.yaml.

For SIPP single-agent planning with dynamic obstacles: 
```
cd ./sipp
python3 sipp.py input.yaml output.yaml
```

For SIPP multi-agent prioritized planning:
```
python3 multi_sipp.py input.yaml output.yaml
```

## Visualization of results
To visualize the generated results

```
python3 visualize_sipp.py input.yaml output.yaml 
```
To record video

```
python3 visualize_sipp.py input.yaml output.yaml --video 'sipp.avi' --speed 1
```

Success                                 | Failure
:-------------------------------------:|:-------------------------:
![Success](./sipp/results/success.gif) |![Failure](./sipp/results/failure.gif)

# Conflict Based Search


