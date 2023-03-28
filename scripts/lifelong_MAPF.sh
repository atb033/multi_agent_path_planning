cd multi_agent_path_planning/lifelong_MAPF
rm dataproducts/output.yaml -f
python3 lifelong_MAPF.py dataproducts/input.yaml dataproducts/output.yaml && python3 visualize_lifelong.py dataproducts/input.yaml dataproducts/output.yaml