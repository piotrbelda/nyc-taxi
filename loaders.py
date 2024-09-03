import httpx
from scrapy import Selector

TAXI_DATA_PAGE_URL = 'https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page'

response = httpx.get(TAXI_DATA_PAGE_URL, timeout=10)
selector = Selector(text = response.content)
file_hyperlink = selector.xpath('//div[@class="faq-answers"]//li//a/@href').get()

def get_latest_taxi_file_hyperlink():
    pass

breakpoint()
