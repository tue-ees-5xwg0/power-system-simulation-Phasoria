import pytest
from src.power_system_simulation.graph_processing import (
    GraphProcessor,
    IDNotFoundError,
    InputLengthDoesNotMatchError,
    IDNotUniqueError,
    GraphNotFullyConnectedError,
    GraphCycleError,
    EdgeAlreadyDisabledError
)

# --------------------------------------------------
# Fixtures for common test graphs
# --------------------------------------------------
@pytest.fixture
def simple_chain_graph():
    """0--10--1--20--2"""
    return GraphProcessor(
        vertex_ids=[0, 1, 2],
        edge_ids=[10, 20],
        edge_vertex_id_pairs=[(0,1), (1,2)],
        edge_enabled=[True, True],
        source_vertex_id=0
    )

@pytest.fixture
def graph_with_backup_edge():
    """0--10--1--20--2 with backup edge 30 (0--2) disabled"""
    return GraphProcessor(
        vertex_ids=[0, 1, 2],
        edge_ids=[10, 20, 30],
        edge_vertex_id_pairs=[(0,1), (1,2), (0,2)],
        edge_enabled=[True, True, False],
        source_vertex_id=0
    )

@pytest.fixture
def complex_graph():
    """0--10--1--20--2--30--3
       \              /
        \--40--4--50-"""
    return GraphProcessor(
        vertex_ids=[0, 1, 2, 3, 4],
        edge_ids=[10, 20, 30, 40, 50],
        edge_vertex_id_pairs=[(0,1), (1,2), (2,3), (0,4), (4,3)],
        edge_enabled=[True, True, True, True, True],
        source_vertex_id=0
    )

# --------------------------------------------------
# Test Group 1: Graph Initialization and Validation
# --------------------------------------------------
class TestGraphInitialization:
    def test_valid_initialization(self, simple_chain_graph):
        assert simple_chain_graph.graph.number_of_nodes() == 3
        assert simple_chain_graph.graph.number_of_edges() == 2

    def test_duplicate_vertex_ids(self):
        with pytest.raises(IDNotUniqueError):
            GraphProcessor(
                vertex_ids=[0, 0],
                edge_ids=[10],
                edge_vertex_id_pairs=[(0,1)],
                edge_enabled=[True],
                source_vertex_id=0
            )

    def test_invalid_vertex_reference(self):
        with pytest.raises(IDNotFoundError):
            GraphProcessor(
                vertex_ids=[0, 1],
                edge_ids=[10],
                edge_vertex_id_pairs=[(0,2)],  # Vertex 2 doesn't exist
                edge_enabled=[True],
                source_vertex_id=0
            )

    def test_disconnected_graph(self):
        with pytest.raises(GraphNotFullyConnectedError):
            GraphProcessor(
                vertex_ids=[0, 1, 2],
                edge_ids=[10, 20],
                edge_vertex_id_pairs=[(0,1), (2,2)],  # Disconnected
                edge_enabled=[True, True],
                source_vertex_id=0
            )

# --------------------------------------------------
# Test Group 2: find_alternative_edges()
# --------------------------------------------------
class TestFindAlternativeEdges:
    def test_single_backup_edge(self, graph_with_backup_edge):
        alternatives = graph_with_backup_edge.find_alternative_edges(10)
        assert alternatives == [30]

    def test_no_alternatives(self, simple_chain_graph):
        assert simple_chain_graph.find_alternative_edges(10) == []

    def test_multiple_alternatives(self):
        gp = GraphProcessor(
            vertex_ids=[0, 1, 2, 3],
            edge_ids=[10, 20, 30, 40],
            edge_vertex_id_pairs=[(0,1), (1,2), (0,3), (3,2)],
            edge_enabled=[True, True, False, False],
            source_vertex_id=0
        )
        alternatives = gp.find_alternative_edges(10)
        assert sorted(alternatives) == [30, 40]

    def test_invalid_edge_id(self, simple_chain_graph):
        with pytest.raises(IDNotFoundError):
            simple_chain_graph.find_alternative_edges(99)

    def test_already_disabled_edge(self):
        gp = GraphProcessor(
            vertex_ids=[0, 1],
            edge_ids=[10],
            edge_vertex_id_pairs=[(0,1)],
            edge_enabled=[False],
            source_vertex_id=0
        )
        with pytest.raises(EdgeAlreadyDisabledError):
            gp.find_alternative_edges(10)

# --------------------------------------------------
# Test Group 3: find_downstream_vertices()
# --------------------------------------------------
class TestFindDownstreamVertices:
    def test_linear_graph(self, simple_chain_graph):
        assert simple_chain_graph.find_downstream_vertices(10) == [1, 2]
        assert simple_chain_graph.find_downstream_vertices(20) == [2]

    def test_branched_graph(self, complex_graph):
        assert sorted(complex_graph.find_downstream_vertices(10)) == [1, 2, 3]
        assert sorted(complex_graph.find_downstream_vertices(40)) == [3, 4]

    def test_disabled_edge(self):
        gp = GraphProcessor(
            vertex_ids=[0, 1],
            edge_ids=[10, 20],
            edge_vertex_id_pairs=[(0,1), (0,1)],
            edge_enabled=[True, False],
            source_vertex_id=0
        )
        assert gp.find_downstream_vertices(20) == []

    def test_invalid_edge_id(self, simple_chain_graph):
        with pytest.raises(IDNotFoundError):
            simple_chain_graph.find_downstream_vertices(99)

# --------------------------------------------------
# Test Group 4: Edge Cases
# --------------------------------------------------
class TestEdgeCases:
    def test_single_node_graph(self):
        with pytest.raises(GraphNotFullyConnectedError):
            GraphProcessor(
                vertex_ids=[0],
                edge_ids=[],
                edge_vertex_id_pairs=[],
                edge_enabled=[],
                source_vertex_id=0
            )

    def test_cyclic_graph(self):
        with pytest.raises(GraphCycleError):
            GraphProcessor(
                vertex_ids=[0, 1, 2],
                edge_ids=[10, 20, 30],
                edge_vertex_id_pairs=[(0,1), (1,2), (2,0)],
                edge_enabled=[True, True, True],
                source_vertex_id=0
            )

    def test_multiple_disabled_edges(self):
        gp = GraphProcessor(
            vertex_ids=[0, 1, 2, 3],
            edge_ids=[10, 20, 30, 40],
            edge_vertex_id_pairs=[(0,1), (1,2), (0,3), (3,2)],
            edge_enabled=[True, True, False, False],
            source_vertex_id=0
        )
        assert sorted(gp.find_alternative_edges(10)) == [30, 40]
        assert sorted(gp.find_alternative_edges(20)) == [30, 40]