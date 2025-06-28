#parameters:
import math_dependencies as md
 #"C:\Users\Matthew\PaperMinecraft\PerlinNoiseProperties.py" "C:\Users\Matthew\PaperMinecraft\Perlin2d.py"
def generatePerlinNoise(scale,numberOfOctaves,offsetX,perlinConfig,seed):#chunkLength=16,width=16,height=16,offsetY=0): #scale (length of chunk in Octave1), width is width of map in terms of Pixels, height as well #add width and height and chunkLength if needed
    #rOV represents range of values, e.g 0 to rOV

    currgrad = []

    def generatePermutationTable():
        perlinConfig.permutationTable = list(md.GeneratePRN(256,perlinConfig.genconsts["A"],perlinConfig.genconsts["C"],perlinConfig.genconsts["M"],seed,(0,255),1))
        perlinConfig.permutationTable += perlinConfig.permutationTable #combine for 512 values in permTable


    def fade(t): #fade/smoothstep Function
        return t ** 3 *(t * (t * 6 - 15) + 10)
    

    def lerp(a, b, t): #linear interpolation
        return a + t * (b - a)
    

    def getDotProduct(ix,iy,x,y):
        gradientIndex = perlinConfig.permutationTable[perlinConfig.permutationTable[ix % 256] + iy % 256] % len(perlinConfig.genconsts["gradients"]) #ensures pesudo-random number extraction
        gradient = perlinConfig.genconsts["gradients"][gradientIndex]
        currgrad.append(gradient)
        dx,dy = x-ix,y-iy #offset Vector (pythagorean distance to gridpoint)
        dotProduct = dx * gradient[0] + dy * gradient[1] #dotproduct Formula
        return dotProduct


    def samplePerlinNoise(x,y):
        x0, x1 = int(x), int(x) + 1
        y0, y1 = int(y), int(y) + 1
        interpolationFactorX = fade(x-x0) #extracted from distance to gridpoint
        interpolationFactorY = fade(y-y0)
        dotProductTopLeft = getDotProduct(x0,y0,x,y) #interpolate horizontally
        dotProductTopRight = getDotProduct(x1,y0,x,y)
        topValue = lerp(dotProductTopLeft,dotProductTopRight,interpolationFactorX)
        dotProductBottomLeft = getDotProduct(x0,y1,x,y) #interpolate horizontally
        dotProductBottomRight = getDotProduct(x1,y1,x,y)
        bottomValue = lerp(dotProductBottomLeft,dotProductBottomRight,interpolationFactorX) 
        finalDotProduct = lerp(topValue, bottomValue, interpolationFactorY) #interpolate vertically   
        return finalDotProduct
    

    

    def getPerlin(scale,offsetX): #generateRawPerlin
        noisemap = []
        for y in range(16):
            row = []
            for x in range(16):
                dotProduct = samplePerlinNoise((x+offsetX)/scale,y/scale) #IMPORTANT! Scale factor tells you the length of chunk/gridcell!
                #print(y*height+x,int(x),int(y),int(x)+1,int(y)+1)
                row.append(dotProduct)
            noisemap.append(row)
        return noisemap
    

    octaves = [] #store octaves after production
    generatePermutationTable()
    for i in range(numberOfOctaves):
        octaves.append(getPerlin(scale/(2**i),offsetX))
    fbmNoise = []
    for z in range(len(octaves[0])): #normalization: extracts values from tuples from list
        ztuple = []
        for y in range(len(octaves[0][0])):
            extractedElements = [val[z][y] for val in octaves]
            sumdps = 0
            for i,element in enumerate(extractedElements):
                sumdps += (element / (2**i))
            ztuple.append(int(sumdps*192+128))
        fbmNoise.append(tuple(ztuple)) #refine to original format
    noise = []
    noise = fbmNoise
        
    return noise
def getChunk0Data(perlinConfig,seed):
    # Generates the 16th block of chunk -1 and 1st block of chunk 1
    vals = (
        generatePerlinNoise(256, 3,16,perlinConfig,0-seed)[0][0],
        generatePerlinNoise(256, 3,16,perlinConfig,seed)[0][0]
    )


    # Uses smoothstep formula that obtains a smooth curve of y values to blend terrain
    def smoothstep(x):
        return x * x * (3 - 2 * x) if 0 <= x <= 1 else (0 if x < 0 else 1)

    def smooth_fade(start, end):
        return [start + (end - start) * smoothstep(i / 15) for i in range(16)]

    chunk0 = smooth_fade(int(vals[1]), int(vals[0]))
    return chunk0








