# -*- coding: utf-8 -*-
# @Author: wyman
# @Date: 4/11/24
# @Description:

# """
# https://github.com/public-apis/public-apis#weather
# http://www.7timer.info/bin/api.pl?lon=113.17&lat=23.09&product=civillight&output=json
# https://www.7timer.info/bin/astro.php?lon=113.17&lat=23.09&product=civillight&output=json
# """

import requests
from http import HTTPStatus

EXTERNAL_WEATHER_API = "http://www.7timer.info/bin/api.pl?lon={longitude}&lat={latitude}s&product=civillight&output=json"


def get_weather_forecast(longitude: float, latitude: float) -> dict:
    """
    get weather forecast for the next 7 days
    :param longitude:
    :param latitude:
    :return: Weather forecast for the next 7 days
    return example:
    {'init': '2024041018',
    'product': 'civillight'
    'dataseries': [{'date': 20240411,
                 'temp2m': {'max': 29, 'min': 28},
                 'weather': 'ts',
                 'wind10m_max': 3},
                {'date': 20240412,
                 'temp2m': {'max': 29, 'min': 26},
                 'weather': 'lightrain',
                 'wind10m_max': 3},

               ...

                {'date': 20240417,
                 'temp2m': {'max': 29, 'min': 28},
                 'weather': 'lightrain',
                 'wind10m_max': 3}],
    }
    """
    url = EXTERNAL_WEATHER_API.format(longitude=longitude, latitude=latitude)
    response = requests.get(url, verify=False)

    if response.status_code != HTTPStatus.OK:
        raise Exception(f"Fetch weather forecast failed, url: {url}")

    return response.json()


if __name__ == '__main__':
    from pprint import pprint

    pprint(get_weather_forecast(113.2592945, 23.1301964))  # 广州
    pprint(get_weather_forecast(116.412144, 40.190632))  # 北京
    pprint(get_weather_forecast(-74.0060152, 40.7127281))  # New York
