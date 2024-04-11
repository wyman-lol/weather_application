# -*- coding: utf-8 -*-
# @Author: wyman
# @Date: 4/11/24
# @Description:

from flask import Flask, render_template
from flask_restx import Api, Resource, fields
from copy import deepcopy
from utils import geo_tools
from utils import http_tools
from datetime import datetime

app = Flask(__name__)
api = Api(app, version='1.0', title='weather application API', description='A simple API', doc="/docs")
ns = api.namespace('weather', description='weather operations', path="/weather")

weather_daily_model = api.model('weather_daily', {
    'date': fields.String(readonly=True, description='Date'),
    'weather': fields.String(readonly=True, description='Weather'),
    'temp_min': fields.Integer(readonly=True, description='The lowest temperature of the day, unit: Celsius'),
    'temp_max': fields.Integer(readonly=True, description='The highest temperature of the day, unit: Celsius'),
    'wind_max': fields.Integer(readonly=True, description='The maximum wind speed for the day, unit: m/s'),
})


@ns.route('/<city_name>')
@ns.param('city_name', 'The city name')
class Weather(Resource):

    @ns.doc('get the weather information by city name')
    @ns.marshal_with(weather_daily_model, as_list=True)
    def get(self, city_name):
        """Get the weather information by city name"""
        result = []

        location = geo_tools.get_city_location(city_name)
        if not location:
            return result, 500

        weather_forecast = http_tools.get_weather_forecast(longitude=location[0], latitude=location[1])

        data_series = weather_forecast["dataseries"]
        data_series.sort(key=lambda x: x['date'])

        for daily_weather in data_series:
            daily_data = deepcopy(weather_daily_model)
            daily_data["date"] = datetime.strptime(str(daily_weather["date"]), "%Y%m%d").strftime("%Y-%m-%d")
            daily_data["weather"] = daily_weather["weather"]
            daily_data["temp_min"] = daily_weather["temp2m"]["min"]
            daily_data["temp_max"] = daily_weather["temp2m"]["max"]
            daily_data["wind_max"] = daily_weather["wind10m_max"]

            result.append(daily_data)

        return result


@app.route("/index.html")
def get_index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=False)
