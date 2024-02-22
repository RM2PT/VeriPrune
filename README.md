

# Table of Contents

1. [File Contents](#file-contents)
2. [Tool Usage Documentation](#tool-usage-documentation)
3. [Running the Experiments](#running-the-experiments)



# File Contents
### DiffNN-Code/ 
This is the source code of VeriPrune. It has the following files:
#### delta\_network\_test.c
The main entry point for Veriprune. It handles parsing the input arguments and starting the verification process.
#### nnet.c
Contains the code for:
- loading a network (function: *load\_network*)
- loading an input property (function: *load\_inputs*)
- performing the forward pass and backward propagation (functions: *forward\_prop\_delta\_symbolic* and *backward\_prop*)
#### nnet.h
Declarations for the functions in nnet.c.
#### split.c
Contains code for:
- The main function that starts the verification process (function: *direct\_run\_check\_delta*) which does the following:
	- Performs the forward pass
	- Checks if the property is satisfied
	- If not, then calling the function to refine the analysis by splitting the input interval (see the next bullet)
- The function that determines which input property to split on, and allocating new memory for the split (function: *split\_interval\_delta*)
#### split.h
Contains the definitions for the above functions.
#### matrix.h
Contains the definition for the struct that stores our matrices and declarations of our matrix mutliplication functions.
#### matrix.c
Contains the functions that call the OpenBLAS matrix multiplication functions on our matrix structs.
#### interval.h
Contains the definition for the struct that represents the intervals during the forward pass.
#### mnist\_tests.h
Defines three data structures for the mnist properties, which are:
- A 2-D array *mnist\_test* that contains 100 test MNIST images (an image is stored as an array of 784 integers)
- An array *correct\_class* of 100 integers corresponding to the correct classification of the 100 test MNIST images
- A 3x100 2-D array *random\_pixels* to determine which pixels to perturb in the 3 pixel experiment. Each entry in this array is a triple of integers each in the range 0-783 which correspond to the three pixels to perturb
#### HAR\_tests.h
Defines two data structures for the HAR properties, which are 
- A 2-D array *HAR\_test* that contains 100 test inputs from the HAR data set
- An array *HAR\_correct\_class* of 100 integers corresponding to the correct classification of the 100 test inputs
#### python/
This directory contains python scripts for
- Create a pruned network (file: *prune\_nnet.py*)(prune one node in the first hidden layer)
- Create a pruned network (file: *prune\_scale_nnet.py*)(prune nodes at scale in every hidden layer)
#### scripts/
This directory contains scripts for:
- Creating all of the pruned networks used in our evaluation (file: *make\_all\_compressed\_nnets.sh*)
- Running all of the experiments in our paper (files: *run\_&#10033;\_exec-time\_experiments.sh* and *run\_ACAS\_prop4\_depth\_exp.sh*)
- Demonstrating example usages of VeriPrune(files: *run\_&#10033;\_artifact.sh*)
#### nnet/
This directory contains all of the neural networks used in our examples. The file format for the neural network is described [here](https://github.com/sisl/NNet/).

# Tool Usage Documentation
Here we document how to use the various scripts and tools for each of the techniques we evaluated in our paper.
### DiffNN-code/delta\_network\_test
This is VeriPrune's main executable. To get a help menu, run *./delta\_network\_test* without any parameters. We also provide the documentation below.
```console
./delta_network_test PROPERTY NNET1 NNET2 EPSILON [OPTIONS]
```
- PROPERTY: an integer value indicating which pre-defined property to verify. The value can be:
	- 1-5, 7-15, 16, 26: These values correspond to the ACAS Xu properties orginally defined by Katz et al. in their [Reluplex](https://arxiv.org/pdf/1702.01135.pdf) and Wang et al. in their [ReluVal](https://arxiv.org/pdf/1804.10829.pdf) paper. See the appendix of [this](https://arxiv.org/pdf/1804.10829.pdf) paper for desciptions. The integers 1-5 and 7-15 directly correspond to properties 1-5 and 7-15 respectively. Property 6 is broken into two parts, corresponding to 16 and 26.
	- 400-499: These values are used for the MNIST properties. Each of the 100 values corresponds to a single input image, and then a perturbation is applied to the image to generate the input property. These properties require that either '-p' or '-t' is specified as an option. If '-p' is specified (see below), a global perturbation will be applied as described in the evaluation of our paper. If '-t' is specified, then three random pixels will be perturbed (see below). 
	- 1000-1099: These values are used for the HAR properties. Each of the 100 values corresponds to a single test input, and then a perturbation is applied to the input to generate the input property. These properties require that '-p' is specified as an option.
- NNET1, NNET2: file paths to \*.nnet files to compare.
- EPSILON: A floating point value. VeriPrune will attempt to verify that NNET1 and NNET2 cannot differ by more than EPSILON over the input region defined by PROPERTY
- OPTIONS<br/>
	-p PERTURB : specifies the strength of the global perturbation to apply to the MNIST and HAR properties. For MNIST this should be an integer between 0-254. For HAR, this should be a float between 0 to 1.<br/>
	-t : Performs three pixel perturbation on the MNIST images instead of global perturbation<br/>
	-m DEPTH : (not used for our paper) forces the analysis to 2^DEPTH splits and then prints region verified at each depth<br/>

### DiffNN-Code/python/prune\_nnet.py
This script takes in a neural net file in the .nnet format, prunes one node in the first hidden layer, and then outputs the result.
```console
python3 prune_nnet.py NNET OUTPUT-PATH
```
- NNET1, NNET2: the two input neural networks to subtract
- OUTPUT-PATH: the location to write the truncated neural net to

### DiffNN-Code/python/prune\_scale\_nnets.py
This script takes in two neural net files in .nnet format and outputs a combined neural net in .nnet format that subtracts the two. Note that the final two layers are assumed to be affine transforms *only* (no ReLU). Our modified ReluVal handles these networks correctly, however the original ReluVal would not handle this correctly.
```console
python3 prune_scale_nnets.py NNET1 NNET2 OUTPUT-PATH
```
- NNET1, NNET2: the two input neural networks to subtract
- OUTPUT-PATH: the output path to write the subtracted neural net to

### DiffNN-Code/scripts/make\_all\_compressed\_nnets.sh
This script will produce all of the truncated and subtracted networks used in our experiments. It takes every network in *DiffNN-Code/nnet*, outputs the truncated network to *DiffNN-Code/compressed\_nnets*, and outputs the subtracted network to *../ReluVal-for-comparison/subbed\_nnets*.

### DiffNN-Code/scripts/run\_&#10033;\_exec-time\_experiments.sh
These four scripts correspond to the four main experiments run in our paper, namey ACAS Xu, MNIST global perturbation, MNIST 3 pixel perturbation, and HAR. They will run VeriPrune on all of the properties for the appropriate experiment and write the results to a log file beginning with *exec-time\_out*. The log file will contain a block of text for each property. The block will start with the command that was run, followed by the command's output. For example, after running ACAS property 1 on ACAS network 1\_1, the following will be written to the log file:
```console
./delta_network_test 1 nnet/ACASXU_run2a_1_1_batch_2000.nnet compressed01_nnets/ACASXU_run2a_1_1_batch_2000_pruned.nnet 0.05
Initial output delta:
[-575.950135 -690.059144 -734.842591 -768.888978 -766.148133]
[578.371154 693.030029 737.171142 769.655822 767.615173]

No adv!
time: 2.422256

numSplits: 2619
```
The two arrays after "Initial output delta:" are the lower and upper bounds of the difference between the two networks computed on the _first forward pass_. "No adv!" indicates that the property was verified, followed by total time taken to verify the property. If there is no line beginning with "time:", then VeriPrune could neither verify nor disprove the property. The last line shows the total number of times the original input interval was split.

### DiffNN-Code/scripts/run\_&#10033;\_artifact.sh
These four scripts contain an example of how to run VeriPrune for a single property of each of the four different experiments.

### DiffNN-Code/scripts/run\_ACAS\_prop4\_depth\_exp.sh
This collects depth information when verifying property 4 as desribed in the evaluation of our paper. Each time the forward pass is able to ceritify a sub-interval, it outputs an integer indicating the current depth to a log file.

# Running the Experiments
Here we document how to re-run our experiments.
## Compile the Code
VeriPrune can be compiled either with or without multi-threading. If you want multithreading, you will need to specify how many threads. In the evaluation of our paper, we configured 10 threads, so if you want to reproduce our experiments, you should compile  VeriPrune as such.

To compile without threads, run:
```console
# from DiffNN-code/ 
make clean all
```

To compile in multi-threaded mode, run:
```console
# from DiffNN-code/ 
CFLAGS+=-DMAX_THREAD=10 make clean all
```
Replace 10 with the desired number of threads.

## Generate the Compressed Networks
```console
# from DiffNN-Code/
bash scripts/make_all_compressed_nnets.sh
```

## Run the experiments
### Artifact Experiments
We provide scripts that run a few  of our main experiments for demonstration purposes. These scripts will write the output directly to the screen. The experiments they run are (in order):
- ACAS property 6
- A single MNIST image globally perturbed on the 3x100 network
- A single MNIST image 3 pixel perturbed on the 3x100 network
- A single HAR input globally perturbed on the HAR network
```console
# from DiffNN-Code/ or ReluVal-for-comparison/
bash scripts/run_ACAS_artifact.sh
bash scripts/run_MNIST-global_artifact.sh
bash scripts/run_MNIST-3pix_artifact.sh
bash scripts/run_HAR_artifact.sh
```
VeriPrune should be able to verify all of these very quickly. 



### Full Experiments
We also provide the scripts to re-run our full experiments. They will output the results to seperate log files beginning with *exec-time\_out*.
```console
# from DiffNN-Code/ 
bash scripts/run_ACAS_exec-time_experiments.sh
bash scripts/run_MNIST-global_exec-time_experiments.sh
bash scripts/run_MNIST-3pix_exec-time_experiments.sh
bash scripts/run_HAR_exec-time_experiments.sh
```

