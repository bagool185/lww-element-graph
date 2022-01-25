from typing import List
import unittest
import time 

from Edge import Edge
from LwwGraph import LwwGraph


class TestLwwGraph(unittest.TestCase):

  def test_add_remove_vertex(self):
    current_timestamp = time.time()
    graph = LwwGraph({})

    graph.add_vertex(42, current_timestamp)
    graph.add_vertex(46, current_timestamp)
    self.assertTrue(graph.vertex_exists(42))
    self.assertTrue(graph.vertex_exists(46))
    
    graph.remove_vertex(42, current_timestamp + 10)
    self.assertTrue(graph.vertex_exists(46))
    self.assertFalse(graph.vertex_exists(42))
    
    expected_vertices_list: list = [46]
    self.assertEqual(graph.get_vertices(), expected_vertices_list)

  def test_add_operation_should_be_idempotent(self):

    current_timestamp = time.time()
    graph = LwwGraph({})
    graph.add_vertex(42, current_timestamp)
    self.assertTrue(graph.vertex_exists(42))
    graph.add_vertex(42, current_timestamp - 1)
    graph.add_vertex(42, current_timestamp + 1)
    
    expected_vertices_list: list = [42]
    self.assertEqual(graph.get_vertices(), expected_vertices_list)
    
  def test_remove_operation_should_be_idempotent(self):
    current_timestamp = time.time()
    graph = LwwGraph({})
    graph.remove_vertex(42, current_timestamp)
    self.assertFalse(graph.remove_vertex(42, current_timestamp - 1))
    self.assertFalse(graph.remove_vertex(42, current_timestamp + 1))

    expected_vertices_list: list = []
    self.assertEqual(graph.get_vertices(), expected_vertices_list)

  def test_merge(self):

    first_graph = LwwGraph({})
    second_graph = LwwGraph({})

    first_graph.add_vertex(1, time.time())
    first_graph.add_vertex(5, time.time())
    first_graph.add_vertex(6, time.time())
    first_graph.add_edge(Edge(5, 6), time.time())
    
    second_graph.add_vertex(3, time.time())
    second_graph.add_vertex(2, time.time())
    second_graph.add_vertex(8, time.time())
    second_graph.add_edge(Edge(3, 8), time.time())

    merged: LwwGraph = first_graph.merge(second_graph)
    
    print(merged.edges.add_set.keys())

    assert {1, 2, 3, 5, 6, 8}.issubset(merged.vertices.add_set.keys())

    expected_edges: List[Edge] = [Edge(5, 6), Edge(3,8)]

    self.assertEqual(len(merged.edges.add_set), 2)
    self.assertEqual(expected_edges, list(merged.edges.add_set.keys()))

  def test_add_edge_remove_vertex(self):

    current_timestamp = time.time()
    graph = LwwGraph({})
  
    graph.add_vertex(21, current_timestamp)
    graph.add_vertex(12, current_timestamp)
    graph.add_edge(Edge(21, 12), current_timestamp + 10)
    graph.remove_vertex(12, current_timestamp + 10)

    self.assertTrue(graph.vertex_exists(21))
    self.assertFalse(graph.edge_exists(Edge(21, 12)))


if __name__ == '__main__':
  unittest.main(verbosity=2)
