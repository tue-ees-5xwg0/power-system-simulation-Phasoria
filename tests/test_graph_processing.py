"""
Test file
"""

import pytest

from power_system_simulation.graph_processing import (
    GraphCycleError,
    GraphNotFullyConnectedError,
    GraphProcessor,
    IDNotFoundError,
    IDNotUniqueError,
    InputLengthDoesNotMatchError,
)


class Tests:
    """
    Testing the raise exception in case of faulty graph
    """

    def test_id_not_unique_error_1(self):
        """
        Testing vertex_ids should be unique
        """
        vertex_ids = [1, 2, 3, 4, 4]
        edge_ids = [1, 2, 3, 4]
        edge_vertex_id_pairs = [(1, 2), (2, 3), (3, 4), (1, 3)]
        edge_enabled = [1, 1, 1, 0]
        source_vertex_id = 1
        with pytest.raises(IDNotUniqueError):
            GraphProcessor(vertex_ids, edge_ids, edge_vertex_id_pairs, edge_enabled, source_vertex_id)

    def test_id_not_unique_error_2(self):
        """
        Testing edge_ids should be unique
        """
        vertex_ids = [1, 2, 3, 4]
        edge_ids = [1, 2, 3, 3]
        edge_vertex_id_pairs = [(1, 2), (2, 3), (1, 3), (1, 4)]
        edge_enabled = [1, 1, 1, 1]
        source_vertex_id = 1
        with pytest.raises(IDNotUniqueError):
            GraphProcessor(vertex_ids, edge_ids, edge_vertex_id_pairs, edge_enabled, source_vertex_id)

    def test_input_length_does_not_match_error_1(self):
        """
        Testing edge_vertex_id_pairs should have the same length as edge_ids
        """
        vertex_ids = [1, 2, 3]
        edge_ids = [1, 2, 3]
        edge_vertex_id_pairs = [(1, 2), (2, 3)]
        edge_enabled = [1, 0, 0]
        source_vertex_id = 1
        with pytest.raises(InputLengthDoesNotMatchError):
            GraphProcessor(vertex_ids, edge_ids, edge_vertex_id_pairs, edge_enabled, source_vertex_id)

    def test_id_not_found_error_1(self):
        """
        Testing edge_vertex_id_pairs should contain valid vertex ids
        """
        vertex_ids = [1, 2, 3]
        edge_ids = [1, 2, 3]
        edge_vertex_id_pairs = [(1, 2), (2, 3), (1, 4)]
        edge_enabled = [1, 0, 0]
        source_vertex_id = 1
        with pytest.raises(IDNotFoundError):
            GraphProcessor(vertex_ids, edge_ids, edge_vertex_id_pairs, edge_enabled, source_vertex_id)

    def test_input_length_does_not_match_error_2(self):
        """
        Testing edge_enabled should have the same length as edge_ids
        """
        vertex_ids = [1, 2, 3]
        edge_ids = [1, 2, 3, 4]
        edge_vertex_id_pairs = [(1, 2), (2, 3), (1, 3)]
        edge_enabled = [1, 1, 0]
        source_vertex_id = 1
        with pytest.raises(InputLengthDoesNotMatchError):
            GraphProcessor(vertex_ids, edge_ids, edge_vertex_id_pairs, edge_enabled, source_vertex_id)

    def test_id_not_found_error_2(self):
        """
        Testing source_vertex_id should be a valid vertex id
        """
        vertex_ids = [1, 2, 3]
        edge_ids = [1, 2, 3]
        edge_vertex_id_pairs = [(1, 2), (2, 3), (1, 3)]
        edge_enabled = [1, 1, 0]
        source_vertex_id = 4
        with pytest.raises(IDNotFoundError):
            GraphProcessor(vertex_ids, edge_ids, edge_vertex_id_pairs, edge_enabled, source_vertex_id)

    def test_graph_not_fully_connected_error(self):
        """
        Testing graph should be fully connected
        """
        vertex_ids = [1, 2, 3, 4]
        edge_ids = [1, 2, 3, 4]
        edge_vertex_id_pairs = [(1, 2), (2, 3), (4, 4), (3, 3)]
        edge_enabled = [1, 1, 1, 0]
        source_vertex_id = 1
        with pytest.raises(GraphNotFullyConnectedError):
            GraphProcessor(vertex_ids, edge_ids, edge_vertex_id_pairs, edge_enabled, source_vertex_id)

    def test_graph_cycle_error(self):
        """
        Testing graph should not contain cycles
        """
        vertex_ids = [1, 2, 3]
        edge_ids = [1, 2, 3]
        edge_vertex_id_pairs = [(1, 2), (2, 3), (1, 3)]
        edge_enabled = [1, 1, 1]
        source_vertex_id = 1
        with pytest.raises(GraphCycleError):
            GraphProcessor(vertex_ids, edge_ids, edge_vertex_id_pairs, edge_enabled, source_vertex_id)
