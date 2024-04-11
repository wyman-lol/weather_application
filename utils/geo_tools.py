# -*- coding: utf-8 -*-
# @Author: wyman
# @Date: 4/11/24
# @Description:
from geopy.geocoders import Nominatim


def get_city_location(city_name: str) -> tuple[float, float] | None:
    """
    Get latitude and longitude by the city name.
    :param city_name: city name
    :return:
    """
    geolocator = Nominatim(user_agent="weather_application")

    location = geolocator.geocode(city_name)

    if location:
        return location.longitude, location.latitude
    else:
        return None


if __name__ == '__main__':
    print(get_city_location("广州"))
    print(get_city_location("北京"))
    print(get_city_location("New York"))
