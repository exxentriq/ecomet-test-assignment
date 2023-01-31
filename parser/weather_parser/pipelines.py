# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from database import Database


class DatabaseInserterPipeline:
    """Processes data and inserts into SQLite database"""

    def open_spider(self, spider):
        # Initialize the database
        self.db = Database()

    def process_item(self, item, spider):
        data = (
            item["city_id"],
            item["temperature_celsius"],
            item["atmospheric_pressure"],
            item["wind_speed"],
            item["time_updated"]
        )
        self.db.insert_data(data)
