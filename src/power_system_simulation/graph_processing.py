"""
This is a skeleton for the graph processing assignment.

We define a graph processor class with some function skeletons.
"""

from typing import List, Tuple

import networkx as nx
from networkx.exception import NetworkXNoCycle


class IDNotFoundError(Exception):
    """
    Raising IDNotFoundError exception
    """


class InputLengthDoesNotMatchError(Exception):
    """
    Raising InputLengthDoesNotMatchError exception
    """


class IDNotUniqueError(Exception):
    """
    Raising IDNotUniqueError exception
    """


class GraphNotFullyConnectedError(Exception):
    """
    Raising GraphNotFullyConnectedError exception
    """


class GraphCycleError(Exception):
    """
    Raising GraphCycleError exception
    """


class EdgeAlreadyDisabledError(Exception):
    """
    Raising EdgeAlreadyDisabledError exception
    """


class GraphProcessor:
    """
    General documentation of this class.
    You need to describe the purpose of this class and the functions in it.
    We are using an undirected graph in the processor.
    """

    def __init__(
        self,
        vertex_ids: List[int],
        edge_ids: List[int],
        edge_vertex_id_pairs: List[Tuple[int, int]],
        edge_enabled: List[bool],
        source_vertex_id: int,
    ) -> None:
        """
        Initialize a graph processor object with an undirected graph.
        Only the edges which are enabled are taken into account.
        Check if the input is valid and raise exceptions if not.
        The following conditions should be checked:
            1. vertex_ids and edge_ids should be unique. (IDNotUniqueError) -- done
            2. edge_vertex_id_pairs should have the same length as edge_ids. (InputLengthDoesNotMatchError) -- done
            3. edge_vertex_id_pairs should contain valid vertex ids. (IDNotFoundError) -- done
            4. edge_enabled should have the same length as edge_ids. (InputLengthDoesNotMatchError) -- done
            5. source_vertex_id should be a valid vertex id. (IDNotFoundError) -- done
            6. The graph should be fully connected. (GraphNotFullyConnectedError) -- done
            7. The graph should not contain cycles. (GraphCycleError) -- done
        If one certain condition is not satisfied, the error in the parentheses should be raised.

        Args:
            vertex_ids: list of vertex ids
            edge_ids: list of edge ids
            edge_vertex_id_pairs: list of tuples of two integer
                Each tuple is a vertex id pair of the edge.
            edge_enabled: list of bools indicating of an edge is enabled or not
            source_vertex_id: vertex id of the source in the graph
        """
        # put your implementation here

        self.graph = nx.Graph()
        self.graph.add_nodes_from(vertex_ids)
        self.graph.add_edges_from(
            [edge_vertex_id_pairs[i] for i in range(len(edge_vertex_id_pairs)) if edge_enabled[i] == 1]
        )
        for i, (u, v) in enumerate(self.graph.edges()):
            self.graph[u][v]["edge_id"] = edge_ids[i]
        self.graph.graph["source_vertex_id"] = source_vertex_id

        if len(vertex_ids) != len(set(vertex_ids)):
            raise IDNotUniqueError("vertex ids must be unique")

        if (len(edge_ids)) != len(set(edge_ids)):
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

        if nx.is_connected(self.graph) is False:
            raise GraphNotFullyConnectedError("graph should be fully connected")

        def has_cycle(self, sc):
            """
            Dealing with the output of nx.find_cycle() function
            """
            try:
                nx.find_cycle(self.graph, sc)
                return True
            except NetworkXNoCycle:
                return False

        if has_cycle(self, source_vertex_id) is True:
            raise GraphCycleError("graph should not have cycles")

    def find_downstream_vertices(self, edge_id: int) -> List[int]:
        """
        Given an edge id, return all the vertices which are in the downstream of the edge,
            with respect to the source vertex.
            Including the downstream vertex of the edge itself!

        Only enabled edges should be taken into account in the analysis.
        If the given edge_id is a disabled edge, it should return empty list.
        If the given edge_id does not exist, it should raise IDNotFoundError.


        For example, given the following graph (all edges enabled):

            vertex_0 (source) --edge_1-- vertex_2 --edge_3-- vertex_4

        Call find_downstream_vertices with edge_id=1 will return [2, 4]
        Call find_downstream_vertices with edge_id=3 will return [4]

        Args:
            edge_id: edge id to be searched

        Returns:
            A list of all downstream vertices.
        """
        # put your implementation here

    def find_alternative_edges(self, disabled_edge_id: int) -> List[int]:
        """
        Given an enabled edge, do the following analysis:
            If the edge is going to be disabled,
                which (currently disabled) edge can be enabled to ensure
                that the graph is again fully connected and acyclic?
            Return a list of all alternative edges.
        If the disabled_edge_id is not a valid edge id, it should raise IDNotFoundError.
        If the disabled_edge_id is already disabled, it should raise EdgeAlreadyDisabledError.
        If there are no alternative to make the graph fully connected again, it should return empty list.


        For example, given the following graph:

        vertex_0 (source) --edge_1(enabled)-- vertex_2 --edge_9(enabled)-- vertex_10
                 |                               |
                 |                           edge_7(disabled)
                 |                               |
                 -----------edge_3(enabled)-- vertex_4
                 |                               |
                 |                           edge_8(disabled)
                 |                               |
                 -----------edge_5(enabled)-- vertex_6

        Call find_alternative_edges with disabled_edge_id=1 will return [7]
        Call find_alternative_edges with disabled_edge_id=3 will return [7, 8]
        Call find_alternative_edges with disabled_edge_id=5 will return [8]
        Call find_alternative_edges with disabled_edge_id=9 will return []

        Args:
            disabled_edge_id: edge id (which is currently enabled) to be disabled

        Returns:
            A list of alternative edge ids.
        """
        # put your implementation here
