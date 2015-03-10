# LINE: Large-scale information network embedding

##Introduction

This is the LINE toolkit developed for embedding very large-scale information networks. It is suitable to a variety of networks including directed, undirected, binary or weighted edges. The LINE model is quite efficient, which is able to embed a network with millions of vertices and billions of edges on a single machine within a few hours.
```
Contact: Jian Tang, Microsoft Research Asia, jiatang@microsoft.com, tangjianpku@gmail.com
Project page: https://sites.google.com/site/pkujiantang/line

```
##Usage

We provide both the Windows and LINUX versions. The toolkit uses some external packages to generate random numbers for the edge-sampling algorithm in the LINE model. For Windows version, we use the BOOST package, which can be downloaded at http://www.boost.org/; for LINUX, we use the GSL package, which can be downloaded at http://www.gnu.org/software/gsl/

**Network Input**

The input of a network consists of the edges in the network. Each line of the input file represents a DIRECTED edge in the network, which is specified as the format "source_node target_node weight" (can be either separated by blank or tab). For each undirected edge, users must use TWO DIRECTED edges to represent it. Here is an input example of a word co-occurrence network:
```
good the 3
the good 3
good bad 1
bad good 1
bad of 4
of bad 4
```

**Run**
```
./line -train network_file -output embedding_file -binary 1 -size 200 -order 2 -negative 5 -samples 100 -rho 0.025 -threads 20
```
- -train, the input file of a network;
- -output, the output file of the embedding;
- -binary, whether saving the output file in binary mode; the default is 0 (off);
- -size, the dimension of the embedding; the default is 100;
- -order, the order of the proximity used; 1 for first order, 2 for second order; the default is 2;
- -negative, the number of negative samples used in negative sampling; the deault is 5;
- -samples, the total number of training samples (*Million);
- -rho, the starting value of the learning rate; the default is 0.025;
- -threads, the total number of threads used; the default is 1.




##Citation

```
@inproceedings{tang2015line,
  title={LINE: Large-scale Information Network Embedding.},
  author={Tang, Jian and Qu, Meng and Wang, Mingzhe and Zhang, Ming and Mei, Qiaozhu},
  booktitle={WWW},
  year={2015},
  organization={ACM}
}
```