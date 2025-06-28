def largest_2_to_1_rectangle(L_width, L_height):
    # Maximum height based on aspect ratio and larger rectangle's dimensions
    max_height = min(L_height, L_width / 2)
    max_length = 2 * max_height  # Length is twice the height
    return max_length, max_height

#Normalize Range Of Values
def do_normalization(listTonormalize,rangeOfVal,roundOrExact):
    if min(listTonormalize) != 0:
        for i in range(len(listTonormalize)):
            listTonormalize[i] -= min(listTonormalize)
    else:
        pass
    scaleFactor = (rangeOfVal[1]-rangeOfVal[0]) / max(listTonormalize)
    if roundOrExact == 1:
        listTonormalize = [round(val*scaleFactor)+rangeOfVal[0] for val in listTonormalize]
        return listTonormalize
    elif roundOrExact == 2:
        listTonormalize = [val*scaleFactor+rangeOfVal[0] for val in listTonormalize]
        return listTonormalize
    else:
        return ValueError
    

#generate perlin required RNG
def GeneratePRN(iterations,A,C,M,seed,rangeOfVal,rOE):
    instances = []
    newseed = seed
    for i in range(iterations): #permutationTable via LCG
        nextseed = (A*newseed + C) % M 
        instances.append(nextseed)
        newseed = nextseed
    return do_normalization(instances,rangeOfVal,rOE)