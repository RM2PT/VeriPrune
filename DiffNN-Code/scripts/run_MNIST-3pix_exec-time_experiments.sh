#!/bin/bash

perturb=3
eps=1
timeout=1800
compressed_nnets="compressed_nnets/mnist_relu_2_512_pruned.nnet
compressed_nnets/mnist_relu_3_100_pruned.nnet
compressed_nnets/mnist_relu_4_1024_pruned.nnet"

IFS=$'\n'
for compressed_nnet in $compressed_nnets; do
	out="exec-time_out_${compressed_nnet/compressed_nnets\//}"
	> $out
	for testcase in $( seq 400 499 ); do
		orig_nnet=${compressed_nnet/compressed_nnets/nnet}
		orig_nnet=${orig_nnet/\_pruned\.nnet/\.nnet}
		echo "./delta_network_test $testcase $orig_nnet $compressed_nnets $eps -p $perturb -t" >> $out
		timeout $timeout ./delta_network_test \
			$testcase \
			$orig_nnet $compressed_nnet\
			$eps -p $perturb -t 2>> $out
	done
done
