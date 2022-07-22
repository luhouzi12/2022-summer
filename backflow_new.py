import copy
from fileinput import filename
import numpy as np

close = np.load(r'C:\xyz\npys\stock_quote\close.npy',allow_pickle= True)
dateMap = np.load(r'C:\xyz\npys\stock_quote\date_map.npy',allow_pickle= True)
codeMap = np.load(r'C:\xyz\npys\stock_quote\code_map.npy',allow_pickle= True)
zx1 = np.load(r'C:\xyz\npys\stock_quote\zx1.npy',allow_pickle= True)

# codeMap.index
closeM5 = np.delete(close, slice(5), 0)
for i in range(5):
    closeM5 = np.append(closeM5,[np.zeros(5600)], axis=0)


rawAlpha = close - closeM5
def deleteAndAppendRow(array):
    afterDelete = np.delete(array, 0, 0)
    return np.vstack(([np.zeros(len(array[0]))], afterDelete))

def dk5(alpha):
    alphaM1 = deleteAndAppendRow(alpha) * 4 / 15
    alphaM2 = deleteAndAppendRow(alphaM1) * 3 / 15
    alphaM3 = deleteAndAppendRow(alphaM2) * 2 / 15
    alphaM4 = deleteAndAppendRow(alphaM3) / 15
    res = alpha * 5 / 15 + alphaM1 + alphaM2 + alphaM3 + alphaM4
    nans = np.empty((4, len(alpha[0])))
    nans.fill(np.nan)
    res[slice(4)] = nans
    return res
alphaAfterDk5 = dk5(rawAlpha)
fileName = r'C:\xyz\temp\alphaAfterDk5'
np.save(fileName, alphaAfterDk5)

def neu(alpha, zx1):
    for rowIndex in range(len(zx1)):
        zx1CodeSet = set(zx1[rowIndex])
        for zx1Code in zx1CodeSet:
            indexList = np.where(zx1[rowIndex] == zx1Code)
            avgAlpha = sum(np.take(alpha[rowIndex], indexList)) / len(indexList)
            minusArray = np.zeros(len(zx1[rowIndex]))
            np.put(minusArray, indexList, avgAlpha)
            alpha[rowIndex] - minusArray
    return alpha
alphaAfterNeu = neu(alphaAfterDk5, zx1)

print(alphaAfterNeu[300][300])