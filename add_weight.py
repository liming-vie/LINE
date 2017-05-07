#!/usr/bin/env python
# encoding: utf-8

import sys
from tqdm import tqdm

input_file=sys.argv[1]
output_file=sys.argv[2]

with open(input_file) as fin, open(output_file, 'w') as fout:
  for line in tqdm(fin):
    fout.write("%s 1\n"%line.rstrip())
