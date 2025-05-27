
import pytest
from find_alternative_edges import (
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
    return GraphProcessor(
        vertex_ids=[0, 1, 2, 3, 4],
        edge_ids=[10, 20, 30, 40, 50],
        edge_vertex_id_pairs=[(0,1), (1,2), (2,3), (0,4), (4,3)],
        edge_enabled=[True, True, True, True, True],
        source_vertex_id=0
    )
class TestGraphInitialization:
    def test_valid_initialization(self, simple_chain_graph):
        ...

    def test_duplicate_vertex_ids(self):
        ...

    def test_invalid_vertex_reference(self):
        ...

    def test_disconnected_graph(self):
        ...

    def test_nonexistent_source_vertex_id(self):
        with pytest.raises(IDNotFoundError):
            GraphProcessor(
                vertex_ids=[0, 1],
                edge_ids=[10],
                edge_vertex_id_pairs=[(0,1)],
                edge_enabled=[True],
                source_vertex_id=2  # Invalid source vertex
            )

    def test_duplicate_edge_ids(self):
        with pytest.raises(IDNotUniqueError):
            GraphProcessor(
                vertex_ids=[0, 1],
                edge_ids=[10, 10],
                edge_vertex_id_pairs=[(0,1), (1,0)],
                edge_enabled=[True, True],
                source_vertex_id=0
            )

    def test_mismatched_edge_ids_and_vertex_pairs(self):
        with pytest.raises(InputLengthDoesNotMatchError):
            GraphProcessor(
                vertex_ids=[0, 1],
                edge_ids=[10, 20],
                edge_vertex_id_pairs=[(0,1)],  # Only one pair
                edge_enabled=[True, True],
                source_vertex_id=0
            )

    def test_mismatched_edge_ids_and_edge_enabled(self):
        with pytest.raises(InputLengthDoesNotMatchError):
            GraphProcessor(
                vertex_ids=[0, 1],
                edge_ids=[10, 20],
                edge_vertex_id_pairs=[(0,1), (1,0)],
                edge_enabled=[True],  # Too short
                source_vertex_id=0
            )

# --------------------------------------------------
# Test Group 1: Graph Initialization and Validation
# --------------------------------------------------
class TestFindAlternativeEdgesCycleDetection:
    def test_candidate_edge_creates_cycle(self):
        """
        Ensure that candidate edges that create cycles are not considered alternatives.
        """
        gp = GraphProcessor(
            vertex_ids=[0, 1, 2],
            edge_ids=[10, 20, 30],
            edge_vertex_id_pairs=[(0,1), (1,2), (0,2)],
            edge_enabled=[True, True, False],  # edge 30 disabled, would create cycle if enabled
            source_vertex_id=0
        )
        # Disabling edge 10, 30 would close a cycle so shouldn't be an alternative
        alternatives = gp.find_alternative_edges(10)
        assert alternatives == []


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
            edge_enabled=[True, True, True, True],
            source_vertex_id=0
        )
        gp.edge_enabled[2] = False  # Disable edge 30
        gp.edge_enabled[3] = False
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
            edge_enabled=[True],
            source_vertex_id=0
        )
        gp.edge_enabled[0] = False  # Manually disable for test
        with pytest.raises(EdgeAlreadyDisabledError):
            gp.find_alternative_edges(10)
        with pytest.raises(EdgeAlreadyDisabledError):
            gp.find_alternative_edges(10)


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


        
