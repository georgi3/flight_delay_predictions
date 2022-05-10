import requests
from src.config import WEATHER_API_KEY
import json
import pandas as pd
from calendar import monthrange

fn_flight = '../data/flight_data.csv'
flight_df = pd.read_csv(fn_flight)



# get all the cities
cities = flight_df['origin_city_name'].unique().tolist()

flight_df['fl_date'] = pd.to_datetime(flight_df['fl_date'])
date_before = pd.to_datetime('2018-02-01')
flight_df2018 = flight_df[flight_df['fl_date'] < date_before]
flight_df2018['origin_city_name'].unique()

dic_format = {
    2018: {  # year
        1: {  # month
            'New Orleans, LA': {  # city
                1: {  # day
                    '00:00': {},  # noon weather
                    '12:00': {},  # midnight weather
                }
            }
        }
    }
}


def clean_response(response, year, month, city_name, i):
    """:returns dictionary with the weather for each day in a month for specified city"""
    if not response:
        print(response.status_code, city_name)
        return response.json()
    n_days = monthrange(year=int(year), month=int(month))[1]
    daily_weather = response.json().get('data', {}).get('weather', [])
    pois = ['windspeedKmph', 'visibility', 'cloudcover', 'precipMM']  # 'totalSnow_cm' as well tho its stored in a different dict
    city = {}

    for day in range(n_days):
        cleaned = {}
        for key, index in zip(('00:00', '12:00'), (0, 1)):
            cleaned[key] = {k:daily_weather[day].get('hourly', [])[index].get(k, None) for k in pois}
            cleaned[key]['totalSnow_cm'] = daily_weather[day].get('totalSnow_cm', None)
            city[day+1] = cleaned
    print(f'returning {city_name}, {i}/362')
    return city


def get_weather_for_each_city(cities, url, year, month, file, headers=None, params=None):
    headers = headers if headers else {}
    params = params if params else {}
    weather = {}
    try:
        if not weather[year]:
            pass
    except KeyError:
        weather[year] = {}
    weather[year][month] = {}
    i = 0
    for city in cities:
        i += 1
        params['q'] = city
        res = requests.get(url, params=params, headers=headers)
        weather[year][month][city] = clean_response(res, year, month, city, i)
    return weather


headers = {
}
params = {
    'q': '',  # location e.g. q=New+york,ny
    'date': '2018-01-01',  # date format yyyy-MM-dd
    'enddate': '2018-01-31',
    'format': 'json',
    'key': WEATHER_API_KEY,
    'tp': '12'
}
url = 'https://api.worldweatheronline.com/premium/v1/past-weather.ashx'

weather = get_weather_for_each_city(cities, url, 2018, 1, '', headers=headers, params=params)


with open('january_weather.json', 'w') as fp:
    json.dump(weather, fp)
