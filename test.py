#20170512 TEST FOR FST



import FST.shingle
import FST.minhash

fp1 = open("results/t1.txt", 'r')
fp2 = open("results/t2.txt", 'r')

d1 = fp1.readlines()
d2 = fp2.readlines()
i = 0
for i in range(len(d1)):
    d1[i] = int(d1[i])
    d2[i] = int(d2[i])
    i += 1

sh1 = FST.shingle.shingle(d1, 9)
sh2 = FST.shingle.shingle(d2, 9)

shList = list()
shList.append(sh1)
shList.append(sh2)

sig = FST.minhash.minhash(shList, 0)

print(FST.minhash.calcSim(sig[0], sig[1]))