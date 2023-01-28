import sqlite3
import json
from datetime import datetime

import scrapy


API_KEY = "b3fb727402f0bdcc2bdd7ad440fe20ca"
DATABASE = "weather_data.db"

class CityNameSpider(scrapy.Spider):
    name = "city_name_spider"

    def start_requests(self):
        self.db_inserter = DatabaseInserter()
        self.db_inserter.open_database()

        city_name = getattr(self, 'city_name', None)

        if city_name is not None:
            url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric".format(city_name, API_KEY)

        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        try:
            # Parse JSON from response
            json_response = json.loads(response.text)
        except json.decoder.JSONDecodeError:
            print("[ PARSE ERROR ]")

        if json_response["cod"] == "404":
            print("[ ERROR ] City not found")
            return None

        weather_data = {
            "city_id": json_response["id"],
            "city_name": json_response["name"],
            "temperature_celsius": json_response["main"]["temp"],
            "atmospheric_pressure": json_response["main"]["pressure"],
            "wind_speed": json_response["wind"]["speed"],
            "last_updated": datetime.timestamp(datetime.now())
        }

        self.db_inserter.insert_data(weather_data)
        self.db_inserter.close_database()

        return weather_data


class DatabaseInserter:
    def open_database(self):
        self.con = sqlite3.connect(DATABASE)
        self.cur = self.con.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS cities(city_id, city_name, temperature_celsius, atmospheric_pressure, wind_speed, last_updated, UNIQUE(city_id))")

    def insert_data(self, item):
        data = (
            item["city_id"],
            item["city_name"],
            item["temperature_celsius"],
            item["atmospheric_pressure"],
            item["wind_speed"],
            item["last_updated"]
        )
        self.cur.execute("""INSERT INTO cities(city_id, city_name, temperature_celsius, atmospheric_pressure, wind_speed, last_updated)
                            VALUES (?, ?, ?, ?, ?, ?)""", data)
        self.con.commit()

        return item

    def close_database(self):
        self.con.close()