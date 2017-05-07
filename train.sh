#!/bin/sh

if [ $# != 4 ] ; then
  echo 'Usage: sh train.sh input_dir input_file output_dir output_file'
  exit 1
fi

input_dir=$1
input_file=$2
output_dir=$3
output_file=$4

g++ -lm -pthread -Ofast -march=native -Wall -funroll-loops -ffast-math -Wno-unused-result line.cpp -o line -lgsl -lm -lgslcblas
g++ -lm -pthread -Ofast -march=native -Wall -funroll-loops -ffast-math -Wno-unused-result reconstruct.cpp -o reconstruct
g++ -lm -pthread -Ofast -march=native -Wall -funroll-loops -ffast-math -Wno-unused-result normalize.cpp -o normalize
g++ -lm -pthread -Ofast -march=native -Wall -funroll-loops -ffast-math -Wno-unused-result concatenate.cpp -o concatenate

weighted_network=$output_dir/graph.weighted
python add_weight.py $input_dir/$input_file $weighted_network

dense_file=$output_dir/graph.dense
1st_wo_norm=$output_dir/vecs.1st_wo_norm
2st_wo_norm=$output_dir/vecs.2nd_wo_norm
1st_vec=$output_dir/vecs.1st_vec
2st_vec=$output_dir/vecs.2st_vec

./reconstruct -train $weighted_network -output $dense_file -depth 2 -k-max 1000
./line -train $dense_file -output $1st_wo_norm -binary 1 -size 128 -order 1 -negative 5 -samples 1000 -threads 40
./line -train $dense_file -output $2nd_wo_norm -binary 1 -size 128 -order 2 -negative 5 -samples 1000 -threads 40
./normalize -input $1st_wo_norm -output $1st_vec -binary 1
./normalize -input $2nd_wo_norm -output $2nd_vec -binary 1
./concatenate -input1 $1st_vec -input2 $2nd_vec -output $output_dir/$output_file -binary 1
