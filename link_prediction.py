#!/usr/bin/env python
# encoding: utf-8

import sys
import word2vec
from edge import Edge
from tqdm import tqdm


def merge_embedding(graph, checkin, num_vertice):
  print 'Merging graph embedding and checkin embedding...'
  gdim=len(graph['0'])
  cdim=len(check['0'])
  for i in tqdm(xrange(num_vertice)):
    si = str(i)
    if si not in graph:
      if si not in check:
        continue
      graph.vocab.append(si)
      graph.vectors.append([0.0 for _ in xrange(gdim)])
      graph.vocab_hash[si]=len(graph.vocab)-1
    if si in check:
      graph[si] += check[si]
    else:
      graph[si] += [0.0 for _ in xrange(cdim)]
  return graph


def predict(embedding, num_lost, num_vertice):
  print 'Predicting...'
  ret={}
  for i in tqdm(xrange(num_vertice)):
    si=str(i)
    if si not in embedding:
      continue
    idxs, scores = embedding.cosine(si, n=num_lost[i])
    for idx, score in zip(idxs, scores):
      edge = Edge(i, idx, score)
      if edge.hash_val not in ret:
        ret[edge.hash_val] = edge
  print 'Sorting predicted edges...'
  ret = sorted(ret.values(), key=lambda edge:edge.score, reverse=True)
  print 'Removing unnecessary edges...'
  for edge in ret:

  return ret


def get_num_lost(edges_num_file):
  print 'Getting edges lost number...'
  ret=[]
  with open(edges_num_file) as fin:
    for line in fin:
      ps = map(int, line.rstrip().split())
      ret.append(ps[1] - ps[2])
  return ret


def save_edges(edges, foutput):
  print 'Saving edges in file %s'%foutput
  with open(foutput, 'w') as fout:
    for edge in edges:
      fout.write("%d\t%d\n"%(edge.v1, edge.v2))

if __name__=='__main__':
  if len(sys.argv) != 5:
    print 'Usage: python link_prediction.py graph_embedding checkin_embedding edges_num_file output_file'
    sys.exit(1)

  graph_embedding=sys.argv[1]
  checkin_embedding=sys.argv[2]
  edges_num_file=sys.argv[3]
  output_file=sys.argv[4]

  print 'Loading embeddings...'
  graph_embedding = word2vec.load(graph_embedding)
  embedding=graph_embedding

  num_lost = get_num_lost(edges_num_file)
  num_vertice=len(num_lost)
  predicted = predict(embedding, num_lost, num_vertice)
  save_edges(predicted, output_file)
