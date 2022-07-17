from cmath import nan
from datetime import date
import pandas as pd
csvContent = pd.read_csv(r'C:\xyz\quote_test\2022\01\quote_20220114.csv')
total = 0
dict1 = {'a': 1.5, 'b': 2}
dict2 = {'a': 5, 'b': 3}
df = pd.DataFrame([dict1, dict2])
print(type(df.corr()))
# for returns in csvContent['RETURNS:10']:
#     if returns == returns:
#         total = total + float(returns)
# print(total)

# a = {'a':1.3, 'b':-2.4}
# b = [{'a':1}, {'a':3,'b':5}]
# for value in a.values():
#     print(type(0.1))
# print(type(a.values()[0]))
# print(len(b))
# print(max(map(abs, a.values())))
# lines = stContent[stContent['S_INFO_WINDCODE:0'].isin(['000518.SZ'])]
# print(lines.loc[lines.index[0]]['ENTRY_DT:2'])
# print(stContent['S_INFO_WINDCODE:0'].str.contains('000518.SZ'))
# print('000558.SZ' in str(stContent['S_INFO_WINDCODE:0']))
# stStockCodeList = []
# for index in stContent.index:
#     stStockCodeList.append(stContent.loc[index][0])
# def convertStringToDate(dateNumber):
#     if dateNumber != dateNumber:
#         return date.today()
#     dateString = str(dateNumber)
#     year = int(dateString[:4])
#     month = int(dateString[4:6])
#     day = int(dateString[6:8])
#     return date(year, month, day)


# def getAvailableStocks(csvContent):
#     for index in csvContent.index:
#         stockCode = csvContent.loc[index][1]
#         if stockCode in stStockCodeList:
#             stIndexs = [i for i,x in enumerate(stStockCodeList) if x==stockCode]
#             Tdate = convertStringToDate(csvContent.loc[index][0])
#             for stIndex in stIndexs:
#                 entryDate = convertStringToDate(stContent.loc[stIndex][2])
#                 endDate = convertStringToDate(stContent.loc[stIndex][3])
#                 if Tdate < endDate and Tdate > entryDate:
#                     csvContent.drop(index=index,inplace=True)
#     return csvContent
# csvTest = pd.read_csv(r'C:\xyz\quote\2017\02\quote_20170210.csv')
# print(getAvailableStocks(csvTest).index)