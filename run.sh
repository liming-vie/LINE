#!/bin/bash

# train graph embedding and do link predction based on cosine similarity 
run() {
  original_graph_file=$1
  edge_file=$2
  checkin_embedding=$3
  output_dir=$4
  result_file=$5

  # train graph embedding
  graph_file=$output_dir/weighted_graph
  python add_weight.py $original_graph_file $graph_file
  graph_embedding=graph_embedding.bin
  sh train_embedding.sh $graph_file $output_dir $graph_embedding 100 128

  python link_prediction.py $output_dir/$graph_embedding $checkin_embedding $edge_file $output_dir/$result_file
}

original_graph_file=../data/edges_remove-20%.txt
edges_num_file=../data/edge_num.txt
checkin_file=../data/totalCheckins.txt
result_file=result

# checkin embedding
output_dir=../output
checkin_graph=$output_dir/checkin_graph
checkin_embedding=checkin_embedding.bin
#python checkin_graph.py $checkin_file $checkin_graph
sh train_embedding.sh $checkin_graph $output_dir $checkin_embedding 500 64

# A/B test
echo '==================== A/B test ====================\n'
output_dir=../output/ab_test
graph_file=$output_dir/sub_graph
losted_file=$output_dir/deleted_graph
edge_file=$output_dir/edges_num
python random_delete.py $original_graph_file $graph_file $losted_file $edge_file 196591
run $graph_file $edge_file $checkin_embedding $output_dir $result_file
python accuracy.py $edge_file $output_dir/$result_file $losted_file

# output result
echo '==================== get result ====================\n'
output_dir=../output/total
run $original_graph_file $edges_num_file $checkin_embedding $output_dir $result_file
