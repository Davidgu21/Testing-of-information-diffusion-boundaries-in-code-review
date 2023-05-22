import unittest
import unittest.mock
from unittest.mock import MagicMock


from simulation.model import CommunicationNetwork
from simulation.model import TimeVaryingHypergraph
from simulation.model import EntityNotFound


class ModelTest(unittest.TestCase):

    cn = CommunicationNetwork({'h1': ['v1', 'v2'], 'h2': ['v2', 'v3'], 'h3': ['v3', 'v4']}, {'h1': 1, 'h2': 2, 'h3': 3})

    def test_vertices(self):
        self.assertEqual(len(ModelTest.cn.vertices()), 4)
        self.assertEqual(ModelTest.cn.vertices('h1'), {'v1', 'v2'})

    def test_hyperedges(self):
        self.assertEqual(len(ModelTest.cn.hyperedges()), 3)
        self.assertEqual(ModelTest.cn.hyperedges('v1'), {'h1'})


class ModelDataTest(unittest.TestCase):
    def test_model_with_data(self):
        communciation_network = CommunicationNetwork.from_json('./data/networks/microsoft.json.bz2')
        self.assertEqual(len(communciation_network.participants()), 37103)
        self.assertEqual(len(communciation_network.channels()), 309740)

        self.assertEqual(len(communciation_network.vertices()), 37103)
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


    def test_TimeVaryingHyperGraph_empty(self):
        """Tests the hyperedges, timings and vertices functions with empty input"""
        
        hypergraph = TimeVaryingHypergraph({}, {})

        self.assertEqual({}, hypergraph.hyperedges())
        self.assertEqual({}, hypergraph.timings())
        self.assertEqual({}, hypergraph.vertices())

    def test_TimeVaryingHyperGraph_no_vertices(self):
        """Tests the vertices class function with no vertices"""
        
        hypergraph = TimeVaryingHypergraph({"h1":[], "h2":[]}, {"h1": 1, "h2": 2})

        #gives set() when empty not {}
        self.assertEqual({}, hypergraph.vertices())
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
    

    def test_time_varying_hypergraph_exceptions_input_strings(self):
        hyper_graph = TimeVaryingHypergraph({'h1': ['v1', 'v2'], 'h2': ['v2', 'v3'], 'h3': ['v3', 'v4']}, {'h1': 'words', 'h2': 'words', 'h3': 'words'})#changed integers to strings
        self.assertRaises(hyper_graph)

    def test_time_varying_hypergraph_exceptions_input_ints(self):
        hyper_graph = TimeVaryingHypergraph({1: [1, 2], 2: [2, 3], 3: [3, 4]}, {1: 1, 2: 2, 3: 3})#changed strings to integers
        self.assertRaises(hyper_graph)

    def test_datastructure_constructor(self):
        pass
            
            
class TestCommunicationNetwork(unittest.TestCase):
    
    def test_from_json(self):
        """Mocks the open function, not done yet"""
        file_path = "file/path"
        #needs fix
        with unittest.mock.patch('pathlib.Path.open', unittest.mock.mock_open()) as mock_file:
            with unittest.mock.patch('json.loads', MagicMock(side_effect= [{"foo": "bar"}])) as json_mock:
                CommunicationNetwork.from_json(file_path)

                mock_file.assert_called_once()
                mock_file.read.assert_called_once()

        #maybe mock
        
    
    
