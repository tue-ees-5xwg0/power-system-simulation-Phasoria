"""
This is a skeleton for the graph processing assignment.

We define a graph processor class with some function skeletons.
"""
#networkx is a package I added (recommened in course github)
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
            1. vertex_ids and edge_ids should be unique. (IDNotUniqueError)
            2. edge_vertex_id_pairs should have the same length as edge_ids. (InputLengthDoesNotMatchError)
            3. edge_vertex_id_pairs should contain valid vertex ids. (IDNotFoundError)
            4. edge_enabled should have the same length as edge_ids. (InputLengthDoesNotMatchError)
            5. source_vertex_id should be a valid vertex id. (IDNotFoundError)
            6. The graph should be fully connected. (GraphNotFullyConnectedError)
            7. The graph should not contain cycles. (GraphCycleError)
        If one certain condition is not satisfied, the error in the parentheses should be raised.

        Args:
            vertex_ids: list of vertex ids
            edge_ids: liest of edge ids
            edge_vertex_id_pairs: list of tuples of two integer
                Each tuple is a vertex id pair of the edge.
            edge_enabled: list of bools indicating of an edge is enabled or not
            source_vertex_id: vertex id of the source in the graph
        """
        # put your implementation here

        #Checking if the graph is empty
        if not vertex_ids:
            raise GraphNotFullyConnectedError("Graph cannot be empty")


        #Here we are validating the input lengths


        if len(edge_vertex_id_pairs) != len(edge_ids):
            raise InputLengthDoesNotMatchError("edge_vertex_id_pairs and edge_ids must have the same length")
        if len(edge_enabled) != len(edge_ids):
            raise InputLengthDoesNotMatchError("edge_enabled and edge_ids must have the same length")
       
        #Here we are validating the uniqueness


        if len(vertex_ids) != len(set(vertex_ids)):
            raise IDNotUniqueError("vertex_ids must be unique")
        if len(edge_ids) != len(set(edge_ids)):
            raise IDNotUniqueError("edge_ids must be unique")
       
       
        #Here we are validating that the vertex IDs actually exist


        vertex_set = set(vertex_ids)
        for u, v in edge_vertex_id_pairs:
            if u not in vertex_set or v not in vertex_set:
                raise IDNotFoundError(f"Vertex ID {(u if u not in vertex_set else v)} not found")
           
           
        #Here we are validating that the sources actually exist


        if source_vertex_id not in vertex_set:
            raise IDNotFoundError(f"Source vertex {source_vertex_id} not found")
       


       


        self.vertex_ids = vertex_ids
        self.edge_ids =edge_ids
        self.edge_vertex_id_pairs = edge_vertex_id_pairs
        self.edge_enabled = edge_enabled
        self.source_vertex_id = source_vertex_id


    #this buildy the graph only using edges that are enabled


        self.G = nx.Graph()
        for edge_id, (u, v), enabled in zip(edge_ids, edge_vertex_id_pairs, edge_enabled):
            if enabled:
                self.G.add_edge(u, v, id=edge_id)


   


        if nx.number_of_edges(self.G) == 0:
            if len(vertex_ids) > 1:
                raise GraphNotFullyConnectedError("Graph isn't fully connected")
    # For single vertex, skip further checks
        else:
            if not nx.is_connected(self.G):
                raise GraphNotFullyConnectedError("Graph isn't fully connected")
            if not nx.is_tree(self.G):
                raise GraphCycleError("Graph has cycles")

        

    


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
        pass

    def find_alternative_edges(self, disabled_edge_id: int) -> List[int]:
    
        #Here I check that if edges are invalid or disabled. If they are it raises an error
        if disabled_edge_id not in self.edge_ids:
            raise IDNotFoundError(f"Edge {disabled_edge_id} not found")
        if not self.edge_enabled[self.edge_ids.index(disabled_edge_id)]:
            raise EdgeAlreadyDisabledError(f"Edge {disabled_edge_id} already disabled")
        

        u, v = self.edge_vertex_id_pairs[self.edge_ids.index(disabled_edge_id)]


        #Now I made a temp graph after edge is removed. I then split the graphs into comp_A and comp_B
        temp_G = self.G.copy()
        temp_G.remove_edge(u, v)

        component_A = nx.node_connected_component(temp_G, u)
        component_B = nx.node_connected_component(temp_G, v)

        #I check the disabled cables
        alternatives = []
        for i, (x, y) in zip(self.edge_ids, self.edge_vertex_id_pairs):
            if not self.edge_enabled[self.edge_ids.index(i)] and i != disabled_edge_id: 
                if(x in component_A and y in component_B) or(x in component_A and y in component_B):
                    temp_G.add_edge(x, y)
                    if nx.is_tree(temp_G):
                        alternatives.append(i)
                    temp_G.remove_edge(x, y)

        return sorted(alternatives)


        