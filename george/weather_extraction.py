from src.config import WEATHER_API_KEY
import requests
import json
from calendar import monthrange
import pandas as pd

fname = '../data/january_flights.csv'
jan_flight_df = pd.read_csv(fname)

jan_flight_df['fl_date'] = pd.to_datetime(jan_flight_df['fl_date'])
jan = pd.to_datetime('2018-02-01')
jan_flight_df = jan_flight_df[jan_flight_df['fl_date'] < jan]
CITIES = jan_flight_df['origin_city_name'].unique().tolist()
CITIES_EX = ['New Orleans, LA',
             'Salt Lake City, UT',
             'Dallas/Fort Worth, TX']


def clean_response(response, year, month, city_name, i):
    """:returns dictionary with the weather for each day in a month for specified city"""
    if not response:
        print(response.status_code, city_name)
        raise Exception('Custom Error: Bad response')
    n_days = monthrange(year=int(year), month=int(month))[1]
    daily_weather = response.json().get('data', {}).get('weather', [])
    pois = ['windspeedKmph', 'visibility',
            'cloudcover', 'precipMM']  # 'totalSnow_cm' as well tho its stored in a different dict
    month = {}
    city = {}
    for day in range(n_days):
        cleaned = {}
        for key, index in zip(('00:00', '12:00'), (0, 1)):
            cleaned[key] = {k: daily_weather[day].get('hourly', [])[index].get(k, None) for k in pois}
            cleaned[key]['totalSnow_cm'] = daily_weather[day].get('totalSnow_cm', None)
            month[day+1] = cleaned
    city[city_name] = month
    print(f'returning {city_name}, {i}/{len(CITIES)}')
    return city


def get_weather_for_each_city(cities, url, year, month, headers=None, params=None):
    """ returns dictionary with weather for noon and midnight for a given month for the list of the cities"""
    headers = headers if headers else {}
    params = params if params else {}
    weather = {}
    weather['cities'] = []
    i = 0
    for city in cities:
        i += 1
        params['q'] = city
        res = requests.get(url, params=params, headers=headers)
        weather['cities'].append(clean_response(res, year, month, city, i))
    return weather


headers = {
}
params = {
    'q': '',  # location e.g. q=New+york,ny
    'date': '2018-01-01',  # date format yyyy-MM-dd
    'enddate': '2018-01-31',  # date format yyyy-MM-dd
    'format': 'json',
    'key': WEATHER_API_KEY,  # CHANGE TO YOUR API CODE
    'tp': '12'  # hour interval (do not change)
}
url = 'https://api.worldweatheronline.com/premium/v1/past-weather.ashx'

weather = get_weather_for_each_city(CITIES_EX, url, 2018, 1, headers=headers, params=params)
with open('january_weather.json', 'w') as fp:
    json.dump(weather, fp)

