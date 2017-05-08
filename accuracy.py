#!/usr/bin/env python
# encoding: utf-8

import sys
from edge import Edge

def accuracy(num_lost, predicted, losted):
  print 'Calculating accuracy...'
  correct=0
  for edge in predicted:
    if edge in losted:
      correct+=2
  acc = float(correct) / sum(num_lost)
  print 'Correct %d/%d, Accuracy: %s'%(correct, sum(num_lost), acc)
  return acc

def load_edges(fname):
  edges={}
  with open(fname) as fin:
    for line in fin:
      ps=line.rstrip().split()
      edge=Edge(ps[0], ps[1])
      edges[edge.hash_val]=edge
  return edges

def get_num_lost(edges_num_file):
  print 'Getting edges lost number...'
  ret=[]
  with open(edges_num_file) as fin:
    for line in fin:
      ps = map(int, line.rstrip().split())
      ret.append(ps[1] - ps[2])
  return ret


if __name__ == '__main__':
  if len(sys.argv) != 4:
    print 'Usage: python accuracy.py num_edge_file predicted_file losted_file'
    sys.exit(1)

  num_edge_file=sys.argv[1]
  predicted_file=sys.argv[2]
  losted_file=sys.argv[3]

  num_lost = get_num_lost(num_edge_file)
  predicted_edges = load_edges(predicted_file)
  losted_edges = load_edges(losted_file)

  accuracy(num_lost, predicted_edges, losted_edges)
