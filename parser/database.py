import os
import sqlite3
from datetime import date

DATABASE = os.getenv("SQLITE3_DATABASE")


class Database:
    def __init__(self):
        """Creates database structure if it does not exist"""

        con = sqlite3.connect(DATABASE)
        cur = con.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS cities (
                city_id int PRIMARY_KEY,
                city_name varchar(255),
                UNIQUE(city_id)
        )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS weather_records (
                city_id int REFERENCES cities(city_id) ON DELETE CASCADE,
                temperature_celsius real,
                atmospheric_pressure int,
                wind_speed real,
                time_updated timestamp
        )
        """)

        con.commit()
        con.close()

    def insert_data(self, data):
        """Creates database structure"""

        con = sqlite3.connect(DATABASE)
        cur = con.cursor()

        cur.execute("""INSERT INTO weather_records(city_id, temperature_celsius, atmospheric_pressure, wind_speed, time_updated)
                            VALUES (?, ?, ?, ?, ?)""", data)

        con.commit()
        con.close()

    def add_new_city(self, data):
        """Adds new city to the database"""

        con = sqlite3.connect(DATABASE)
        cur = con.cursor()

        cur.execute("""INSERT INTO cities(city_id, city_name)
                            VALUES (?, ?)""", data)

        con.commit()
        con.close()

    def read_all_cities(self, search = None):
        """Reads all added cities with their last recorded temperatures"""

        con = sqlite3.connect(DATABASE)
        cur = con.cursor()

        cities_list = []

        if search is not None:
            for row in cur.execute(f"""
                SELECT city_id, city_name,
                (SELECT temperature_celsius FROM weather_records ORDER BY time_updated DESC LIMIT 1)
                FROM cities WHERE city_name LIKE '%{search}%'
            """):
                cities_list.append({
                    "city_id": row[0],
                    "city_name": row[1],
                    "temperature_celsius": row[2],
                })
        else:
            for row in cur.execute("""
                SELECT city_id, city_name,
                (SELECT temperature_celsius FROM weather_records ORDER BY time_updated DESC LIMIT 1)
                FROM cities
            """):
                cities_list.append({
                    "city_id": row[0],
                    "city_name": row[1],
                    "temperature_celsius": row[2],
                })

        con.close()
        
        return cities_list

    def read_all_ids(self):
        """Reads all added IDs from OpenWeatherMap"""

        con = sqlite3.connect(DATABASE)
        cur = con.cursor()

        id_list = []

        for row in cur.execute("""SELECT city_id FROM cities"""):
            id_list.append(row[0])

        con.close()
        
        return id_list

    def read_city_stats(self, city_id, time_from = None, time_to = None):
        """Reads all city stats for the specified period"""

        con = sqlite3.connect(DATABASE)
        cur = con.cursor()

        if time_from is not None and time_to is not None:
            all_records = []

            for row in cur.execute(f"""
                SELECT city_id, temperature_celsius, atmospheric_pressure, wind_speed, time_updated
                FROM weather_records
                ORDER BY time_updated DESC
                WHERE city_id = {city_id} AND time_updated >= {time_from} AND time_updated <= {time_to}
            """):
                all_records.append({
                    "temperature_celsius": row[1],
                    "atmospheric_pressure": row[2],
                    "wind_speed": row[3],
                    "time_updated": date.fromtimestamp(row[4])
                })

            average_values = cur.execute(f"""
                SELECT AVG(temperature_celsius), AVG(atmospheric_pressure), AVG(wind_speed)
                FROM weather_records
                ORDER BY time_updated DESC
                WHERE city_id = {city_id} AND time_updated >= {time_from} AND time_updated <= {time_to}
            """)

            data = {
                "city_id": city_id,
                "records_count": len(all_records),
                "average_temperature": average_values[0],
                "average_pressure": average_values[1],
                "average_wind_speed": average_values[2],
                "time_from": date.fromtimestamp(time_from),
                "time_to": date.fromtimestamp(time_to),
                "all_records": all_records
            }

        elif time_from is not None and time_to is None:
            all_records = []

            for row in cur.execute(f"""
                SELECT city_id, temperature_celsius, atmospheric_pressure, wind_speed, time_updated
                FROM weather_records
                ORDER BY time_updated DESC
                WHERE city_id = {city_id} AND time_updated >= {time_from}
            """):
                all_records.append({
                    "temperature_celsius": row[1],
                    "atmospheric_pressure": row[2],
                    "wind_speed": row[3],
                    "time_updated": date.fromtimestamp(row[4])
                })

            average_values = cur.execute(f"""
                SELECT AVG(temperature_celsius), AVG(atmospheric_pressure), AVG(wind_speed)
                FROM weather_records
                ORDER BY time_updated DESC
                WHERE city_id = {city_id} AND time_updated >= {time_from}
            """)

            last_updated = cur.execute(f"""
                SELECT time_updated
                FROM weather_records
                ORDER BY time_updated DESC
                LIMIT 1
                WHERE city_id = {city_id} AND time_updated >= {time_from}
            """)

            data = {
                "city_id": city_id,
                "records_count": len(all_records),
                "average_temperature": average_values[0],
                "average_pressure": average_values[1],
                "average_wind_speed": average_values[2],
                "time_from": date.fromtimestamp(time_from),
                "time_to": date.fromtimestamp(last_updated),
                "all_records": all_records
            }

        elif time_from is None and time_to is not None:
            all_records = []

            for row in cur.execute(f"""
                SELECT city_id, temperature_celsius, atmospheric_pressure, wind_speed, time_updated
                FROM weather_records
                ORDER BY time_updated DESC
                WHERE city_id = {city_id} AND time_updated <= {time_to}
            """):
                all_records.append({
                    "temperature_celsius": row[1],
                    "atmospheric_pressure": row[2],
                    "wind_speed": row[3],
                    "time_updated": date.fromtimestamp(row[4])
                })

            average_values = cur.execute(f"""
                SELECT AVG(temperature_celsius), AVG(atmospheric_pressure), AVG(wind_speed)
                FROM weather_records
                ORDER BY time_updated DESC
                WHERE city_id = {city_id} AND time_updated <= {time_to}
            """)

            first_updated = cur.execute(f"""
                SELECT time_updated
                FROM weather_records
                ORDER BY time_updated ASC
                LIMIT 1
                WHERE city_id = {city_id} AND time_updated <= {time_to}
            """)

            data = {
                "city_id": city_id,
                "records_count": len(all_records),
                "average_temperature": average_values[0],
                "average_pressure": average_values[1],
                "average_wind_speed": average_values[2],
                "time_from": data.fromtimestamp(first_updated),
                "time_to": date.fromtimestamp(time_to),
                "all_records": all_records
            }

        else:
            all_records = []

            for row in cur.execute(f"""
                SELECT city_id, temperature_celsius, atmospheric_pressure, wind_speed, time_updated
                FROM weather_records
                ORDER BY time_updated DESC
                WHERE city_id = {city_id}
            """):
                all_records.append({
                    "temperature_celsius": row[1],
                    "atmospheric_pressure": row[2],
                    "wind_speed": row[3],
                    "time_updated": date.fromtimestamp(row[4])
                })

            average_values = cur.execute(f"""
                SELECT AVG(temperature_celsius), AVG(atmospheric_pressure), AVG(wind_speed)
                FROM weather_records
                ORDER BY time_updated DESC
                WHERE city_id = {city_id}
            """)

            first_updated = cur.execute(f"""
                SELECT time_updated
                FROM weather_records
                ORDER BY time_updated ASC
                LIMIT 1
                WHERE city_id = {city_id}
            """)

            last_updated = cur.execute(f"""
                SELECT time_updated
                FROM weather_records
                ORDER BY time_updated DESC
                LIMIT 1
                WHERE city_id = {city_id}
            """)

            data = {
                "city_id": city_id,
                "records_count": len(all_records),
                "average_temperature": average_values[0],
                "average_pressure": average_values[1],
                "average_wind_speed": average_values[2],
                "time_from": date.fromtimestamp(first_updated),
                "time_to": date.fromtimestamp(last_updated),
                "all_records": all_records
            }

        con.close()

        return data
