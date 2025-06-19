#parameters:
import WorldClasses,RNGMinecraft   #"C:\Users\Matthew\PaperMinecraft\PerlinNoiseProperties.py" "C:\Users\Matthew\PaperMinecraft\Perlin2d.py"
def generatePerlinNoise(scale,numberOfOctaves,seed,chunkNum,chunkLength,width,height,rOV,offsetX,offsetY): #scale (length of chunk in Octave1), width is width of map in terms of Pixels, height as well
    #rOV represents range of values, e.g 0 to rOV

    world = WorldClasses.PerlinProperties(25214903917,11,2**48,seed,[],[(1, 1), (-1, 1), (1, -1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)],chunkNum,chunkLength,[])
    currgrad = []

    def generatePermutationTable():
        world.permutationTable = list(RNGMinecraft.GeneratePRN(256,world.A,world.C,world.M,world.firstSeed,(0,255),1))
        world.permutationTable += world.permutationTable #combine for 512 values in permTable


    def fade(t): #fade/smoothstep Function
        return t ** 3 *(t * (t * 6 - 15) + 10)
    

    def lerp(a, b, t): #linear interpolation
        return a + t * (b - a)
    

    def getDotProduct(ix,iy,x,y):
        gradientIndex = world.permutationTable[world.permutationTable[ix % 256] + iy % 256] % len(world.gradients) #ensures pesudo-random number extraction
        gradient = world.gradients[gradientIndex]
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
    

    #print(len(world.gradients))


    # def Normalize(data,rOV):
    #     flatValues = [value for t in data for value in t]
    #     minVal = min(flatValues)
    #     maxVal = max(flatValues)
    #     normalizedData = [
    #         tuple(round((value - minVal) / (maxVal-minVal) * rOV) if maxVal != minVal else 0 for value in t)
    #         for t in data
    #     ]
    #     return normalizedData
    

    def getPerlin(scale,width,height,offsetX,offsetY): #generateRawPerlin
        noisemap = []
        for y in range(height):
            row = []
            for x in range(width):
                dotProduct = samplePerlinNoise((x+offsetX)/scale,(y+offsetY)/scale) #IMPORTANT! Scale factor tells you the length of chunk/gridcell!
                #print(y*height+x,int(x),int(y),int(x)+1,int(y)+1)
                row.append(dotProduct)
            noisemap.append(row)
        return noisemap
    

    octaves = [] #store octaves after production
    generatePermutationTable()
    for i in range(numberOfOctaves):
        octaves.append(getPerlin(scale/(2**i),width,height,offsetX,offsetY))
    fbmNoise = []
    for z in range(len(octaves[0])): #normalization: extracts values from tuples from list
        ztuple = []
        for y in range(len(octaves[0][0])):
            extractedElements = [val[z][y] for val in octaves]
            sumdps = 0
            for i,element in enumerate(extractedElements):
                sumdps += (element / (2**i))
            ztuple.append(int(sumdps*160+100))
        fbmNoise.append(tuple(ztuple)) #refine to original format
    noise = []
    noise = fbmNoise
        
    return noise




