#!/bin/bash

mkdir -p compressed05_nnets
#mkdir -p ../ReluVal-for-comparison/subbed05_nnets

for nnet in nnet/ACAS*; do
	compressed_nnet=${nnet/nnet/compressed05_nnets}
	compressed_nnet=${compressed_nnet/\.nnet/\_pruned05.nnet}
	python3 python/prune_scale_nnet.py $nnet $compressed_nnet
	#python3 python/subtract_nnets.py $nnet $compressed_nnet \
			#${compressed_nnet/compressed_nnets/..\/ReluVal-for-comparison/subbed_nnets}
done
