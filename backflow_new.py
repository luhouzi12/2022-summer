import numpy as np


dateMap = np.load(r'C:\xyz\npys\stock_quote\date_map.npy',allow_pickle= True)  

startDate = 20100101
endDate = 20220701

dateIndexs = ((dateMap >= startDate) & (dateMap <= endDate))
datePeriod = dateMap[dateIndexs]

close = np.load(r'C:\xyz\npys\stock_quote\close.npy',allow_pickle= True)[dateIndexs]
zx1 = np.load(r'C:\xyz\npys\stock_quote\zx1.npy',allow_pickle= True)[dateIndexs]
returns = np.load(r'C:\xyz\npys\stock_quote\return.npy',allow_pickle= True)[dateIndexs]
exst = np.load(r'C:\xyz\npys\stock_quote\EXST.npy',allow_pickle= True) [dateIndexs]

closeM5 = np.delete(close, slice(5), 0)
for i in range(5):
    closeM5 = np.append(closeM5,[np.zeros(5600)], axis=0)


exst= np.where(exst==0, np.nan, exst)

rawAlpha = close - closeM5
rawAlpha = rawAlpha * exst

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

arrWithoutNanArray = []
def powrank(alpha):
    arrAfterSort = np.sort(alpha, axis = 1) 
    for rowIndex in range(4,len(alpha)):
        arrWithoutNanArray.append(np.array(np.where(alpha[rowIndex] == alpha[rowIndex])).flatten())
        alpha[rowIndex] = np.searchsorted(arrAfterSort[rowIndex], alpha[rowIndex][:]) **2
    return alpha
alphaAfterPowrank = powrank(alphaAfterNeu)
arrWithoutNanArray = np.array(arrWithoutNanArray)


def normalizeAlpha(alphaRow, notNanIndexs):
    alphaRow = (alphaRow - sum(alphaRow[notNanIndexs]) / len(alphaRow[notNanIndexs])) / sum(abs(alphaRow[notNanIndexs]))
    return alphaRow

alphaAfterNormalization = np.empty(alphaAfterPowrank.shape)

for rowIndex in range(4,len(alphaAfterPowrank)):
    alphaAfterNormalization[rowIndex] = normalizeAlpha(alphaAfterPowrank[rowIndex], arrWithoutNanArray[rowIndex - 4])


def calcReturn(alpha, returns):
    returnArray = alpha * returns
    returnList = []
    for rowIndex in range(4,len(returnArray)):
        arrWithoutNan = returnArray[rowIndex][~np.isnan(returnArray[rowIndex])]
        returnList.append(sum(arrWithoutNan))
    return returnList
returnList = calcReturn(alphaAfterNormalization, returns)
totalRet = sum(returnList)
totalRetList = []
for index in range(len(returnList)):
    totalRetList.append(sum(returnList[:index]))

maxDrawDown = (max(totalRetList) - min(totalRetList))

def calcRankIc(alphaRow, returnsRow, withoutNanIndexArr):
    corr = np.correlate(alphaRow[withoutNanIndexArr], returnsRow[withoutNanIndexArr])[0]
    return corr

rankIcList = []
for rowIndex in range(4,len(alphaAfterNormalization) - 1):
    ic = calcRankIc(alphaAfterNormalization[rowIndex], returns[rowIndex + 1], arrWithoutNanArray[rowIndex - 4])
    rankIcList.append(ic)
rankIcArr = np.array(rankIcList)

def calculateIR(icList):
    noNanRankIcArr = icList[~np.isnan(icList)]
    return (sum(noNanRankIcArr) / len(noNanRankIcArr)) / noNanRankIcArr.std()
IR = calculateIR(rankIcArr)

def calcTakeOverRate(alphaRow, withoutNanIndexArr):
    return sum(abs(alphaRow[withoutNanIndexArr]))

TVR = []
for rowIndex in range(4,len(alphaAfterNormalization)):
    TVR.append(calcTakeOverRate(alphaAfterNormalization[rowIndex],arrWithoutNanArray[rowIndex - 4]))

print('max draw down: ' + str(maxDrawDown))
print('total return: ' + str(totalRet))
print('ICList: ' + str(rankIcList))
print('IR: ' + str(IR))
print('TVR: ' + str(TVR))
