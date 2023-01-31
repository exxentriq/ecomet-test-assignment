from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from weather_parser.spiders.weather_spider import WeatherSpider


if __name__ == "__main__":
    process = CrawlerProcess(get_project_settings())

    process.crawl(WeatherSpider)
    process.start()  # the script will block here until the crawling is finished
