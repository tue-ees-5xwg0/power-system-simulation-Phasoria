import unittest
import sys
import os

# Add parent directory to path to allow importing Assignment_1
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from power_system_simulation.Assignment_1 import (
    GraphProcessor,
    IDNotFoundError,
    InputLengthDoesNotMatchError,
    IDNotUniqueError,
    GraphNotFullyConnectedError,
    GraphCycleError
)

class TestGraphProcessor(unittest.TestCase):
    """Test suite for the GraphProcessor class."""

    def setUp(self):
        """Set up test fixtures."""
        self.vertex_ids = [1, 2, 3, 4, 5]
        self.edge_ids = [10, 11, 12, 13]
        self.edge_vertex_id_pairs = [(1, 2), (2, 3), (3, 4), (3, 5)]
        self.edge_enabled = [True, True, True, True]
        self.source_vertex_id = 1

        self.processor = GraphProcessor(
            vertex_ids=self.vertex_ids,
            edge_ids=self.edge_ids,
            edge_vertex_id_pairs=self.edge_vertex_id_pairs,
            edge_enabled=self.edge_enabled,
            source_vertex_id=self.source_vertex_id,
        )

    def test_valid_construction(self):
        """Test that GraphProcessor is correctly instantiated."""
        self.assertIsInstance(self.processor, GraphProcessor)

    def test_invalid_edge_length(self):
        """Test that InputLengthDoesNotMatchError is raised for mismatched edge lengths."""
        with self.assertRaises(InputLengthDoesNotMatchError):
            GraphProcessor(
                self.vertex_ids,
                self.edge_ids,
                self.edge_vertex_id_pairs,
                [True, False],  # Incorrect length
                self.source_vertex_id
            )

    def test_duplicate_vertex_ids(self):
        """Test that IDNotUniqueError is raised for duplicate vertex IDs."""
        with self.assertRaises(IDNotUniqueError):
            GraphProcessor(
                [1, 1, 2],  # Duplicate vertex IDs
                [10],
                [(1, 2)],
                [True],
                1
            )

    def test_missing_vertex_in_edge(self):
        """Test that IDNotFoundError is raised for edges referencing non-existent vertices."""
        with self.assertRaises(IDNotFoundError):
            GraphProcessor(
                [1, 2],  # Vertex 3 does not exist
                [10],
                [(1, 3)],  # Invalid edge
                [True],
                1
            )

    def test_graph_not_connected(self):
        """Test that GraphNotFullyConnectedError is raised for disconnected graphs."""
        with self.assertRaises(GraphNotFullyConnectedError):
            GraphProcessor(
                [1, 2, 3],
                [10],
                [(1, 2)],  # No path to vertex 3
                [True],
                1
            )

    def test_cycle_detection(self):
        """Test that GraphCycleError is raised for cyclic graphs."""
        edge_pairs_with_cycle = [(1, 2), (2, 3), (3, 1), (3, 4)]  # Cycle: 1 → 2 → 3 → 1
        with self.assertRaises(GraphCycleError):
            GraphProcessor(
                [1, 2, 3, 4],
                [10, 11, 12, 13],
                edge_pairs_with_cycle,
                [True, True, True, True],
                1
            )

    def test_find_downstream_vertices(self):
        """Test that downstream vertices are correctly identified for a given edge."""
        # Edge 12: (3, 4), downstream vertex is 4
        result = self.processor.find_downstream_vertices(12)
        self.assertEqual(result, [4])

    def test_multiple_downstream_paths(self):
        """Test graph with multiple paths from source (without creating cycles)"""
        processor = GraphProcessor(
            vertex_ids=[1, 2, 3, 4, 5],
            edge_ids=[10, 11, 12, 13],
            edge_vertex_id_pairs=[(1, 2), (1, 3), (2, 4), (3, 5)],  # Tree structure
            edge_enabled=[True, True, True, True],
            source_vertex_id=1
        )
        # Edge 10: (1,2) → downstream is 2
        self.assertEqual(processor.find_downstream_vertices(10), [2])
        # Edge 11: (1,3) → downstream is 3
        self.assertEqual(processor.find_downstream_vertices(11), [3])
        # Edge 12: (2,4) → downstream is 4
        self.assertEqual(processor.find_downstream_vertices(12), [4])
        # Edge 13: (3,5) → downstream is 5
        self.assertEqual(processor.find_downstream_vertices(13), [5])

    def test_partially_disabled_graph(self):
        """Test graph where disabled edges don't break connectivity"""
        processor = GraphProcessor(
            vertex_ids=[1, 2, 3, 4],
            edge_ids=[10, 11, 12, 13],
            edge_vertex_id_pairs=[(1, 2), (2, 3), (3, 4), (1, 4)],  # Alternative path
            edge_enabled=[True, True, False, True],  # Disable (3,4) but keep (1,4)
            source_vertex_id=1
        )
        # Graph should remain valid
        self.assertIsInstance(processor, GraphProcessor)
        # Disabled edge should return empty
        self.assertEqual(processor.find_downstream_vertices(12), [])
        # Enabled edges should work normally
        self.assertEqual(processor.find_downstream_vertices(10), [2])
        self.assertEqual(processor.find_downstream_vertices(13), [4])  # Test alternative path

    def test_edge_not_found(self):
        """Test that IDNotFoundError is raised for non-existent edges."""
        with self.assertRaises(IDNotFoundError):
            self.processor.find_downstream_vertices(99)  # Invalid edge ID

    def test_empty_graph(self):
        """Test behavior with an empty graph."""
        with self.assertRaises(InputLengthDoesNotMatchError):
            GraphProcessor(
                vertex_ids=[],
                edge_ids=[],
                edge_vertex_id_pairs=[],
                edge_enabled=[],
                source_vertex_id=None
            )

    def test_single_vertex_graph(self):
        """Test behavior with a single vertex and no edges."""
        processor = GraphProcessor(
            vertex_ids=[1],
            edge_ids=[],
            edge_vertex_id_pairs=[],
            edge_enabled=[],
            source_vertex_id=1
        )
        with self.assertRaises(IDNotFoundError):
            processor.find_downstream_vertices(10)  # No edges exist

if __name__ == "__main__":
    unittest.main()
