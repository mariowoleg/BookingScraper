#!/usr/bin/env python3
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from src.spiders.booking_scrapper import BookingScrapperSpider
from webdriver_manager.chrome import ChromeDriverManager

def main():
    print("=" * 50)
    print("Iniciando programa para hacer WEB SCRAPING")
    print("=" * 50)

    #Configuració de Scrapy
    config = get_project_settings()
    config.update({
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'ROBOTSTXT_OBEY': False,
        'CONCURRENT_REQUESTS': 16,
        'REACTOR_THREADPOOL_MAXSIZE':20,
        'DOWNLOAD_DELAY': 0,
        'AUTOTHROTTLE_ENABLED': False,

        #Config de scrappy:
        'SELENIUM_DRIVER_NAME': 'chrome',
        'SELENIUM_DRIVER_EXECUTABLE_PATH': ChromeDriverManager().install(),
        'SELENIUM_DRIVER_ARGUMENTS': ['--no-sandbox', '--disable-dev-shm-usage'],

        #Middleware selenium
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_selenium.SeleniumMiddleware': 800
        },

        'FEEDS': {
            'dataset/booking_hotels_barcelona.json': {
                'format': 'json',
                'encoding': 'utf8',
                'indent': 4,
            },

            'dataset/booking_hotels_barcelona.csv': {
                'format': 'csv',
                'encoding': 'utf8',
                'fields': [
                    'id', 'title', 'city', 'description', 'tipus_allotjament',
                    'score', 'stars', 'rating_text', 'comments', 'image_url',
                    'hotel_url', 'original_price', 'current_price', 'exact_address', 'location_mark', 'cleanliness_mark',
                    'comfort_mark', 'facilities_mark', 'staff_mark', 'value_for_money_mark',
                    'wifi_mark', 'key_points', 'popular_services', 'last_comments'
                ],
            }
        },
        'LOG_LEVEL': 'INFO',

    })

    process = CrawlerProcess(settings=config)
    process.crawl(BookingScrapperSpider)
    process.start()


if __name__ == "__main__":
    main()