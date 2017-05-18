#20170518 JJA Improved LSH for analysing time series

##### Shingling length of data into shingling size
def shingle(_data, _sh_size):
    shingled = list()
    for i in range(0, len(_data) - _sh_size + 1):
        shingled.append(_data[i:i + _sh_size])
    return shingled


##### 2차원 벡터 데이터를 1차원 벡터 데이터로 변환, 반환.
def unifying(_data, _outputName):
    if _outputName != "":
        outputName = _outputName
    else :
        outputName = 'unified_' + _data[0]

    r = len(_data)
    for i in range(0, r):
        _data[i] = _data[i].split()

    n = len(_data[0])
    output = list()

    for i in range(0, n):
        for l in _data:
            output.append(l[i])
    return output        
    

def tokenize(_data):
    output = list()
    for i in range(0, len(_data)):
        output.append(hash(_data[i]))
    return output

#20170513 JJA

#간소화된 민해싱. 


RANGE = 30000
HASHCOUNT = 100

#input으로 한 document의 shingles을 받고,
#기본해시를 이용해 boolean matrix를 생성한다.
def createBoolMat(_shingles, _range):
    if _range != 0:
        rangeValue = _range
    else:
        rangeValue = RANGE

    boolMat = [False] * rangeValue
    for shingle in _shingles:
        index = hashFunc(sum(shingle), 1) % rangeValue
        boolMat[index] = True

    return boolMat

def hashFunc(_input, _pow):
    #output = int(str(_input) + str(_pow))
    #output = _input + _pow*7
    #if _pow > 1:
        #for i in range(1, _pow):
            #output = hash(str(output))
    poly = 0xEDB88320
    output = 0
    inp = str(_input)
    poly += _pow
    for i in range(len(inp)):
        output = output * poly + int(inp[i])
    return output
#
#여러 documents의  boolean matrice(hashed shingles)를 받아서
#주어진 해시함수 내의 signature를 반환한다.
#이때 hashed shingles는 2차원 벡터 데이터이다.
def createSignature(_boolMats, _range):
    if _range != 0:
        rangeValue = _range
    else:
        rangeValue = RANGE
    
    #input parameter _hashedList is constructed by 
    #a row = a document , a column = a booleaned shingle of that document
    ##range = column number

    ###CREATE SIGNATURE WITH POWERED HASH FUNCTION
    signature = [[0]*HASHCOUNT for i in range(len(_boolMats))]
    for i in range(0, HASHCOUNT):
        for d in range(0, len(_boolMats)):
           # signature = [0] * HASHCOUNT
            minimum = RANGE + 1
            for b in range(0, rangeValue):
                index = hashFunc(b, i) % rangeValue
                if _boolMats[d][index] == True:
                    if minimum > index:
                        minimum = index
            signature[d][i] = minimum
            
    return signature           


#Calculate similarity of two documents
def calcSim(_sig1, _sig2):
    #row : number of hash funcs
    n = len(_sig1)
    andc = 0

    for i in range(n):
        if _sig1[i] == _sig2[i]:
            andc += 1

    return andc/n

#minhash

def minhash(_data, _range):
    if _range != 0:
        rangeValue = _range
    else:
        rangeValue = RANGE
    #number of documents
    n = len(_data)
    bm = list()
    
    for i in range(0, n):
        bm.append(createBoolMat(_data[i], rangeValue))
    output = createSignature(bm, rangeValue)
    if n == 1:
        return output[0]
    else:
        return output
    
#1:N
def LSH_1_N(_model, _data, _b):
    doc_Count = len(_data)
    output = [False] * doc_Count
    #band = [[False] * HASHCOUNT for i in range(_b)]
    j = -1
    band = [True] * doc_Count
    
    for i in range(HASHCOUNT):
        j += 1
        #Every start point of band...
        if j == _b:
            #OR LSH
            for o in range(doc_Count):
                output[o] = output[o] | band[o] 
            band = [True] * doc_Count
            j = 0
        hashedM = hashFunc(_model[i], i)
        #AND LSH
        for o in range(doc_Count):
            if band[o] == True:
                band[o] = band[o] & (hashedM == hashFunc(_data[o][i], i))
        
    return output