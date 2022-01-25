import time
from typing import List

import LwwElementSets, Edge


class LwwGraph:

  def __init__(self, adjacency_list: List[any]) -> None:
      self.vertices = LwwElementSets()
      self.edges = LwwElementSets()
      self.adjacency_list = adjacency_list

  def edge_exists(self, edge: Edge) -> bool:
    if self.vertex_exists(edge.vertex1) and self.vertex_exists(edge.vertex2):
      return self.edges.element_exists(edge)

    return False

  def vertex_exists(self, vertex) -> bool:
    return self.vertices.element_exists(vertex)

  def add_vertex(self, vertex, timestamp):
    
    time_now = time.time()

    if self.vertex_exists(vertex):
      return False 

    if vertex in self.vertices.remove_set:
      if self.vertices.remove_set[vertex] <= timestamp:
        if timestamp < time_now:
          timestamp = time_now

        self.vertices.add_set[vertex] = timestamp
        self.adjacency_list[vertex] = []

        return True

    else:
      if timestamp < time_now:
        timestamp = time_now
      
      self.vertices.add_set[vertex] = timestamp
      self.adjacency_list[vertex] = []

      return True

    return False

  def __create_edge(self, edge: Edge):
    self.adjacency_list[edge.vertex1].append(edge.vertex2)
    self.adjacency_list[edge.vertex2].append(edge.vertex1)

  def add_edge(self, edge: Edge, timestamp):

    if self.vertex_exists(edge.vertex1) and self.vertex_exists(edge.vertex2):

      if not self.edge_exists(edge):
        self.edges.add_set[edge] = timestamp
        self.__create_edge(edge)

        return True 

      return False
  
  def remove_vertex(self, vertex, timestamp):

    if self.vertex_exists(vertex):

      self.vertices.sync_timestamp(vertex, timestamp)
    
      if self.vertices.remove_set[vertex] > self.vertices.add_set[vertex]:
        
        for v in self.adjacency_list:
          if vertex in self.adjacency_list[v]:
            self.adjacency_list[v].remove(vertex)

        self.adjacency_list.pop(vertex)
        return True 

      else:
        self.vertices.remove_set[vertex] = timestamp 
        return False 
    else:
      self.vertices.sync_timestamp(vertex, timestamp)

  def remove_edge(self, edge: Edge, timestamp):

    if self.edge_exists(edge):
      self.edges.sync_timestamp(edge, timestamp)

      if self.edges.remove_set[edge] > self.edges.remove_set[edge]:
        self.adjacency_list[edge.vertex1].remove(edge.vertex2)
        self.adjacency_list[edge.vertex2].remove(edge.vertex1)

        return True

      return False 
    else: 
      if edge in self.edges.remove_set:
        self.edges.sync_timestamp(edge, timestamp)

  def find_path(self, start_vertex, end_vertex, path = None):

    if path is None:
      path = []

    if self.vertex_exists(start_vertex) and self.vertex_exists(end_vertex):
      path += [start_vertex]

      if start_vertex == end_vertex:
        return path

      if start_vertex not in self.adjacency_list:
        return None  

      for vertex in self.adjacency_list[start_vertex]:
        if vertex not in path:
          new_path = self.find_path(vertex, end_vertex, path)
          if new_path:
            return new_path
    
    return None

  def merge(self, lww_graph):
    self.vertices.merge(lww_graph.vertices)
    self.edges.merge(lww_graph.edges)

    return self

  def get_vertices(self) -> list:

      vertices = []

      for vertex in self.vertices.add_set:
        if self.vertices.element_exists(vertex):
          vertices.append(vertex)

      return vertices
