import requests

OPEN_WEATHER_MAP_APIKEY = 'f97e8a21e760edcece9e8bcebe2365c4'
degree_sign = u'\N{DEGREE SIGN}'

# 5098135  Fort Lee  NJ
# 5128581  New York City
# 6167863  Toronto

def get_weather_data_by_city_id(city_id):
    url = f'https://api.openweathermap.org/data/2.5/forecast?id={city_id}&appid={OPEN_WEATHER_MAP_APIKEY}&units=metric'
    print(f"Getting data via {url}")
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    else:
        return None

def get_min_max_temp(res_weather_data_json):

    if not res_weather_data_json:
        # fail to retreive data
        return None

    city_weather_json_lst = res_weather_data_json['list']
    min_temp_lst, max_temp_lst = [], []
    for idx in range(4):
        weather_in_3_hr = city_weather_json_lst[idx]['main']
        min_temp_lst.append(weather_in_3_hr['temp_min'])
        max_temp_lst.append(weather_in_3_hr['temp_max'])

    return min(min_temp_lst), max(max_temp_lst)

def get_weather_description(res_weather_data_json):
    if not res_weather_data_json:
        # fail to retreive data
        return None

    city_weather_json_lst = res_weather_data_json['list']
    weather_list = []
    last_weather = ""
    for idx in range(4):
        weather = city_weather_json_lst[idx]['weather'][0]['main']
        if weather != last_weather:
            weather_list.append(weather)
            last_weather = weather

    return " -> ".join(weather_list)

def get_info_by_city_id(city_id):
    res_weather_data_json = get_weather_data_by_city_id(city_id)
    min_temp, max_temp = get_min_max_temp(res_weather_data_json)
    weather = get_weather_description(res_weather_data_json)
    city_name = res_weather_data_json['city']['name']
    
    res = "{} 温度: {:.0f}-{:.0f}{}C 天气: {}".format(city_name, min_temp, max_temp, degree_sign, weather)
    return res


def get_openweather_info():
    fort_lee_info = get_info_by_city_id(5098135)
    nyc_info = get_info_by_city_id(5128581)
    toronto_info = get_info_by_city_id(6167865)
    res = "\n" + fort_lee_info + "\n" + nyc_info + "\n" + toronto_info
    return res

if __name__ == '__main__':
    print("Getting Weather Data")
    city_id = 5098135

    res = get_openweather_info()
    print(res)