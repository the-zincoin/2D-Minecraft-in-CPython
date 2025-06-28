#PseudoRandom NumberGenerator Library
import scalingFunction
def GeneratePRN(iterations,A,C,M,seed,rangeOfVal,rOE):
    instances = []
    newseed = seed
    for i in range(iterations): #permutationTable via LCG
        nextseed = (A*newseed + C) % M 
        instances.append(nextseed)
        newseed = nextseed
    return scalingFunction.doNormalization(instances,rangeOfVal,rOE)