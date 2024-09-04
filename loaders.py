import re
from typing import Tuple

import httpx
from scrapy import Selector

TAXI_DATA_PAGE_URL = 'https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page'


def sort_by_year_month(s: str) -> Tuple[int, int]:
    search = re.search(r"(\d{4})-(\d{2})", s)
    return int(search.group(1)), int(search.group(2))


def get_latest_taxi_file_hyperlink() -> list[str]:
    response = httpx.get(TAXI_DATA_PAGE_URL, timeout=10)
    selector = Selector(text = response.content)
    hyperlinks = selector.xpath('//div[@class="faq-answers"]//li//a/@href').getall()
    hyperlinks = sorted(hyperlinks, key=sort_by_year_month)
    return hyperlinks[-1]
