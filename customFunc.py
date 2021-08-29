import pickle
import numpy as np


def getForecast(store,fcastDays,startDate,endDate):
    model = pickle.load(open('model/'+store+'.sav', 'rb'))
    fcastHorizon = int(fcastDays) + 31
    future = model.make_future_dataframe(periods=fcastHorizon * 24,freq='h',include_history=False)
    future = future[(future['ds'].dt.hour > 9) & (future['ds'].dt.hour <= 20)]
    forecast = model.predict(future)

    forecast = forecast[['ds','yhat']]
    forecast = forecast[forecast['ds'] >= startDate]
    forecast = forecast[forecast['ds'] <= endDate]
    forecast['yhat'] = np.where(forecast['yhat']<0,0,forecast['yhat'])
    return forecast

def formatForecast(forecast):
    finalForecast = forecast[['ds','yhat']]
    finalForecast['date'] = finalForecast.ds.dt.date
    finalForecast['time'] = finalForecast.ds.dt.time
    finalForecast = finalForecast[['date','time','yhat']]
    finalForecast.columns = ['Date','Time','Forecast']
    return finalForecast