#!/usr/bin/env python
# encoding: utf-8

class Edge:
  """ Edge
  v1, v2: vertice index connecting to this edge, always let v1<v2
  hash_val: hash value for this edge, only care about v1 and v2
  score: edge weight or score
  """
  def __init__(self, v1, v2, s=0.):
    v1, v2=[int(v1), int(v2)]
    if v1>v2:
      self.v1, self.v2=[v2,v1]
    else:
      self.v1, self.v2=[v1,v2]
    self.hash_val=hash(str([self.v1,self.v2]))
    self.score=s

  def equal(self, v1, v2):
    if v1>v2:
      return self.hash_val == hash(str([v2, v1]))
    return self.hash_val == hash(str([v1, v2]))
