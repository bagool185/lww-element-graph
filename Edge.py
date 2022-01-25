class Edge:

  def __init__(self, vertex1, vertex2):
    self.vertex1 = vertex1
    self.vertex2 = vertex2

  def __eq__(self, other):
    """== operator overloading"""
    return self.vertex1 == other.vertex1 and self.vertex2 == other.vertex2

  def __hash__(self):
    """Required for equality check"""
    return hash(f'{self.vertex1}_{self.vertex2}')