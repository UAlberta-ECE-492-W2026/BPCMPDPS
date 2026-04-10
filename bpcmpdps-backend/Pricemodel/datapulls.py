from datetime import datetime
from pathlib import Path

import pandas as pd
import requests

from forecasting.build_training_dataset import fetch_open_meteo_hourly_history


def addnewrow(newrow):
  fieldnames = ['timestamp', 'Price', 'temperature_c', 'wind_speed_kph', 'humidity', 'feels_like_c', 'precipitation_mm']
  # Append to the CSV file
  newrow.to_csv('C:\\Users\\ktgar\\PycharmProjects\\BPCMPDPS\\bpcmpdps-backend\\Pricemodel\\data\\Price_weather_training.csv', mode='a', index=False, header=False)

def createnewrow(timestamp, Price):
  fieldnames = ['timestamp', 'Price', 'temperature_c', 'wind_speed_kph', 'humidity', 'feels_like_c', 'precipitation_mm']
  # replace with better output once timeing for price is found
  if Price=='':Price='0'
  latitude = 53.54087514959737
  longitude = -113.49119564477701
  start_date=datetime.today().date()
  end_date=datetime.today().date()
  timedate=datetime.strptime(timestamp,"%Y-%m-%d %H:%M:%S")
  time = int(timedate.strftime("%H"))

  weatherdata=fetch_open_meteo_hourly_history( latitude, longitude, start_date, end_date)
  weatherrow=weatherdata.iloc[time].to_frame().T
  weatherrow=weatherrow.drop(weatherrow.columns[0], axis=1)
  weather_inputs=weatherrow.iloc[0].tolist()

  inputs=[[timedate,float(Price)]+weather_inputs]
  newrow=pd.DataFrame(inputs,columns=fieldnames)

  return newrow

def createurl(startdate, enddate):
  url="https://apimgw.aeso.ca/public/poolprice-api/v1.1/price/poolPrice?startDate="+startdate+"&endDate="+enddate
  return url


def get_hourly_data(url):

  payload = {}
  headers = {
    'Accept': 'application/json',
    'API-KEY': '1b5f6b0772b04b6a9938bf67945157e5',
    'Cookie': 'AESO-Cookie=!iwl5czYM1DN1J7rkEGZ9zWXiVGb4KQcBgsnOMlbjj7B8sCFkBwmQQX+vYmho3D/dl9SjphtCTGtjQO0='
  }

  response = requests.request("GET", url, headers=headers, data=payload)

  return response.json()

  def natgasvalues():
    gasvalues = []

    return gasvalues


def getgasvalstocsv():
  url = "https://api.economicdata.alberta.ca/api/data?code=666e6195-c509-479b-b79f-b95e05536032"
  payload = {}
  headers = {}
  response = requests.request("GET", url, headers=headers, data=payload)
  jason=response.json()
  gasdf=pd.DataFrame(jason)
  output_dir = Path("data")
  output_dir.mkdir(parents=True, exist_ok=True)
  gasdf.to_csv(output_dir / "gasvals.csv", index=False)

def processgassvals():
  gasdf=pd.read_csv("C:\\Users\\ktgar\\PycharmProjects\\BPCMPDPS\\bpcmpdps-backend\\Pricemodel\\data\\gasvals.csv")
  gasdf=gasdf.drop(range(0,384))
  columnslist=gasdf.columns.tolist()
  gasdf=gasdf.drop(columns=columnslist[1])
  gasdf=gasdf.drop(columns=columnslist[2])
  columnslist = gasdf.columns.tolist()
  i=0
  #fixes index
  for index in gasdf.iterrows():
    index=i
    i=i+1

  # fixs T in string
  newgasdf = []
  for index,value in gasdf[columnslist[0]].items():
    newvalue=value.replace("T"," ")
    gasdf.at[index,columnslist[0]]=newvalue
  hrvales=['00:00:00','01:00:00','02:00:00','03:00:00','04:00:00','05:00:00','06:00:00','07:00:00','08:00:00','09:00:00','10:00:00','11:00:00','12:00:00','13:00:00','14:00:00','15:00:00','16:00:00','17:00:00','18:00:00','19:00:00','20:00:00','21:00:00','22:00:00','23:00:00']
  #creates new matrix with row index of the system
  for row in gasdf.itertuples():
    value=row[1]
    newdt=[]
    newvalue=value.split()
    for item in hrvales:
      newdt.append(newvalue[0]+" "+item)
    for item in newdt:
      newitem=datetime.strptime(item,"%Y-%m-%d %H:%M:%S")
      newrow=(newitem, row[2])
      newgasdf.append(newrow)
  newgasdf.pop(0)
  newgasdf=pd.DataFrame(newgasdf, columns=[columnslist[0],"NatGas_price_$perkj"])
  gasdf=newgasdf
  # for later renaming of gasdf
  glcolumnslist = gasdf.columns.tolist()

  gasdf.rename(columns={glcolumnslist[0]: "timestamp"}, inplace=True)
  output_dir = Path("data")
  output_dir.mkdir(parents=True, exist_ok=True)
  gasdf.to_csv(output_dir /"gasvals.csv", index=False)


def get_hourly_price():
  start=datetime.now()
  formateddate=start.strftime("%Y-%m-%d")
  url=createurl(formateddate, formateddate)
  json=get_hourly_data(url)
  time=int(start.strftime("%H"))
  time-=1
  return json['return']['Pool Price Report'][time+1]['begin_datetime_mpt']+':00',json['return']['Pool Price Report'][time]['pool_price']

def getandaddnewrow(startdate, enddate):
  startdate,price=get_hourly_price()
  newrow=createnewrow(startdate,price)
  addnewrow(newrow)

if __name__=="__main__":
  getgasvalstocsv()
  processgassvals()
