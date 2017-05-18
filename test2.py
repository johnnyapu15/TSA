#20170516 FST test_JJA

#1:1 비교에 대한 LSH 기초 테스트 완료.
#1:N 비교를 통해 적절한 결과가 나오는 지를 확인

import FST.minhash
import FST.shingle

fp1 = open("results/t2-1.txt", 'r') #Model
fp2 = open("results/t2-2.txt", 'r') #Field data

d1 = fp1.readlines()
d2 = fp2.readlines()

for i in range(len(d1)):
    d1[i] = int(d1[i])
    i += 1

for i in range(len(d2)):
    d2[i] = int(d2[i])
    i += 1

#우선 필드 데이터를 모델 사이즈만큼 슁글링
shData = FST.shingle.shingle(d2, len(d1))

sh1 = FST.shingle.shingle(d1, 9)
sig_Model = FST.minhash.minhash([sh1], 0)
sig_Data =list()

for d in shData:
        tmp = FST.shingle.shingle(d, 9)
        sig_Data.append(FST.minhash.minhash([tmp], 0))

testOutput = FST.minhash.LSH_1_N(sig_Model, sig_Data, 20)