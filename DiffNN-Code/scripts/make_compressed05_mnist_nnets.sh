#!/bin/bash

mkdir -p compressed_nnets
mkdir -p ../ReluVal-for-comparison/subbed_nnets

nnets="mnist_relu_4_1024.nnet
mnist_relu_3_100.nnet
mnist_relu_2_512.nnet"

for nnet in $nnets; do
	python3 python/prune_scale_nnet.py nnet/$nnet \
			compressed05_nnets/${nnet/\.nnet/_pruned05.nnet}
	#python3 python/subtract_nnets.py nnet/$nnet \
			#compressed_nnets/${nnet/\.nnet/_pruned.nnet} \
			#../ReluVal-for-comparison/subbed_nnets/${nnet/\.nnet/_pruned.nnet}
done
