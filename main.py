import sqlite3

from typing import Union
from fastapi import FastAPI, Query
from pydantic import Required

import scrapy.crawler as crawler
from multiprocessing import Process, Queue
from twisted.internet import reactor
from scrapy.utils.log import configure_logging
from weather_parser.weather_parser.spiders.city_name_spider import CityNameSpider

app = FastAPI()

DATABASE = "weather_data.db"

def run_spider(spider, city_name):
    def spawn_crawler(queue, city_name):
        try:
            runner = crawler.CrawlerRunner({
                "USER_AGENT": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
                "DOWNLOAD_DELAY": 2,
                "HTTPERROR_ALLOWED_CODES": [404]
            })
            deferred = runner.crawl(spider, city_name=city_name)
            deferred.addBoth(lambda _: reactor.stop())
            reactor.run()
            queue.put(None)
        except Exception as exception:
            queue.put(exception)

    queue = Queue()
    process = Process(target=spawn_crawler, args=(queue, city_name))
    process.start()
    result = queue.get()
    process.join()

    if result is not None:
        raise result


@app.post("/weather/{city}")
async def add_city(city: str):
    """API method for adding a new city to the database"""

    configure_logging()
    run_spider(CityNameSpider, city)
    
    return {"city_name": city, "message": "Success"}


@app.get("/last_weather/")
async def get_all_cities(search: str | None = None):
    """API method for getting weather data for all database entries"""

    con = sqlite3.connect(DATABASE)
    cur = con.cursor()

    cities_list = []

    if search is not None:
        for row in cur.execute("SELECT city_id, city_name, temperature_celsius, atmospheric_pressure, wind_speed, last_updated FROM cities WHERE city_name LIKE '%{}%'".format(search)):
            cities_list.append({
                "city_id": row[0],
                "city_name": row[1],
                "temperature_celsius": row[2],
                "atmospheric_pressure": row[3],
                "wind_speed": row[4],
                "last_updated": row[5]
            })

    else:
        for row in cur.execute("SELECT city_id, city_name, temperature_celsius, atmospheric_pressure, wind_speed, last_updated FROM cities"):
            cities_list.append({
                "city_id": row[0],
                "city_name": row[1],
                "temperature_celsius": row[2],
                "atmospheric_pressure": row[3],
                "wind_speed": row[4],
                "last_updated": row[5]
            })

    response = {
        "count": len(cities_list),
        "list": cities_list
    }

    return response


@app.get("/city_stats/")
async def get_city_stats(city_id: int = Query(default=Required)):
    """API method for getting weather data of a specified city"""

    pass