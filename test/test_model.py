import unittest
import unittest.mock
from unittest.mock import MagicMock
import json


from simulation.model import CommunicationNetwork
from simulation.model import TimeVaryingHypergraph
from simulation.model import EntityNotFound


class ModelTest(unittest.TestCase):

    cn = CommunicationNetwork({'h1': ['v1', 'v2'], 'h2': ['v2', 'v3'], 'h3': ['v3', 'v4']}, {'h1': 1, 'h2': 2, 'h3': 3})

    def test_vertices_len(self):
        self.assertEqual(len(ModelTest.cn.vertices()), 4)

    def test_vertices(self):
        self.assertEqual(ModelTest.cn.vertices('h1'), {'v1', 'v2'})

    def test_hyperedges_len(self):
        self.assertEqual(len(ModelTest.cn.hyperedges()), 3)

    def test_hyperedges(self):
        self.assertEqual(ModelTest.cn.hyperedges('v1'), {'h1'})


class ModelDataTest(unittest.TestCase):
    def test_model_with_data_participants(self):
        communciation_network = CommunicationNetwork.from_json('./data/networks/microsoft.json.bz2')
        self.assertEqual(len(communciation_network.participants()), 37103)

    def test_model_with_data_channels(self):
            communciation_network = CommunicationNetwork.from_json('./data/networks/microsoft.json.bz2')
            self.assertEqual(len(communciation_network.channels()), 309740)

    def test_model_with_data_vertices(self):
        communciation_network = CommunicationNetwork.from_json('./data/networks/microsoft.json.bz2')
        self.assertEqual(len(communciation_network.vertices()), 37103)
    
    def test_model_with_data_hyperedges(self):
        communciation_network = CommunicationNetwork.from_json('./data/networks/microsoft.json.bz2')
        self.assertEqual(len(communciation_network.hyperedges()), 309740)


class TestTimeVaryingHypergraph(unittest.TestCase):
    """Tests the TimeVaryingHypergraph class"""

    def test_TimeVaryingHypergraph_vertex(self):
        """Tests that the correct hyperedges are returned by hyperedges class function"""

        hypergraph = TimeVaryingHypergraph({"h1": ["v1","v2"]}, {"h1": 1, "h2": 4})

        #gives hedges(first param)
        self.assertEqual({"h1"}, hypergraph.hyperedges())

    def test_TimeVaryingHypergraph_vertices(self):
        """Tests that the correct vertices are returned by the vertices class function"""
        
        hypergraph = TimeVaryingHypergraph({"h1" : ["v1", "v2"]}, {"h1": 1})

        self.assertEqual({"v1", "v2"}, hypergraph.vertices())

    def test_TimeVaryingHypergraph_timings(self):
        """Tests that the correct timings are returned by the timings class function"""

        hypergraph = TimeVaryingHypergraph({"h1": ["v1", "v2"]}, {"h1":1, "h2":32})

        self.assertEqual({"h1": 1, "h2":32}, hypergraph.timings())



    def test_TimeVaryingHyperGraph_empty_hyperedges(self):
        """Tests the hyperedges, timings and vertices functions with empty input"""
        
        hypergraph = TimeVaryingHypergraph({}, {})

        self.assertEqual({}, hypergraph.hyperedges())
    
    def test_TimeVaryingHyperGraph_empty_timings(self):
        """Tests the hyperedges, timings and vertices functions with empty input"""
            
        hypergraph = TimeVaryingHypergraph({}, {})

        self.assertEqual({}, hypergraph.timings())

    def test_TimeVaryingHyperGraph_empty_vertices(self):
        """Tests the hyperedges, timings and vertices functions with empty input"""
            
        hypergraph = TimeVaryingHypergraph({}, {})

        self.assertEqual({}, hypergraph.vertices())


    def test_TimeVaryingHyperGraph_no_vertices(self):
        """Tests the vertices class function with no vertices"""
        
        hypergraph = TimeVaryingHypergraph({"h1":[], "h2":[]}, {"h1": 1, "h2": 2})

        #gives set() when empty not {}
        self.assertEqual({}, hypergraph.vertices())

    def test_TimeVaryingHyperGraph_no_vertices_len(self):
        """Tests the vertices class function with no vertices"""
            
        hypergraph = TimeVaryingHypergraph({"h1":[], "h2":[]}, {"h1": 1, "h2": 2})

        #gives set() when empty not {}
        self.assertEqual(len(hypergraph.vertices()), 0)

    
    def test_TimeVaryingHyperGraph_unknown_edge(self):
        """Tests that the hyperedges class function raises the correct exception when input is a unknown edge"""
        hypergraph = TimeVaryingHypergraph({"h1": ["v1", "v2"]}, {"h1":1})

        with self.assertRaises(EntityNotFound) as err:
            hypergraph.hyperedges("v3")

    def test_TimeVaryingHyperGraph_unknown_vertex(self):
        """Tests that the vertices class function raises the correct exception when input is a unknow vertex """
        hypergraph = TimeVaryingHypergraph({"h1": ["v1"]}, {"h1":1})

        with self.assertRaises(EntityNotFound) as err:
            hypergraph.vertices("h2")
    
class TestTimeVaryingHypergraphCorrectness(unittest.TestCase):
    """these tests check to see whether various methods return their expected outputs"""
    def test_datastructure_constructor_hedges(self):
        """this unittest is intented to make sure that the constructor works properly for the hyperedges"""
        hyper_graph = TimeVaryingHypergraph({'h1': ['v1', 'v2'], 'h2': ['v2', 'v3'], 'h3': ['v3', 'v4']}, {'h1': 1, 'h2': 2, 'h3': 3})
        self.assertEqual(hyper_graph._hedges, {'h1': ['v1', 'v2'], 'h2': ['v2', 'v3'], 'h3': ['v3', 'v4']})

    def test_datastructure_constructor_vertices(self):
        """this unittest is intented to make sure that the constructor works properly for the vertices"""
        hyper_graph = TimeVaryingHypergraph({'h1': ['v1', 'v2'], 'h2': ['v2', 'v3'], 'h3': ['v3', 'v4']}, {'h1': 1, 'h2': 2, 'h3': 3})
        self.assertEqual(hyper_graph._vertices, {'v1': ['h1'], 'v2': ['h1', 'h2'], 'v3': ['h2', 'h3'], 'v4': ['h3']})

class TestTimeVaryingHypergraphInputs(unittest.TestCase):      
    """these tests are designed to see how the hypergraph class responds to various inputs"""
    def test_time_varying_hypergraph_exceptions_input_strings(self):
        """testing how the datastructure handles inputs that are all strings"""
        hyper_graph = TimeVaryingHypergraph({'h1': ['v1', 'v2'], 'h2': ['v2', 'v3'], 'h3': ['v3', 'v4']}, {'h1': 'words', 'h2': 'words', 'h3': 'words'})
        self.assertRaises(hyper_graph)

    def test_time_varying_hypergraph_exceptions_input_ints(self):
        """testing how the datastructure handles inputs that are all integers"""
        hyper_graph = TimeVaryingHypergraph({1: [1, 2], 2: [2, 3], 3: [3, 4]}, {1: 1, 2: 2, 3: 3})
        self.assertRaises(hyper_graph)

class TestCommunicationNetwork(unittest.TestCase):
    
    def test_from_json(self):
        """Mocks the open function, tests that open and read are called"""
        file_path = "file/path"
        #tests with orjson, if json change orsjon.loads to json.loads 
        with unittest.mock.patch('pathlib.Path.open', unittest.mock.mock_open(read_data="fake file")) as mock_file:
            with unittest.mock.patch('orjson.loads', MagicMock(side_effect= [{"-1000045392462314428":{"bound":"right_bounded","end":"2020-02-05T12:49:39","participants":[-4790071369877151138,-6410414390854871141],"start":"2020-02-04T07:10:58"}}])) as json_mock:
                CommunicationNetwork.from_json(file_path)
                
                #test that open() is called
                mock_file.assert_called_once()
                #test that read() is called
                mock_file().read.assert_called_once()

    
        
    
    
