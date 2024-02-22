#!/bin/bash

mkdir -p compressed_nnets
mkdir -p ../ReluVal-for-comparison/subbed_nnets

nnet="HAR.nnet"

python3 python/prune_nnet.py nnet/$nnet \
		compressed_nnets/${nnet/\.nnet/_pruned.nnet}
python3 python/prune_scale_nnet.py nnet/$nnet \
		compressed_nnets/${nnet/\.nnet/_pruned.nnet} \
		../ReluVal-for-comparison/subbed_nnets/${nnet/\.nnet/_pruned.nnet}
