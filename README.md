# Multi-Agent path planning in python
 
 ## Methods implemented:
 * Safe-Interval Path Planning (DOI: 10.1109/ICRA.2011.5980306)

## Run test

Please run the following commands to generate a plan. 

The dimensions of the map, obstacles, and initial and final positions of the agents must be mentioned in input.yaml. The output is generated and stored in output.yaml.

SIPP single-agent planning with dynamic obstacles
```
cd ./sipp
python3 sipp.py input.yaml output.yaml
```

SIPP multi-agent prioritized planning 
```
python3 multi_sipp.py input.yaml output.yaml
```

## Visualization of results
To visualize the generated results

```
 python3 visualize_sipp.py input.yaml output.yaml 
```