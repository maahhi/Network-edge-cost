this repository simulate a network and calculate the cost of each link/edge to failure.
here is an implementation of decremental dijkestra.
first we will calculcate the shortest path from each node to others. then by keeping track of the shortest path tree, we can update the cost of each edge in the network.

to try the code simply run dijkstra.py with python3. 

-- Networkx shortest path functions works faster specially on bigger files and easier interface for graph handling but I found wrong answers on [shortest_path function](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.generic.shortest_path.html#networkx.algorithms.shortest_paths.generic.shortest_path)

-- bigger files used for testing: roadNet-CA from stanford SNAP data and bitcoinalpha.txt from [this repository](https://github.com/NDS-VU/signed-network-datasets)
