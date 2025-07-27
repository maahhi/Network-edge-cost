import heapq
import loadgraph as lg
import networkx as nx

def dijkstra(graph, start):
    # graph: adjacency list {node: [(neighbor, weight), ...]}
    # start: starting node

    # Step 1: Initialize distances and parent map
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    parents = {node: None for node in graph}  # for path reconstruction

    # Step 2: Priority queue (min-heap) to pick smallest distance node
    pq = [(0, start)]  # (distance, node)

    while pq:
        current_dist, current_node = heapq.heappop(pq)

        # Skip if we already found a better path
        if current_dist > distances[current_node]:
            continue

        # Step 3: Check neighbors
        for neighbor, weight in graph[current_node]:
            distance = current_dist + weight

            # If a shorter path to neighbor is found
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                parents[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))

    return distances, parents


def reconstruct_path(parents, start, end):
    # Build path from end to start using parent pointers
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = parents[current]
    path.reverse()

    # If start is not in path, no valid path exists
    if path[0] != start:
        return None
    return path


def dijkstra_edge_participation(dijkstra_edge_participants,adjacency_list):

    baseline_dijkstra = {}
    for node in adjacency_list:
        distances,parents = dijkstra(adjacency_list, start=node) # run dijkestra for each node - baseline
        baseline_dijkstra[node] = {"distances":distances, "parents":parents}
        print("Distances:", distances, "Parents:", parents)
        for node2 in adjacency_list:
            path = reconstruct_path(parents, start=node, end=node2)
            print("Reconstructed path from node", node, "to node ",node2,":", path)
            if len(path) > 1:
                for i in range(len(path)-1):
                    if node not in dijkstra_edge_participants[(path[i], path[i+1])]:
                        dijkstra_edge_participants[(path[i], path[i+1])].append(node)
    print("Dijkstra edge participation:", dijkstra_edge_participants)
    return baseline_dijkstra, dijkstra_edge_participants

def remove_edge(adjacency_list,edge_to_remove):
    # make a copy of the adjacency list
    new_adjacency_list = {node: neighbors.copy() for node, neighbors in adjacency_list.items()}
    u , v = edge_to_remove
    for pair in new_adjacency_list[u]:
        vp, weight = pair
        if vp == v:
            new_adjacency_list[u].remove(pair)
    return new_adjacency_list


if __name__ == "__main__":

    file = "bitcoinalpha.txt"
    file = "sample_graph_bid.txt"
    # Load edges from file
    edges = lg.load_edges(file)
    dijkstra_edge_participants = {(u, v): [] for u, v, _ in edges}  # ignore weights for adjacency list
    removing_edge_cost = {(u, v): 0 for u, v, _ in edges}
    adjacency_list = lg.build_adjacency_list(edges, directed=True)

    baseline_dijkstra, dijkstra_edge_participants = dijkstra_edge_participation(dijkstra_edge_participants,adjacency_list)
    for edge in dijkstra_edge_participants:
        new_adjacency_list = remove_edge(adjacency_list, edge)
        print("Removing edge:", edge)
        for i,node in enumerate(new_adjacency_list):
            if node not in dijkstra_edge_participants[edge]:
                continue
            distances, parents = dijkstra(new_adjacency_list, start=node)
            # cost of removing this edge
            dif =  sum(distances.values()) - sum(baseline_dijkstra[node]["distances"].values())
            removing_edge_cost[edge] += dif
            print("cost of removing edge", edge, "for shortest paths from node", node, "is", dif)


    print(removing_edge_cost)




    """
    file = "bitcoinalpha.txt"  # start from 1
    file = "sample_graph_bid.txt"
    G = lg.load_graph_nx(file)
    for v in G.nodes():
        path = nx.single_source_shortest_path(G, v)
        print("Shortest paths from node ",v,":", path)

    G = lg.load_graph_nx(file)
    p = nx.shortest_path(G)
    print("Shortest paths ", p)

    cycle = nx.find_cycle(G, orientation="original")
    print("cycle",cycle)

    file = "sample_graph_bid.txt"
    edges = lg.load_edges(file)
    adjacency_list = lg.build_adjacency_list(edges, directed=True)
    for node in adjacency_list:
        print(f"Node {node}: {adjacency_list[node]}")
        distances,parents = dijkstra(adjacency_list, start=node)
        print("Distances:", distances, "Parents:", parents)
        for node2 in adjacency_list:
            print("Reconstructed path from node", node, "to node ",node2,":", reconstruct_path(parents, start=node, end=node2))
    """