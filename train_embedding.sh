#!/bin/sh

if [ $# != 5 ] ; then
  echo 'Usage: sh train_embedding.sh input_path output_dir output_file num_samples vec_size'
  exit 1
fi

input_file=$1
output_dir=$2
output_file=$3
num_samples=$4
vec_size=$5

code_dir=./LINE
bin_dir=./LINE/bin

g++ -lm -pthread -Ofast -march=native -Wall -funroll-loops -ffast-math -Wno-unused-result $code_dir/line.cpp -o $bin_dir/line -lgsl -lm -lgslcblas
g++ -lm -pthread -Ofast -march=native -Wall -funroll-loops -ffast-math -Wno-unused-result $code_dir/reconstruct.cpp -o $bin_dir/reconstruct
g++ -lm -pthread -Ofast -march=native -Wall -funroll-loops -ffast-math -Wno-unused-result $code_dir/normalize.cpp -o $bin_dir/normalize
g++ -lm -pthread -Ofast -march=native -Wall -funroll-loops -ffast-math -Wno-unused-result $code_dir/concatenate.cpp -o $bin_dir/concatenate

dense_file=$output_dir/graph.dense
wo_norm_1st=$output_dir/vecs.1st_wo_norm
wo_norm_2nd=$output_dir/vecs.2nd_wo_norm
vec_1st=$output_dir/vecs.1st_vec
vec_2nd=$output_dir/vecs.2nd_vec

$bin_dir/reconstruct -train $input_file -output $dense_file -depth 2 -k-max 1000
$bin_dir/line -train $dense_file -output $wo_norm_1st -binary 1 -size $vec_size -order 1 -negative 5 -samples $num_samples -threads 40
$bin_dir/line -train $dense_file -output $wo_norm_2nd -binary 1 -size $vec_size -order 2 -negative 5 -samples $num_samples -threads 40
$bin_dir/normalize -input $wo_norm_1st -output $vec_1st -binary 1
$bin_dir/normalize -input $wo_norm_2nd -output $vec_2nd -binary 1
$bin_dir/concatenate -input1 $vec_1st -input2 $vec_2nd -output $output_dir/$output_file -binary 1
