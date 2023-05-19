import unittest
import random

from simulation.model import CommunicationNetwork
from simulation.minimal_paths import single_source_dijkstra_vertices, single_source_dijkstra_hyperedges, DistanceType, TimeVaryingHypergraph


class MinimalPath(unittest.TestCase):
    cn = CommunicationNetwork({'h1': ['v1', 'v2'], 'h2': ['v2', 'v3'], 'h3': ['v3', 'v4']}, {'h1': 1, 'h2': 2, 'h3': 3})
    tm = TimeVaryingHypergraph({'h1': ['v1', 'v2'], 'h2': ['v2', 'v3'], 'h3': ['v3', 'v4']}, {'h1': 1, 'h2': 2, 'h3': 3})

    def test_known_path(self):
        """
        Tests if shortest path is eqivelent to a specific dictionary:
        {'v2': 1, 'v3': 2, 'v4': 3}
        """
        self.assertEqual(single_source_dijkstra_vertices(MinimalPath.cn, 'v1', DistanceType.SHORTEST, min_timing=0), {'v2': 1, 'v3': 2, 'v4': 3})

    def test_7(self):
        self.assertEqual(single_source_dijkstra_vertices(MinimalPath.tm, 'v1', DistanceType.SHORTEST, min_timing=0), {'v2': 1, 'v3': 2, 'v4': 3})

    def test_vertices_vs_hyperedges_shortest(self):
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


    def test_timings(self):
        """Tests the timings with the help of tm"""
        self.assertEqual(MinimalPath.tm.timings(), {'h1': 1, 'h2': 2, 'h3': 3})
 
    def test_vertices(self):
        """Tests the vertices with the help of tm"""
        self.assertEqual(MinimalPath.tm.vertices(), {'v1', 'v2', 'v3', 'v4'})

    def test_hyperedges(self):
        """Tests the hyperedges with the help of tm"""
        self.assertEqual(MinimalPath.tm.hyperedges(), {'h1', 'h2', 'h3'})
     # changed variable input
    # def test_5_wierd_parameter(self):
    #     self.assertEqual(single_source_dijkstra_vertices(MinimalPath.cn, 'v1', DistanceType.SHORTEST, min_timing=0), {'v2': 2, 'v3': 2, 'v4': 3})

    # Repeat test
    def test_6(self):   # EJ KLAR - Kräver mer alg. Research
        rep_dict = {
            'v2': 2,
            'v3': 2,
            'v4': 3
        }

        for i in range(5):
            result_1 = single_source_dijkstra_vertices(MinimalPath.cn, 'v1', DistanceType.SHORTEST, min_timing=0)
            result_2 = single_source_dijkstra_vertices(MinimalPath.cn, 'v1', DistanceType.SHORTEST, min_timing=0)



class CorrectnessTest(unittest.TestCase):

    def test_if_empty(self):
        hedges = {}
        timings = {}

        hyper = TimeVaryingHypergraph(hedges, timings)
        self.assertDictEqual(single_source_dijkstra_vertices(hyper, None, DistanceType.SHORTEST, min_timing=0), {})

    def setUp(self):
        """tests the setup"""
        channels = {
            'channel1': ['participant1', 'participant2'],
            'channel2': ['participant2', 'participant3'],
            'channel3': ['participant1', 'participant3']
        }

        # Create an instance of CommunicationNetwork for testing
        self.network = self.CommunicationNetwork(channels, name='Test Network')

    def test_channels(self):
        """Tests the channels"""
        expected_result = {'channel1', 'channel2', 'channel3'}
        self.assertEqual(self.network.channels(), expected_result)

    def test_participants(self):
        """Tests the participants"""
        expected_result = {'participant1', 'participant2', 'participant3'}
        self.assertEqual(self.network.participants(), expected_result)

    def test_vertices(self):
        """Test the vertices"""
        expected_result = {'channel1', 'channel3'}
        self.assertEqual(self.network.vertices('participant1'), expected_result)

    def test_hyperedges(self):
        """Tests the hyperedges() method"""
        expected_result = {'participant1', 'participant2'}
        self.assertEqual(self.network.hyperedges('channel1'), expected_result)

    def test_timings(self):
        """Tests the timings"""
        self.assertIsNone(self.network.timings())  # No timings provided in this test case
        expected_result = None
        self.assertEqual(self.network.timings('channel2'), expected_result)
