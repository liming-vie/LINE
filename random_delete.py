#!/usr/bin/env python
# encoding: utf-8

import sys
import random
from tqdm import tqdm
from edge import Edge

def save_edges(edges, foutput):
  with open(foutput, 'w') as fout:
    for edge in edges:
      fout.write('%d\t%d\n%d\t%d\n'%(edge.v1, edge.v2, edge.v2, edge.v1))

def count_edge_num(edges, num_vertice):
  ret=[0 for _ in xrange(num_vertice)]
  for edge in edges:
    ret[edge.v1]+=1
    ret[edge.v2]+=1
  return ret

if __name__=='__main__':
  if len(sys.argv) != 6:
    print 'Usage: python random_delete.py original_graph sub_graph deleted_graph sub_edge_file total_vertice'
    sys.exit(1)

  original_graph=sys.argv[1]
  sub_graph=sys.argv[2]
  deleted_graph=sys.argv[3]
  sub_edge_file=sys.argv[4]
  tot_vertice=int(sys.argv[5])

  print 'Loading edges...'
  edges={}
  with open(original_graph) as fin:
    for line in tqdm(fin):
      ps=line.rstrip().split()
      edge=Edge(ps[0], ps[1])
      edges[edge.hash_val]=edge

  edges=edges.values()
  random.shuffle(edges)

  print 'Saving deleted edges in %s, sub graph in %s'%(deleted_graph, sub_graph)
  tot=len(edges)
  save_edges(edges[:tot/10], deleted_graph)
  save_edges(edges[tot/10:], sub_graph)

  print 'Counting edges number, and save in %s'%sub_edge_file
  original_edge_num = count_edge_num(edges, tot_vertice)
  sub_edge_num = count_edge_num(edges[tot/10:], tot_vertice)
  with open(sub_edge_file, 'w') as fout:
    for i, nums in enumerate(zip(original_edge_num, sub_edge_num)):
      fout.write('%d %d %d\n'%(i, nums[0], nums[1]))
