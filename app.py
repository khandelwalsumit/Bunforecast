import pandas as pd
import numpy as np
import json
import plotly
import plotly.express as px
from fbprophet import Prophet
from datetime import datetime,date,timedelta

import plotly.express as px
from flask import Flask, render_template, request, redirect, url_for, session, flash,Response
import customFunc

###############################################################################
# SQL server details
###############################################################################
appData = {}

app = Flask(__name__)
app.secret_key = 'Bunforecast'
app.debug = False
###############################################################################
# getting data 
###############################################################################




###############################################################################
# flask routes
###############################################################################
## app logic
@app.route("/")
def index():
    global appData
    appData = {}
    return render_template("index.html", appData=appData)


@app.route("/runModel", methods = ['GET','POST'])
def runModel():
    global appData
    store = request.form['store']
    fcastDays = request.form['fcastDays'] #2021-08-01
    startDate = datetime.strptime(request.form['startDate'],'%Y-%m-%d')
    startDate = datetime(startDate.year, startDate.month, startDate.day)
    endDate = startDate + timedelta(days=int(fcastDays)+1)

    forecast = customFunc.getForecast(store,fcastDays,startDate,endDate)
    
    baseFcast = forecast[['ds','yhat']]
    baseFcast.columns = ['Date','Forecast']
    baseFcast = baseFcast.groupby(baseFcast.Date.dt.date).sum().reset_index()

    fig = px.line(baseFcast, x='Date', y='Forecast')
    fig.update_layout(title = store+' forecast for next '+fcastDays+' days', xaxis_title='Forecast Horizon', yaxis_title='Sales')

    # fig = px.scatter(forecast, x='Date', y='Forecast')

    appData['store'] = store
    appData['fcastDays'] = fcastDays
    appData['startDate'] = startDate

    finalForecast = customFunc.formatForecast(forecast)
    appData['forecast'] = finalForecast

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    appData['graphJSON'] = graphJSON

    return render_template("index.html", appData=appData)



@app.route("/downloadData")
def downloadData():
    return Response(
       appData['forecast'].to_csv(index=False),
       mimetype="text/csv",
       headers={"Content-disposition":"attachment; filename="+appData['store']+"_"+appData['fcastDays']+"Days_Forecast.csv"}
    )

###############################################################################
# run app
###############################################################################
if __name__ == "__main__":
    app.run()



