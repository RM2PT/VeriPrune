from common import *
import sys

def nodePrune_nnet(nnet):
    import numpy as np

    weights = nnet["weights"]
    biases = nnet["biases"]
    hidden_numlayers = nnet["numLayers"] - 1
    #print(hidden_numlayers)

    #find 30% nodes in each hidden layer
    h = 0
    while h < hidden_numlayers:
        onorm = []
        j = 0
        while j < nnet["layerSizes"][h+1]:
            temp = 0.0
            i = 0
            while i < nnet["layerSizes"][h+2]:
                temp = temp + abs(float(nnet["weights"][h+1][i][j]))
                i = i + 1
            onorm.append(temp)
            j = j + 1

        #print(len(onorm))
        #print(onorm)

        p = 0
        while p < int(nnet["layerSizes"][h+1] * 0.0010):
            #locate the node
            locate = onorm.index(min(onorm))
            onorm[locate] = sys.float_info.max

            #prune weight
            i = 0
            while i < nnet["layerSizes"][h]:
                nnet["weights"][h][locate][i] = 0
                i = i + 1
            i = 0
            while i < nnet["layerSizes"][h+2]:
                nnet["weights"][h+1][i][locate] = 0
                i = i + 1
            nnet["biases"][h][locate] = -1.0

            onorm.pop(locate)
            p = p + 1

        h = h + 1


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
#    if len(sys.argv) != 3:
    if len(sys.argv) != 4 and len(sys.argv) != 5:
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
