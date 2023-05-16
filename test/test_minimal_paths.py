import unittest
import random

from simulation.model import CommunicationNetwork
from simulation.minimal_paths import single_source_dijkstra_vertices, single_source_dijkstra_hyperedges, DistanceType

from simulation.minimal_paths import TimeVaryingHypergraph

class MinimalPath(unittest.TestCase):
    cn = CommunicationNetwork({'h1': ['v1', 'v2'], 'h2': ['v2', 'v3'], 'h3': ['v3', 'v4']}, {'h1': 1, 'h2': 2, 'h3': 3})

    def test_known_path(self):
        """
        Tests if shortest path is eqivelent to a specific dictionary:
        {'v2': 1, 'v3': 2, 'v4': 3}
        """
        self.assertEqual(single_source_dijkstra_vertices(MinimalPath.cn, 'v1', DistanceType.SHORTEST, min_timing=0), {'v2': 1, 'v3': 2, 'v4': 3})

    def test_vertices_vs_hyperedges_shortest(self):
        """
        checks if the dijkstra algorithm for vertices and hyperedges gives the same result for shortest path
        """
        result_1 = single_source_dijkstra_vertices(MinimalPath.cn, 'v1', DistanceType.SHORTEST, min_timing=0)
        result_2 = single_source_dijkstra_hyperedges(MinimalPath.cn, 'v1', DistanceType.SHORTEST, min_timing=0)
        self.assertEqual(result_1, result_2, 'Single-source Dijkstra implementations are not equivalent')

    def test_vertices_vs_hyperedges_fastest(self):
        """
        checks if the dijkstra algorithm for vertices and hyperedges gives the same result for fastest path
        """
        result_1 = single_source_dijkstra_vertices(MinimalPath.cn, 'v1', DistanceType.FASTEST, min_timing=0)
        result_2 = single_source_dijkstra_hyperedges(MinimalPath.cn, 'v1', DistanceType.FASTEST, min_timing=0)
        self.assertEqual(result_1, result_2, 'Single-source Dijkstra implementations are not equivalent')

    def test_vertices_vs_hyperedges_foremost(self):
        """
        checks if the dijkstra algorithm for vertices and hyperedges gives the same result for foremost path
        """
        result_1 = single_source_dijkstra_vertices(MinimalPath.cn, 'v1', DistanceType.FOREMOST, min_timing=0)
        result_2 = single_source_dijkstra_hyperedges(MinimalPath.cn, 'v1', DistanceType.FOREMOST, min_timing=0)
        self.assertEqual(result_1, result_2, 'Single-source Dijkstra implementations are not equivalent')

class test_stability(unittest.TestCase):
    # changed variable input
    def test_bad_parameter(self):
        """
        gives an integer instead of string with name of source node
        """
        self.assertEqual(single_source_dijkstra_vertices(MinimalPath.cn, 1, DistanceType.SHORTEST, min_timing=0), {'v2': 1, 'v3': 2, 'v4': 3})

    # Repeat test
    def test_graph_fuzzer(self):   # EJ KLAR - Kräver mer alg. Research
        nr_of_nodes = random.randrange(0,10)
        #create nodes

        #create links

        #fuzz it
        for i in range(5):
            pass

class test_correctness(unittest.TestCase):
    def setUp(self):
        """Check to see if the setup works"""
        hedges = {
            'h1': ['v1', 'v2', 'v3'],
            'h2': ['v2', 'v4'],
            'h3': ['v1', 'v3', 'v4'],
        }
        timings = {
            'h1': 1,
            'h2': 2,
            'h3': 3,
        }
        self.hypergraph = TimeVaryingHypergraph(hedges, timings)
    
    def test_shortest_distance(self):
        """test shortest distance for dijkstras"""
        source_vertex = 'v1'
        distance_type = 'SHORTEST'
        min_timing = 0

        expected_distances = {
            'v2': 1,
            'v3': 1,
            'v4': 2,
        }

        distances = single_source_dijkstra_vertices(self.hypergraph, source_vertex, distance_type, min_timing)
        self.assertEqual(distances, expected_distances)

    def test_single_source_dijkstra_vertices(self):
        """test the single source dijkstra function to see if it works as it"""
        # Create a sample hypergraph
        hedges = {
            'h1': ['v1', 'v2', 'v3'],
            'h2': ['v2', 'v4'],
            'h3': ['v1', 'v3', 'v4'],
        }
        timings = {
            'h1': 1,
            'h2': 2,
            'h3': 3,
        }
        hypergraph = TimeVaryingHypergraph(hedges, timings)

        # Compute minimal distances from source vertex 'v1'
        minimal_distances = single_source_dijkstra_vertices(hypergraph, 'v1', DistanceType.SHORTEST, 0)

        # Verify the expected minimal distances
        expected_distances = {
            'v2': 1,
            'v3': 1,
            'v4': 2,
        }
        self.assertEqual(minimal_distances, expected_distances)

