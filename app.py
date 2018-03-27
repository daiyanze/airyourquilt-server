from flask import Flask, request, jsonify
from flask_cors import CORS
from forecastiopy import *

app = Flask(__name__)
CORS(app)

SECRET_KEY = 'af1dd67f02165446b1427f3ca8323d12'

@app.route('/')
def home():
  return 'running'

@app.route('/weather', methods=['GET'])
def getWeather():
  ts = request.args.get('time')
  latitude = request.args.get('latitude')
  longitude = request.args.get('longitude')
  params = {}
  if ts:
    params['time'] = ts
  if latitude:
    params['latitude'] = latitude
  if longitude:
    params['longitude'] = longitude

  fio = forcast(**params)
  daily = fio.get_daily()
  res = {
    'windSpeed': daily['data'][0]['windSpeed'],
    'temperatureHigh': daily['data'][0]['temperatureHigh'],
    'temperatureLow': daily['data'][0]['temperatureLow'],
    'average_temperature': (
      daily['data'][0]['temperatureHigh'] + daily['data'][0]['temperatureLow']
      ) / 2,
    'humidity': daily['data'][0]['humidity'],
    'timezone': fio.timezone
  }
  print(fio.get_url())
  return jsonify(res)

def forcast(latitude=35.68, longitude=139.76, time=None):
  fio = ForecastIO.ForecastIO(SECRET_KEY,
          units=ForecastIO.ForecastIO.UNITS_SI,
          latitude=latitude, longitude=longitude, time=time)

  return fio


if __name__ == '__main__':
  app.run()

