import os

import requests

from fastapi import FastAPI, Query
from pydantic import Required

from database import Database

API_KEY = os.getenv("OPENWEATHER_API_KEY")

app = FastAPI()

db = Database()


@app.post("/weather/{city}")
async def add_city(city: str):
    """API method for adding a new city to the database"""

    url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric".format(city, API_KEY)

    response = requests.post(url)

    if response.status_code != 404:
        data = (response.json()["id"], response.json()["name"])
        db.add_new_city(data)
        return {"message": "[ SUCCESS ] City has been added: {}".format(response.json()["name"])}
    else:
        return {"message": "[ ERROR ] City not found"}


@app.get("/last_weather/")
async def get_all_cities(search: str | None = None):
    """API method for getting weather data for all database entries"""

    cities_list = db.read_all_cities(search)

    response = {
        "count": len(cities_list),
        "list": cities_list
    }

    return response


@app.get("/city_stats/")
async def get_city_stats(city_id: int = Query(default=Required), time_from: int | None = None, time_to: int | None = None):
    """API method for getting weather data of a specified city"""

    if time_from is not None and time_to is not None:
        return db.read_city_stats(city_id=city_id, time_from=time_from, time_to=time_to)

    elif time_from is not None and time_to is None:
        return db.read_city_stats(city_id=city_id, time_from=time_from)

    elif time_from is None and time_to is not None:
        return db.read_city_stats(city_id=city_id, time_to=time_to)
    else:
        return db.read_city_stats(city_id=city_id)
