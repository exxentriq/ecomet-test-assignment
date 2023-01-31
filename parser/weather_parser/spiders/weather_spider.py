import os
import json
import datetime

import scrapy

from database import Database

API_KEY = os.getenv("OPENWEATHER_API_KEY")


class WeatherSpider(scrapy.Spider):
    name = "weather_spider"

    def start_requests(self):
        db = Database()

        for city_id in db.read_all_ids():
            yield scrapy.Request(
                "https://api.openweathermap.org/data/2.5/weather?id={}&appid={}&units=metric".format(city_id, API_KEY))

    def parse(self, response):
        try:
            # Parse JSON from response
            json_response = json.loads(response.text)
        except json.decoder.JSONDecodeError:
            print("[ PARSE ERROR ]")

        # This cannot happen
        if json_response["cod"] == "404":
            print("[ ERROR ] City not found")
            return None

        weather_data = {
            "city_id": json_response["id"],
            "temperature_celsius": json_response["main"]["temp"],
            "atmospheric_pressure": json_response["main"]["pressure"],
            "wind_speed": json_response["wind"]["speed"],
            "time_updated": datetime.datetime.timestamp(datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0))
        }

        yield weather_data
