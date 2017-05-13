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
        index = hash(str((shingle))) % rangeValue
        boolMat[index] = True

    return boolMat

def poweredHash(_input, _pow):
    output = hash(str(_input) + str(_pow))
    #if _pow > 1:
        #for i in range(1, _pow):
            #output = hash(str(output))
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
                index = poweredHash(b, i) % rangeValue
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
    
    return createSignature(bm, rangeValue)
    
    
