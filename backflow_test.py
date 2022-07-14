import copy
from datetime import date
import pandas as pd
import numpy as np
import warnings
import os
warnings.filterwarnings("ignore") #狗狗
basePath = r'C:\xyz\quote_test'
stockCodeColumnIndex = 1
preCloseColumnIndex = 2
closeColumnIndex = 6

stContent = pd.read_csv(r'C:\xyz\st.csv')
industryContent = pd.read_csv(r'C:\xyz\zx_industry.csv')
yearList = [2022]

stStockCodeList = []
for index in stContent.index:
    stStockCodeList.append(stContent.loc[index][0])
industryCodeStockCodeListdict = {}
for index in industryContent.index:
    stockCode = industryContent.loc[index][0]
    industryCode = industryContent.loc[index][3]
    if industryCode not in industryCodeStockCodeListdict.keys():
        industryCodeStockCodeListdict[industryCode] = []
    industryCodeStockCodeListdict[industryCode].append(stockCode)
print(industryCodeStockCodeListdict)

def readCsv (fileName):
    return pd.read_csv(fileName)

def convertStringToDate(dateNumber):
    if dateNumber != dateNumber:
        return date.today()
    dateString = str(dateNumber)
    year = int(dateString[:4])
    month = int(dateString[4:6])
    day = int(dateString[6:8])
    return date(year, month, day)


def getAvailableStocks(csvContent):
    resultCsvContent = copy.deepcopy(csvContent)
    for index in csvContent.index:
        stockCode = csvContent.loc[index][stockCodeColumnIndex]
        if stockCode in stStockCodeList:
            stIndexs = [i for i,x in enumerate(stStockCodeList) if x==stockCode]
            Tdate = convertStringToDate(csvContent.loc[index][0])
            for stIndex in stIndexs:
                entryDate = convertStringToDate(stContent.loc[stIndex][2])
                endDate = convertStringToDate(stContent.loc[stIndex][3])
                if Tdate < endDate and Tdate > entryDate and index in resultCsvContent.index:
                    resultCsvContent.drop(index=index,inplace=True)
    return resultCsvContent
    
# basePath = r'C:\Users\xyz\Desktop\202207\data\stock_quote\quote'

def generateAvailableCsvContentFilePathList():
    yearPathList = []
    for year in yearList:
        yearPath = basePath + '\\' + str(year)
        yearPathList.append(yearPath)
    monthPathList = []
    for yearPath in yearPathList:
        thisYearMonthPathList = os.listdir(yearPath)
        for monthPath in thisYearMonthPathList:
            monthPathList.append(yearPath + '\\' + monthPath)
    csvPathList = []
    for monthPath in monthPathList:
        for fileName in os.listdir(monthPath):
            csvPathList.append(monthPath + '\\' + fileName)
    resultCsvPathList = copy.deepcopy(csvPathList)
    for csvPath in csvPathList:
        csvContent = readCsv(csvPath)
        if len(csvContent) == 0:
            resultCsvPathList.remove(csvPath)
    return resultCsvPathList

def generate5dr(csvFilePathList):
    for csvFilePath in csvFilePathList:
        if csvFilePathList.index(csvFilePath) > 5:
            TCsvContent = readCsv(csvFilePath) # Today's CSV content
            availableTCsvContent = getAvailableStocks(TCsvContent) # filter out st stocks
            TStockCodeAlphaRawDict = {}
            TM5CsvFilePath = csvFilePathList[csvFilePathList.index(csvFilePath) - 5]
            TM5CsvContent = readCsv(TM5CsvFilePath) # T-5 's CSV Content
            for index in availableTCsvContent.index: # loop today's available stocks
                stockCode = availableTCsvContent.loc[index][stockCodeColumnIndex]
                stockTClose = availableTCsvContent.loc[index][closeColumnIndex] # close
                # f.loc[df['column_name'] == some_value]
                stockLinesInTM5 = TM5CsvContent[TM5CsvContent['S_INFO_WINDCODE:1'].isin([str(stockCode)])]
                if len(stockLinesInTM5):
                    TM5Close = stockLinesInTM5.loc[stockLinesInTM5.index[0]]['S_DQ_CLOSE:6']
                    TStockCodeAlphaRawDict[stockCode] = stockTClose - TM5Close
            TStockCodeAlphaRawDictList.append(TStockCodeAlphaRawDict)
    return

csvFilePathList = generateAvailableCsvContentFilePathList()
TStockCodeAlphaRawDictList = []
for csvFilePath in csvFilePathList:
    if csvFilePathList.index(csvFilePath) > 5:
        # TDate = csvFilePath[]
        TCsvContent = readCsv(csvFilePath) # Today's CSV content
        availableTCsvContent = getAvailableStocks(TCsvContent) # filter out st stocks
        TStockCodeAlphaRawdict = {}
        TM5CsvFilePath = csvFilePathList[csvFilePathList.index(csvFilePath) - 5]
        TM5CsvContent = readCsv(TM5CsvFilePath) # T-5 's CSV Content
        for index in availableTCsvContent.index: # loop today's available stocks
            stockCode = availableTCsvContent.loc[index][stockCodeColumnIndex]
            stockTClose = availableTCsvContent.loc[index][closeColumnIndex] # close
            stockLinesInTM5 = TM5CsvContent[TM5CsvContent['S_INFO_WINDCODE:1'].isin([str(stockCode)])]
            if len(stockLinesInTM5):
                TM5Close = stockLinesInTM5.loc[stockLinesInTM5.index[0]]['S_DQ_CLOSE:6']
                TStockCodeAlphaRawdict[stockCode] = stockTClose - TM5Close
        TStockCodeAlphaRawDictList.append(TStockCodeAlphaRawdict)

def neu(stockCodeAlphaRawdict):
    for industryCode in industryCodeStockCodeListdict.keys():
        stockCodeList = industryCodeStockCodeListdict[industryCode]
        stockCodeInCurrentIndustryAlphadictList = list(filter(lambda stockCode: stockCode in stockCodeList, stockCodeAlphaRawdict))
        currentIndustryAlphas = []
        for stockCode in stockCodeInCurrentIndustryAlphadictList:
            currentIndustryAlphas.append(stockCodeAlphaRawdict[stockCode])
        avgAlpha = sum(currentIndustryAlphas) / len(currentIndustryAlphas)
        for stockCode in stockCodeInCurrentIndustryAlphadictList:
            stockCodeAlphaRawdict[stockCode] = stockCodeAlphaRawdict[stockCode] - avgAlpha

def dk5(stockCodeAlphaRawdictList):
    for stockCodeAlphaRawdict in stockCodeAlphaRawdictList:
        TIndex = stockCodeAlphaRawdictList.index(stockCodeAlphaRawdict)
        if TIndex >= 4:
            dropStockCodeList = []
            for stockCode in stockCodeAlphaRawdict.keys():
                available = True
                for i in range(5):
                    if stockCode not in stockCodeAlphaRawdictList[TIndex - i].keys():
                        available = False
                if available:
                    stockCodeAlphaRawdict[stockCode] = (5 * stockCodeAlphaRawdict[stockCode] + 4 * stockCodeAlphaRawdictList[TIndex - 1][stockCode] + 3 * stockCodeAlphaRawdictList[TIndex - 2][stockCode] + 2 * stockCodeAlphaRawdictList[TIndex - 3][stockCode] + stockCodeAlphaRawdictList[TIndex - 4][stockCode]) / (1 + 2 + 3 + 4 + 5)
                else:
                    dropStockCodeList.append(stockCode)
            for stockCode in dropStockCodeList:    
                stockCodeAlphaRawdict.pop(stockCode)
        
def powrank(stockCodeAlphaRawdict):
    sortedDict = dict(sorted(stockCodeAlphaRawdict.items(), key=lambda item: item[1]))
    for stockCode in sortedDict.keys():
        sortedDict[stockCode] = list(sortedDict.keys()).index(stockCode)**2
    maxAbsAlpha = max(map(abs, sortedDict.values()))
    for stockCode in sortedDict.keys():
        sortedDict[stockCode] = sortedDict[stockCode] / maxAbsAlpha
    avgAlpha = sum(sortedDict.values()) / len(sortedDict)
    for stockCode in sortedDict.keys():
        sortedDict[stockCode] = sortedDict[stockCode] - avgAlpha
    return sortedDict

for stockCodeAlphaRawdict in TStockCodeAlphaRawDictList:
    neu(stockCodeAlphaRawdict)
dk5(TStockCodeAlphaRawDictList)
for index in range(len(TStockCodeAlphaRawDictList)):
    TStockCodeAlphaRawDictList[index] = powrank(TStockCodeAlphaRawDictList[index])
def calculateReturn(stockCodeAlphaDict, csvContent):
    stockCodeReturnDict = {}
    for stockCode in stockCodeAlphaDict.keys():
        stockLineInCsvContent = csvContent[csvContent['S_INFO_WINDCODE:1'].isin([str(stockCode)])]
        TReturn = stockLineInCsvContent.loc[stockLineInCsvContent.index[0]]['RETURNS:10']
        stockCodeReturnDict[stockCode] = stockCodeAlphaDict[stockCode] * TReturn
    return stockCodeReturnDict
stockCodeReturnDictList = []
for index in range(len(TStockCodeAlphaRawDictList)):
    stockCodeReturnDictList.append(calculateReturn(TStockCodeAlphaRawDictList[index], readCsv(csvFilePathList[index + 6])))
dailyReturnList = []
for stockCodeReturnDict in stockCodeReturnDictList:
    dailyReturnList.append(sum(stockCodeReturnDict.values()))
print(dailyReturnList)

# IR IC return rate huanshoulv BPMG bodonglv zuidahuiche
# zhengti/fennian

# TCsv = readCsv(r'C:\Users\xyz\Desktop\202207\data\stock_quote\quote\2022\01\quote_20220112.csv')

# print(TCsv)