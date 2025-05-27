import copy
import networkx as nx
from typing import List, Tuple

class IDNotFoundError(Exception):
    pass

class InputLengthDoesNotMatchError(Exception):
    pass

class IDNotUniqueError(Exception):
    pass

class GraphNotFullyConnectedError(Exception):
    pass

class GraphCycleError(Exception):
    pass

class EdgeAlreadyDisabledError(Exception):
    pass


class GraphProcessor:
  

    def __init__(
        self,
        vertex_ids: List[int],
        edge_ids: List[int],
        edge_vertex_id_pairs: List[Tuple[int, int]],
        edge_enabled: List[bool],
        source_vertex_id: int,
    ) -> None:
        

        self.vertex_ids = vertex_ids
        self.edge_ids = edge_ids
        self.edge_vertex_id_pairs = edge_vertex_id_pairs
        self.edge_enabled = edge_enabled
        self.source_vertex_id = source_vertex_id

        self.graph = nx.Graph()
        self.graph.add_nodes_from(vertex_ids)
        self.graph.add_edges_from(
            [edge_vertex_id_pairs[i] for i in range(len(edge_vertex_id_pairs)) if edge_enabled[i] == 1]
        )
        for i, (u, v) in enumerate(edge_vertex_id_pairs):
            if edge_enabled[i]:
                self.graph[u][v]["edge_id"] = edge_ids[i]

        self.graph.graph["source_vertex_id"] = source_vertex_id

        if len(vertex_ids) != len(set(vertex_ids)):
            raise IDNotUniqueError("vertex ids must be unique")

        if len(edge_ids) != len(set(edge_ids)):
            raise IDNotUniqueError("edge ids must be unique")

        if len(edge_vertex_id_pairs) != len(edge_ids):
            raise InputLengthDoesNotMatchError("edge_vertex_id_pairs should have the same length as edge_ids")

        for i, j in edge_vertex_id_pairs:
            if i not in vertex_ids or j not in vertex_ids:
                raise IDNotFoundError("edge_vertex_id_pairs should contain valid vertex ids")

        if len(edge_enabled) != len(edge_ids):
            raise InputLengthDoesNotMatchError("edge_enabled should have the same length as edge_ids")

        if source_vertex_id not in vertex_ids:
            raise IDNotFoundError("source_vertex_id should be a valid vertex id")
        if len(vertex_ids) == 1:
            raise GraphNotFullyConnectedError("graph with single node is not considered connected")

        if nx.is_connected(self.graph) is False:
            raise GraphNotFullyConnectedError("graph should be fully connected")

        def has_cycle(self, sc):
            """
            Dealing with the output of nx.find_cycle() function
            """
            try:
                nx.find_cycle(self.graph, sc)
                return True
            except nx.NetworkXNoCycle:
                return False

        if has_cycle(self, source_vertex_id) is True:
            raise GraphCycleError("graph should not have cycles")

    def find_alternative_edges(self, disabled_edge_id: int) -> List[int]:

        # Get a list of all edges that are currently disabled
        originally_disabled_edges = [self.edge_ids[i] for i, enabled in enumerate(self.edge_enabled) if not enabled]

        # Check if the given edge ID exists
        if disabled_edge_id not in self.edge_ids:
            raise IDNotFoundError(f"Edge id {disabled_edge_id} not found")

        # Check if the given edge is already disabled
        if disabled_edge_id in originally_disabled_edges:
            raise EdgeAlreadyDisabledError(f"Edge id {disabled_edge_id} is already disabled")

        # Prepare a list to hold alternative edges
        alt_list = []

        # Create a copy of the disabled edges list and add the edge we want to disable
        updated_disabled_edges = copy.copy(originally_disabled_edges)
        updated_disabled_edges.append(disabled_edge_id)

        # Pair each edge with its vertex pair, current enabled/disabled status, and edge ID
        full_edge_list = list(zip(self.edge_vertex_id_pairs, self.edge_enabled, self.edge_ids))

        # Update the edge list to mark the edge to be disabled as disabled
        updated_full_edge_list = [
            (vertex_pair, False if edge_id == disabled_edge_id else enabled, edge_id)
            for vertex_pair, enabled, edge_id in full_edge_list
        ]

        # Iterate over each originally disabled edge to test enabling it temporarily
        for candidate_edge_id in originally_disabled_edges:
            # Temporarily enable the candidate edge while keeping others' statuses updated
            temp_edge_list = [
                (vertex_pair,
                 True if edge_id == candidate_edge_id else enabled,
                 edge_id)
                for vertex_pair, enabled, edge_id in updated_full_edge_list
            ]

            # Build a temporary graph with updated edge statuses
            temp_graph = nx.Graph()
            temp_graph.add_nodes_from(self.vertex_ids)
            for vertex_pair, enabled, edge_id in temp_edge_list:
                if enabled:
                    temp_graph.add_edge(*vertex_pair, id=edge_id)

            # Check if the temporary graph is fully connected
            connected = nx.is_connected(temp_graph)

            # Check if the temporary graph contains cycles
            try:
                nx.find_cycle(temp_graph)
                has_cycle = True
            except nx.NetworkXNoCycle:
                has_cycle = False

            # If graph is connected and acyclic, add candidate edge to alternatives
            if connected and not has_cycle:
                alt_list.append(candidate_edge_id)

        # Return the list of alternative edges
        return alt_list
