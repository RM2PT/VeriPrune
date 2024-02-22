#!/bin/bash

mkdir -p compressed_nnets
mkdir -p ../ReluVal-for-comparison/subbed_nnets

for nnet in nnet/ACAS*; do
	compressed_nnet=${nnet/nnet/compressed_nnets}
	compressed_nnet=${compressed_nnet/\.nnet/\_pruned.nnet}
	python3 python/prune_nnet.py $nnet $compressed_nnet
	python3 python/prune_scale_nnet.py $nnet $compressed_nnet \
			${compressed_nnet/compressed_nnets/..\/ReluVal-for-comparison/subbed_nnets}
done
