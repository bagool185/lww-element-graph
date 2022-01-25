class LwwElementSets:

  def __init__(self):
    self.add_set = {}
    self.remove_set = {}

  def element_exists(self, element) -> bool:

    if element not in self.add_set:
      return False
    elif element not in self.remove_set:
      return True
    # make sure the latest operation was 'add' if element is in both sets 
    elif self.remove_set[element] - self.add_set[element] <= 0:
      return True
    
    return False 

  def sync_timestamp(self, elem, timestamp):
    """Make sure the latest timestamp is used for concurrent operations"""
    if elem in self.remove_set:
      if self.remove_set[elem] < timestamp:
        self.remove_set[elem] = timestamp 
    else:
      self.remove_set[elem] = timestamp

  @staticmethod
  def __merge_sets(first_set, second_set):
    """Create a union of the add & remove sets"""
    for key in second_set:
      if key not in first_set:
        first_set[key] = second_set[key]
      else:
        if second_set[key] > first_set[key]:
          first_set[key] = second_set[key]

  def merge(self, second_elem):
    LwwElementSets.__merge_sets(self.add_set, second_elem.add_set)
    LwwElementSets.__merge_sets(self.remove_set, second_elem.remove_set)