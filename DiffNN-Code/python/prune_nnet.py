from common import *
import sys

def nodePrune_nnet(nnet):
    import numpy as np

    weights = nnet["weights"]
    biases = nnet["biases"]

    #find the least important node in first hidden layer
    onorm = []
    j = 0
    while j < nnet["layerSizes"][1]:
        temp = 0.0
        i = 0
        while i < nnet["layerSizes"][2]:
            temp = temp + abs(float(nnet["weights"][1][i][j]))
            i = i + 1
        onorm.append(temp)
        j = j + 1

    #print(len(onorm))
    #print(onorm)

    #locate the node
    locate = onorm.index(min(onorm))
    #print((locate))

    #prune weight
    #nnet["layerSizes"][1] -=1
    i = 0
    while i < nnet["layerSizes"][0]:
        nnet["weights"][0][locate][i] = 0
        i = i + 1
    i = 0
    while i < nnet["layerSizes"][2]:
        nnet["weights"][1][i][locate] = 0
        i = i + 1
    nnet["biases"][0][locate] = -1.0


    #write back
    new_weights = []
    new_biases = []
    for k, weightMatrix in enumerate(weights):
        matrix = []
        for row in weightMatrix:
            matrix.append(list(map(lambda f: np.float16(f), row)))
        new_weights.append(matrix)

        bias = list(map(lambda f: np.float16(f), biases[k]))
        new_biases.append(bias)
    nnet["weights"] = new_weights
    nnet["biases"] = new_biases
    return nnet

def main():
    if len(sys.argv) != 3:
        print("usage: python %s <nnet-path> <output-path> " % (sys.argv[0]))
        exit(1)

    nnet = read_network(sys.argv[1])


    #print(nnet["layerSizes"])
    #print(len(nnet["weights"][3][1]))
    #print(nnet["biases"][0])

    pruned_nnet = nodePrune_nnet(nnet)

    #print(pruned_nnet["layerSizes"])
    write_network(pruned_nnet, sys.argv[2])

if __name__ == "__main__":
    main()
