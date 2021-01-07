from flask import Flask, url_for, render_template
from typing import Dict, List
import requests
import os

LIST = 'list'
MAIN = 'main'
TEMP_MIN = 'temp_min'
CITY = 'city'
os.environ[
    'URL'] = 'http://api.openweathermap.org/data/2.5/forecast?q={}&appid=4796f3765df8979006c4bc9c3ffc6719&units=metric'

lowest_temp_city = None
lowest_temp_overall = float('inf')


def get_min_dict() -> Dict:
    cities_list = ['Tel-aviv', 'Berlin', 'Budapest']
    return create_dict(cities_list)


def create_dict(cities_list: List[str]) -> Dict:
    min_data_dict = {}
    for city in cities_list:
        city_data = get_data(city)
        min_data_dict[city] = update_dict(city_data, city)
    return min_data_dict[lowest_temp_city]


def get_data(city):
    try:
        curr_url = os.environ.get('URL').format(city)
        response = requests.get(curr_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)


def update_dict(city_data, city) -> Dict:
    curr_info_min = find_min_temp_min(city_data)
    curr_temp_min = curr_info_min[TEMP_MIN]
    if curr_temp_min < lowest_temp_overall:
        update_lowest_temp_overall(curr_temp_min, city)
    return get_city_dict(city, curr_info_min)


def find_min_temp_min(city_data):
    curr_temp_min = city_data[LIST][0][MAIN][TEMP_MIN]
    for weather_info in city_data[LIST][1:]:
        curr_temp = weather_info[MAIN][TEMP_MIN]
        if curr_temp < curr_temp_min:
            curr_temp_min = curr_temp
            curr_info_min = (weather_info[MAIN])
    return curr_info_min


def update_lowest_temp_city(city):
    global lowest_temp_city
    lowest_temp_city = city


def update_lowest_temp_overall(curr_temp_min, city):
    update_lowest_temp_city(city)
    global lowest_temp_overall
    lowest_temp_overall = curr_temp_min


def get_city_dict(city, curr_info_min) -> Dict:
    city_dict = {CITY: city}
    city_dict.update(curr_info_min)
    return city_dict


app = Flask(__name__)


@app.route("/get_lowest_temp")
def get_lowest_temp():
    return render_template("index.html", min_data_dict=get_min_dict(),
                           lowest_temp_city=lowest_temp_city)


if __name__ == "__main__":
    app.run()
