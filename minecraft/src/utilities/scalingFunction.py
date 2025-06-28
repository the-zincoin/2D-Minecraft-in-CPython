#Library for future uses (Normalize in rangeOfValues)
def doNormalization(listTonormalize,rangeOfVal,roundOrExact):
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
    
