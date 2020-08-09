import requests
import csv
import json
import pandas as pd
from pandas import DataFrame as df
import datetime

import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px
pio.renderers.default='browser'

JSON_URL = 'https://api.covid19india.org/v5/min/timeseries-MH.min.json'


dist_name  = []
covidData =[]
covidRec = []
covidDeath = []


dtcolNames =[]

req = requests.get(JSON_URL)



distNames = df(req.json()['MH']['districts'])
distNames = distNames.T

for dis in distNames.index:
    dist_name.append(dis)

dates = df(req.json()['MH']['districts'][dist_name[0]])
for dt in dates.index:
    dtcolNames.append(dt + ",")




for dist  in dist_name:   
  
    if not 'Other State' in dist:
        i=0
        #covidData.append('\n')

       
        
        covid = df(req.json()['MH']['districts'][dist])
        
                
        for conf, dt in zip(covid.dates, covid.index):
            month_str = dt            
            month_obj = datetime.datetime.strptime(month_str, '%Y-%m-%d')
            month = month_obj.ctime().split(' ')[1]
            
            dt = dt + ","
            i+=1
            index = dtcolNames.index(dt) + 1
            if i!= index:
                #print("city:" +  dist + ":" + dt + ": Ind:" + str(index) + ": i :" + str(i))
                for n in range(index-1):
                    covidData.append(dist + "," + dt + month + "," + "0," + "0,"+ "0" + '\n')
            
                i = index
            for t in conf.keys():
                if 'total' in t:
                    if 'confirmed' in (conf['total'].keys()):
                        covidData.append(dist + "," + dt + month + "," + str(conf['total']['confirmed']) + ",")
                    if not 'confirmed' in (conf['total'].keys()):
                        covidData.append(dist + "," + dt + month + "," + "0,")
                    
                    if 'recovered' in (conf['total'].keys()):
                        covidData.append(str(conf['total']['recovered'])+ ",")
                    if not 'recovered' in (conf['total'].keys()):
                        covidData.append("0,")
                      
                    if 'deceased' in (conf['total'].keys()):
                        covidData.append(str(conf['total']['deceased']) + '\n')
                    if not 'deceased' in (conf['total'].keys()):
                        covidData.append("0" + '\n')
                        
                    
                        
# TODO: Delta and no of tests
                                
   
with open('test.csv', 'w') as f:
   
    f.writelines('City,'+ 'Date,' + 'Month,' + 'Confirmed,' + 'Recovered,' + 'Deceased')
    f.writelines("\n")
    f.writelines(covidData)
    

df1=pd.read_csv('test.csv')
fig = go.Figure(px.scatter(df1, x ='Confirmed', y = 'Deceased' , animation_frame = 'Date', animation_group = 'City',
           color = 'City', size = 'Confirmed', size_max = 80,hover_name = 'City',
           hover_data=['Date','Confirmed', 'Recovered', 'Deceased'],
           log_x = True,log_y = True, range_x = [10, 1000000], range_y  = [10, 100000]))

fig.update_layout(
    title={
        'text': '<b>Covid19 plot for Cities of Maharashtra</b>',
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
      },
    xaxis_title="Confirmed Cases",
    yaxis_title="Death toll",
    legend_title="Legend Title",
    font=dict(
        family="Courier New, monospace",
        size=12,
        color="RebeccaPurple"
    ))

fig.show()