import clr
clr.AddReference(r"C:\Program Files (x86)\PIPC\AF\PublicAssemblies\4.0\OSIsoft.AFSDK")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 

from OSIsoft import AF
from OSIsoft.AF import *
import datetime as datetime
import statsmodels.api as sm
from pandas import Series
#DATABASE BAĞLANTISI
piDB = AF.PI.PIServers().DefaultPIServer
piPoint = AF.PI.PIPoint.FindPIPoint(piDB,"BA:TEMP.1")

#EĞİTİM VERİLERİ ZAMAN DİLİMİ
startTime = AF.Time.AFTime("2018-08-07 22:00:00")
endTime = AF.Time.AFTime("2018-08-08 9:00:00") 
timeRange = AF.Time.AFTimeRange(startTime, endTime)
#VERİLERİN ARALIĞI
span = AF.Time.AFTimeSpan.Parse("1m")


#TAHMİN VERİLERİ
startPredictTime = AF.Time.AFTime("2018-08-08 9:00:00")
sp = datetime.datetime.strptime(startPredictTime.LocalTime.ToString(), '%m/%d/%Y %I:%M:%S %p')
endPredictTime = AF.Time.AFTime("2018-08-08 17:00:00")
ep = datetime.datetime.strptime(endPredictTime.LocalTime.ToString(),'%m/%d/%Y %I:%M:%S %p')

'''
#EĞİTİM VERİLERİ
startTime = AF.Time.AFTime("*-9h")
endTime = AF.Time.AFTime("*")
timeRange = AF.Time.AFTimeRange(startTime, endTime)
#VERİLERİN ARALIĞI
span = AF.Time.AFTimeSpan.Parse("1m")
#TAHMİN VERİLERİ
startPredictTime = AF.Time.AFTime("*")
sp = datetime.datetime.strptime(startPredictTime.LocalTime.ToString(), '%m/%d/%Y %I:%M:%S %p')
endPredictTime = AF.Time.AFTime("*+9h")
ep = datetime.datetime.strptime(endPredictTime.LocalTime.ToString(),'%m/%d/%Y %I:%M:%S %p')

'''

#EĞİTİM VERİLERİNİN ÇEKİLMESİ
recordedValues = piPoint.InterpolatedValues(timeRange,span, "",False)

recordedValuesDict = dict()
#EĞİTİM VERİLERİNİN DİCTİONARY'e ATILMASI
for event in recordedValues:
    dt = datetime.datetime.strptime(event.Timestamp.LocalTime.ToString(),'%m/%d/%Y %I:%M:%S %p')
    recordedValuesDict[dt] = event.Value
    
#EĞİTİM VERİLERİNDEN OLUŞAN DATAFRAME'in OLUŞTURULMASI
df = pd.DataFrame(recordedValuesDict.items(),columns=["TimeStamp","Value"])
df['TimeStamp'] = pd.to_datetime(df['TimeStamp'])
indexed_df = df.set_index(['TimeStamp']).sort_index()
#EĞİTİM VERİLERİNİN GRAFİK GÖSTERİMİ
plt.plot(indexed_df)


#REGRESYON
ar_model = sm.tsa.AR(indexed_df)
pandas_ar_res = ar_model.fit(maxlag=200,method='cmle', disp=-1)

#TAHMİN
pred = pandas_ar_res.predict(start=str(sp) , end=str(ep))
#TAHMİN VERİLERİNİN GRAFİK GÖSTERİMİ
plt.plot(pred)
plt.show()
'''
#TAHMİN VERİLERİNİN CSV DOSYASI HALİNE GETİRİLMESİ
import csv
prediction = pd.DataFrame(pred,columns = ['predictions']).to_csv('prediction.csv')

with open('prediction.csv') as File:
    reader = csv.reader(File)
    for row in reader:
        print(row)
'''        
#TAHMİN VERİLERİNİN PI DATA ARCHİVE'e KAYDEDİLMESİ

#DATABASE BAĞLANTISI
piPointPredict = AF.PI.PIPoint.FindPIPoint(piDB,"BA:Temp.1_Future")

#TAHMİN VERİLERİNİN DATAFRAME'den AFVALUE'a DÖNÜŞTÜRMEK
newValues = AF.Asset.AFValues()

#TIMESTAMP ve VALUE'ların ayarlanması
for index,value in enumerate(pred):
    newValue = AF.Asset.AFValue()
    newValue.Timestamp = AF.Time.AFTime(pred.index[index].strftime('%m/%d/%Y %I:%M:%S %p'))
    newValue.Value = float(value)
    newValues.Add(newValue)

updateOption = AF.Data.AFUpdateOption.InsertNoCompression
bufferOption = AF.Data.AFBufferOption.BufferIfPossible
piPointPredict.UpdateValues(newValues, updateOption, bufferOption)

startTime_deviation = AF.Time.AFTime("2018-08-08 09:00:00")
endTime_deviation = AF.Time.AFTime("2018-08-08 17:00:00") 
timeRange_deviation = AF.Time.AFTimeRange(startTime_deviation, endTime_deviation)

recordedValues_deviation = piPoint.InterpolatedValues(timeRange_deviation,span, "",False)

recordedValuesDict_deviation = dict()
#EĞİTİM VERİLERİNİN DİCTİONARY'e ATILMASI
for event in recordedValues_deviation:
    dt = datetime.datetime.strptime(event.Timestamp.LocalTime.ToString(),'%m/%d/%Y %I:%M:%S %p')
    recordedValuesDict_deviation[dt] = event.Value

df_deviation = pd.DataFrame(recordedValuesDict_deviation.items(),columns=["TimeStamp","Value"])
df_deviation['TimeStamp'] = pd.to_datetime(df_deviation['TimeStamp'])
indexed_df_deviation = df_deviation.set_index(['TimeStamp']).sort_index()
#EĞİTİM VERİLERİNİN GRAFİK GÖSTERİMİ
plt.plot(indexed_df)
plt.plot(pred)
plt.plot(indexed_df_deviation)

preddf = Series.to_frame(pred)
preddf_array = preddf.values

indexed_df_deviation_array = indexed_df_deviation.values


#for i in range(0,len(indexed_df_deviation_array)):
#    mean = (indexed_df_deviation_array[i]+preddf_array[i])/2
#    ortDev = (abs(indexed_df_deviation_array[i]-mean) + abs(preddf_array[i]-mean))/2
#    hataPayi = ortDev*100/mean
#    print(i,hataPayi)
print('----------------------------------------------')
for i in range(0,len(indexed_df_deviation_array)):
    print(i,(abs(indexed_df_deviation_array[i]-preddf_array[i]))/indexed_df_deviation_array[i])
        
        
    

        
