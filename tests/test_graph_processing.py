# tests/test_graph_processing.py
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
# Test 1: Valid Graph Initialization
# --------------------------------------------------
def test_valid_graph_initialization():
    """Test successful graph creation with valid inputs"""
    processor = GraphProcessor(
        vertex_ids=[0, 1, 2],
        edge_ids=[10, 20],
        edge_vertex_id_pairs=[(0,1), (1,2)],
        edge_enabled=[True, True],
        source_vertex_id=0
    )
    assert processor.G.number_of_edges() == 2

# --------------------------------------------------
# Test 2: Input Validation
# --------------------------------------------------
def test_invalid_input_lengths():
    """Test mismatched input lengths"""
    with pytest.raises(InputLengthDoesNotMatchError):
        GraphProcessor(
            vertex_ids=[0, 1],
            edge_ids=[10],
            edge_vertex_id_pairs=[(0,1), (1,2)],  # Extra pair
            edge_enabled=[True],
            source_vertex_id=0
        )

def test_duplicate_vertex_ids():
    """Test duplicate vertex IDs"""
    with pytest.raises(IDNotUniqueError):
        GraphProcessor(
            vertex_ids=[0, 0],  # Duplicate
            edge_ids=[10],
            edge_vertex_id_pairs=[(0,1)],
            edge_enabled=[True],
            source_vertex_id=0
        )

# --------------------------------------------------
# Test 4: find_alternative_edges
# --------------------------------------------------
def test_find_alternative_edges_with_backup():
    """Test finding alternative paths"""
    processor = GraphProcessor(
        vertex_ids=[0, 1, 2],
        edge_ids=[10, 20, 30],
        edge_vertex_id_pairs=[(0,1), (1,2), (0,2)],
        edge_enabled=[True, True, False],  # 30 is disabled backup
        source_vertex_id=0
    )
    assert processor.find_alternative_edges(10) == [30]  # 0-2 can replace 0-1-2

def test_find_alternative_edges_already_disabled():
    """Test error when edge is already disabled"""
    processor = GraphProcessor(
        vertex_ids=[0, 1],
        edge_ids=[10],
        edge_vertex_id_pairs=[(0,1)],
        edge_enabled=[False],  # Already disabled
        source_vertex_id=0
    )
    with pytest.raises(EdgeAlreadyDisabledError):
        processor.find_alternative_edges(10)

# --------------------------------------------------
# Test 5: Edge Cases
# --------------------------------------------------
def test_empty_graph():
    """Test empty graph creation fails"""
    with pytest.raises(GraphNotFullyConnectedError):
        GraphProcessor(
            vertex_ids=[],
            edge_ids=[],
            edge_vertex_id_pairs=[],
            edge_enabled=[],
            source_vertex_id=0
        )

def test_cyclic_graph():
    """Test cycle detection"""
    with pytest.raises(GraphCycleError):
        GraphProcessor(
            vertex_ids=[0, 1, 2],
            edge_ids=[10, 20, 30],
            edge_vertex_id_pairs=[(0,1), (1,2), (2,0)],  # Triangle
            edge_enabled=[True, True, True],
            source_vertex_id=0
        )