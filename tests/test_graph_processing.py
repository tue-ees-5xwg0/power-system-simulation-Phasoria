from power_system_simulation.graph_processing import GraphProcessor

vertex_ids = [1, 2, 3]
edge_ids = [1, 2, 3]
edge_vertex_id_pairs = [(1, 2), (2, 3), (1, 3)]
edge_enabled = [1, 0, 0]
source_vertex_id = 1

graph = GraphProcessor([1, 2, 3], [1, 2, 3], [(1, 2), (2, 3), (1, 3)], [1, 1, 0], 1)

print(graph.graph)