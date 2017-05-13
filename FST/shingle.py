#20170512~ JJA





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
