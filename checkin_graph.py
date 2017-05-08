#!/usr/bin/env python
# encoding: utf-8

import sys
from edge import Edge
from tqdm import tqdm

if __name__=='__main__':
  if len(sys.argv) != 3:
    print 'Usage: python checkin_graph.py checkin_file output_file'
    sys.exit(1)

  checkin_file=sys.argv[1]
  output_file=sys.argv[2]

  print 'Loading checkin file...'
  table={}
  with open(checkin_file) as fin:
    for line in tqdm(fin):
      ps=line.rstrip().split()
      uid=ps[0]
      pid=ps[-1]
      if pid not in table:
        table[pid]={}
      if uid not in table[pid]:
        table[pid][uid]=1
      else:
        table[pid][uid]+=1

  print 'Generating checkin graph...'
  edges={}
  for pid in tqdm(table):
    tb=table[pid]
    users=tb.keys()
    for i in xrange(len(users)):
      for j in xrange(i+1, len(users)):
        edge=Edge(users[i], users[j], min(tb[users[i]], tb[users[j]]))
        if edge.hash_val in edges:
          edges[edge.hash_val].score += edge.score
        else:
          edges[edge.hash_val]=edge

  print 'Saving edges in file %s...'%output_file
  edges=edges.values()
  with open(output_file, 'w') as fout:
    for edge in tqdm(edges):
      fout.write('%d\t%d\t%d\n%d\t%d\t%d\n'
          %(edge.v1, edge.v2, edge.score, edge.v2, edge.v1, edge.score))
