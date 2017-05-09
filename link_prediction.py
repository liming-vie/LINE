#!/usr/bin/env python
# encoding: utf-8

import sys
import word2vec
import threading
import numpy as np
from edge import Edge
from tqdm import tqdm


class PredictThread(threading.Thread):
  """ Predict Thread
  Thread class for predict most possible edges with cosine metric
  """
  def __init__(self, num_lost, embedding, num_vertice, bi, ei):
    """
    Predict for edge [bi, ei) with needed number of edges num_lost[]
    """
    threading.Thread.__init__(self)
    self.num_lost = num_lost
    self.embedding=embedding
    self.num_vertice = num_vertice
    self.bi=bi
    self.ei=min(ei, num_vertice)

  def run(self):
    ret={}
    for i in xrange(self.bi, self.ei):
      si=str(i)
      if si not in embedding:
        continue
      idxs, scores = self.embedding.cosine(si, n=self.num_lost[i]*20)
      for idx, score in zip(idxs, scores):
        idx = self.embedding.vocab[idx]
        edge=Edge(i, idx, score)
        ret[edge.hash_val] = edge
    self.result=ret.values()

  def get_result(self):
    return self.result


def merge_embedding(graph, checkin, num_vertice):
  print 'Merging graph embedding and checkin embedding...'
  gdim=len(graph['0'])
  cdim=len(checkin['0'])
  vectors=graph.vectors.tolist()
  vocab=graph.vocab.tolist()
  for i in tqdm(xrange(num_vertice)):
    si = str(i)
    if si not in graph:
      if si not in checkin:
        continue
      vocab.append(si)
      graph.vocab = np.array(vocab)
      vectors.append([0.0 for _ in xrange(gdim)])
      graph.vocab_hash[si]=len(vocab)-1
    if si in checkin:
      vec = checkin[si]
    else:
      vec = [0.0 for _ in xrange(cdim)]
    idx = graph.ix(si)
    vectors[idx] = np.append(vectors[idx], vec, 0)
  graph.vectors = np.array(vectors)
  return graph


def predict(embedding, num_lost, num_vertice):
  print 'Predicting...'
  ret={}
  pool=[]
  thread_num=25
  predict_per_thread=100

  # get result from thread t
  def get_result(ret, t):
    t.join()
    for edge in t.get_result():
      if edge.hash_val not in ret:
        ret[edge.hash_val] = edge

  for i in tqdm(xrange(0, num_vertice, predict_per_thread)):
    if len(pool)==thread_num:
      get_result(ret, pool[0])
      pool=pool[1:]
    pool.append(PredictThread(num_lost, embedding, num_vertice, \
            i, i+predict_per_thread))
    pool[-1].start()
  l=len(pool)
  for i in xrange(l):
    get_result(ret, pool[i])
  del pool

  print 'Sorting predicted edges...'
  ret = sorted(ret.values(), key=lambda edge:edge.score, reverse=True)
  needed = sum(num_lost) / 2
  return ret[:needed]


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
    for edge in tqdm(edges):
      fout.write("%d\t%d\n"%(edge.v1, edge.v2))


if __name__=='__main__':
  if len(sys.argv) != 5:
    print 'Usage: python link_prediction.py graph_embedding checkin_embedding edges_num_file output_file'
    sys.exit(1)

  graph_embedding=sys.argv[1]
  checkin_embedding=sys.argv[2]
  edges_num_file=sys.argv[3]
  output_file=sys.argv[4]

  num_lost = get_num_lost(edges_num_file)
  num_vertice=len(num_lost)

  print 'Loading embeddings...'
  graph_embedding = word2vec.load(graph_embedding)
  checkin_embedding = word2vec.load(checkin_embedding)
  embedding=merge_embedding(graph_embedding, checkin_embedding, num_vertice)

  predicted = predict(embedding, num_lost, num_vertice)
  save_edges(predicted, output_file)
