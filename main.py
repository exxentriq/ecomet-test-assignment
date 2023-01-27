from typing import Union
from fastapi import FastAPI

app = FastAPI()


@app.post("/weather/{city}")
async def add_city(city: str):
    """API method for adding a new city to the database"""

    pass


@app.get("/last_weather/")
async def get_all_cities(search: str | None = None):
    """API method for getting weather data for all database entries"""

    pass


@app.get("/city_stats/")
async def get_city_stats(city_id: int = Query(default=Required)):
    """API method for getting weather data of a specified city"""

    pass