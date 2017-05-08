#!/usr/bin/env python
# encoding: utf-8

import sys
from tqdm import tqdm

if __name__ == '__main__':
  if len(sys.argv) != 3:
    print 'Usage: python add_weight.py input_file output_file'
    sys.exit(1)

  input_file=sys.argv[1]
  output_file=sys.argv[2]

  print 'Adding weight 1.0 for each edges...'
  with open(input_file) as fin, open(output_file, 'w') as fout:
    for line in tqdm(fin):
      fout.write("%s\t1\n"%line.rstrip())
